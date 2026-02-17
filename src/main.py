#!/usr/bin/env python3
import boto3
import logger_config
import disk_utils
from aws_utils import verify_and_log_aws_identity, list_my_buckets
# Import the backup function
from backup_to_s3 import ensure_secure_bucket, backup_to_s3 

def main():
    # 1. Initialize the logger
    logger_config.setup_logging()
    
    # 2. Run the identity check
    verify_and_log_aws_identity()
        # list_my_buckets()
    
    # 3. Check size of home folder
    home = disk_utils.get_home_path()
    total_bytes = disk_utils.get_dir_size(home)
    # Using your existing format_size utility for a prettier output
    print(f"Total space used in {home}: {disk_utils.format_size(total_bytes)}")

    # 4. Define your bucket name
    bucket_name = "ubuntu-cloud-backup-bucket"
    
    # 5. Initialize the Boto3 client
    s3_client = boto3.client('s3')

    # 6. Ensure bucket exists and is private
    ensure_secure_bucket(s3_client, bucket_name)

    # 7. RUN THE BACKUP
    print(f"\n--- Starting Backup to S3: {bucket_name} ---")
    backup_to_s3(s3_client, bucket_name, home)
    print("\n--- Backup Complete ---")

if __name__ == "__main__":
    main()