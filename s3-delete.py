import boto3
import argparse
from datetime import date, timedelta

def cli():
    """setup command-line arguments"""
    options = argparse.ArgumentParser()       
    options.add_argument('--url', help="s3 api endpoint url", required=True)
    options.add_argument('--keyid', help="s3 access key id", required=True)  
    options.add_argument('--secret', help="s3 secret access key", required=True)  
    options.add_argument("--bucket", help="bucket name", required=True)   
    options.add_argument("--days", help="older than days", required=True)  
    return options


def main(endpoint_url, access_key_id, secret_access_key, bucket_name, older_than_days):
    verify_ssl = False

    # prepare previous date
    older_than_date = date.today() - timedelta(days=int(older_than_days))

    # init the s3 client
    s3 = boto3.client('s3', endpoint_url=endpoint_url, 
                            aws_access_key_id=access_key_id, 
                            aws_secret_access_key=secret_access_key,
                            verify=verify_ssl )

    # search all objects older than the provided days
    print(f"> s3api list-object-versions older than {older_than_days} days")
    s3_paginator = s3.get_paginator('list_object_versions')
    s3_iterator = s3_paginator.paginate(Bucket=bucket_name)
    filtered_iterator = s3_iterator.search(
        "Versions[?to_string(LastModified)<='\"%s\"'].{Key: Key,VersionId: VersionId}" % older_than_date
    )

    # iter over result and delete the object
    count = 0
    for obj in filtered_iterator:
        if obj is None: continue
        count+= 1
        print(f"> s3 api delete-object {bucket_name} {obj['Key']} {obj['VersionId']}")
        _ = s3.delete_object(
            Bucket=bucket_name,
            Key=obj['Key'],
            VersionId=obj['VersionId'],
        )
    print(f"< {count} objects deleted")

if __name__ == '__main__':
    options = cli()
    args = options.parse_args()
    main(args.url, args.keyid, args.secret, args.bucket, args.days)
