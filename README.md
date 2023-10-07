# Some scripts for S3 objects storage

## Delete objects older than xx days

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
