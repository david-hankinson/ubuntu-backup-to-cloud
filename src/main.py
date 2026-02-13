#!/usr/bin/env python3
from pathlib import Path

import boto3
import logger_config
import disk_utils
from aws_utils import verify_and_log_aws_identity, list_my_buckets
from backup_to_s3 import ensure_secure_bucket

def main():
    # Initialize the logger
    logger_config.setup_logging()
    
    # Run the identity check
    if verify_and_log_aws_identity():
        # Only list buckets if identity is verified
        list_my_buckets()
    
    # Check size of home folder
    home = disk_utils.get_home_path()
    total_bytes = disk_utils.get_dir_size(home)
    print(f"Total space used in {home}: {total_bytes / (1024**3):.2f} GB")

    # Define your bucket name
    bucket_name = "REDACTED"
    
    # 2. Initialize the Boto3 client
    # This uses the AWS credentials configured on your machine
    s3_client = boto3.client('s3')

    ensure_secure_bucket(s3_client, bucket_name)

if __name__ == "__main__":
    main()