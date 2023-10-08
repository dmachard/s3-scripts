import boto3
import os

import s3config
s3 = boto3.client('s3', **s3config.cfg )

folder_path = "/var/log"
bucket_name = "test-bucket5"

for root, dirs, files in os.walk(folder_path):
    for name in files:
        print(f"upload {name}")
        s3.upload_file(os.path.join(root, name), bucket_name, name)
    break