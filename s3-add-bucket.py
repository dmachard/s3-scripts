import boto3

import s3config
s3 = boto3.client('s3', **s3config.cfg )

bucket_name = "test-bucket5"

response = s3.create_bucket(ACL='private', Bucket=bucket_name)
print(response["Location"])
