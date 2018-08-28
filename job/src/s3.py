import boto3

class S3Bucket:
    def __init__(self, bucket_name: str):
        self.bucket = boto3.resource('s3').Bucket(bucket_name)

    def put_files(self, local_path: str, destination: str):
                self.bucket.upload_file(local_path, destination,
                                        ExtraArgs={
                                            'ServerSideEncryption': 'AES256'
})