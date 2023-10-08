# Some scripts for S3 objects storage

## (shell) delete objects older than xx days

> `awscli` and `jq` are mandatory to use this script.

Script usage:

```bash
$ ./s3-delete.sh
USAGE: ./s3-delete.sh [s3-endpoint-url] [bucket-name] [days]
```

Example to delete all objects older than 10 days in the bucket `test`

```bash
$./s3-delete.sh https://s3api test 10
> ls s3://test
> s3api list-object-versions older than 0 days
< 2 objects detected
> s3 api delete-object test file1.txt 198a5b42-e7d3-447f-9883-a580581fee49
> s3 api delete-object test file2.txt 0c5b1164-5177-4c48-9a40-c0dd15d0c02a
```

## (python) delete objects older than xx days

Install prerequisites

```bash
pip install boto3
```

Usage

```bash
$ python3 s3-delete.py
usage: s3-delete.py [-h] --api-url API_URL --bucket BUCKET --days DAYS
s3-delete.py: error: the following arguments are required: --api-url, --bucket, --days
```

```bash
$ python3 s3-delete.py --url http://127.0.0.1:9000 --keyid dd7H5P6oILzBF8rIY5ai --secret C3Sfev3nf5lgX9PzTGoibwKmtbmqjOpJFWaDHl0I --bucket pdnsbackup --days 0
> s3api list-object-versions older than 0 days
> s3 api delete-object test backup.tar.gz b97bfd89-3835-4f18-b0f6-6976c7dc9432
> s3 api delete-object test backup.tar.gz 89c31db7-4bd5-49b4-aea9-749f577edc61
< 2 objects detected
```
