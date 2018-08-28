import os

import helper_functions
from configuration import Configuration
from helper_functions import log_job_status, print_version_from_file
from s3 import S3Bucket

# create folder
TMP_DIR = '/tmp/dim-hotel/'

def setup(config):
    bucket_name = config.get('s3_bucket')
    prefix = config.get('s3_prefix')

    return bucket_name, prefix

def upload(s3_bucket, prefix):
    # should be the tmp_dir
    local_path = ''
    file_type = 'dim_hotel'
    filename = 'hotel_lookup'
    destination = os.path.join(prefix, file_type, filename)
    print('Uploading...', destination)
    s3_bucket.put_files(local_path, destination)




@log_job_status
def main(config: Configuration):
    # Execute job here
    # bucket_name, prefix = setup(config)
    # s3_bucket = S3Bucket(bucket_name)
    print ('UPLOAD ABOUT TO BEGIN!')
    # upload(s3_bucket, prefix)


if __name__ == "__main__":
    print_version_from_file('VERSION')
    default_config_path = os.path.join(os.path.dirname(__file__), 'config/config.ini')
    config = Configuration([default_config_path])
    config.print_as_json()
    main(config)
