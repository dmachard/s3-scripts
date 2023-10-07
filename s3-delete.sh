#!/bin/bash

if [[ $# != 3 ]] ; then
  echo 'USAGE: ./s3-delete.sh [s3-endpoint-url] [bucket-name] [days]'
  exit 0
fi

ENDPOINT_URL=$1
BUCKET_NAME=$2
OLDER_THAN_DAYS=$3
OLDER_THAN_DATE=$(date --date="$OLDER_THAN_DAYS days ago" +"%Y-%m-%d""T""%H:m:%S.000000")

echo "> ls s3://$BUCKET_NAME"
aws s3 ls --endpoint-url "$ENDPOINT_URL" "s3://$BUCKET_NAME" 1>/dev/null 2>&1
if [[ $? -ne 0 ]]; then
    echo "< error - bucket $BUCKET_NAME does not exist"
    exit 1
fi

echo "> s3api list-object-versions older than $OLDER_THAN_DAYS days"
objects=$(aws s3api list-object-versions --endpoint-url "$ENDPOINT_URL" --bucket "$BUCKET_NAME" --query "Versions[?LastModified<='$OLDER_THAN_DATE'].{Key: Key,VersionId: VersionId}"  --output json)
if [[ $? -ne 0 ]]; then
    echo "< error - unable to fetch objects"
    exit 1
fi

count=$(echo "$objects" | jq 'length')
if [[ "$count" == 0 ]]; then
   echo "< no objects, do nothing"
   exit 0
else
   echo "< $count objects detected"
fi

for obj in $(echo $objects | jq -c '.[]'); do
  objectKey=$(jq -r '.Key' <<< "$obj")
  versionId=$(jq -r '.VersionId' <<< "$obj")

  echo "> s3 api delete-object" $BUCKET_NAME $objectKey $versionId
  aws s3api delete-object --endpoint-url "$ENDPOINT_URL" --bucket "$BUCKET_NAME" --key "$objectKey" --version-id "$versionId" --output text 1>/dev/null 2>&1
  if [[ $? -ne 0 ]]; then
     echo "< error - unable to delete object"
     exit
  fi
done
