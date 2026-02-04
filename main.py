#!/usr/bin/env python3

import boto3
import logging
from logging.handlers import TimedRotatingFileHandler

# --- 1. Setup Rotating Logging ---
log_filename = 'ubuntu-backup-to-s3.log'

# Create a handler that rotates every day at midnight
# backupCount=7 means it keeps 7 days of history before deleting the oldest
handler = TimedRotatingFileHandler(
    log_filename,
    when="midnight",
    interval=1,
    backupCount=7,
    encoding='utf-8'
)

# Set the suffix for the rotated files (e.g., ubuntu-backup-to-s3.log.2026-02-04)
handler.suffix = "%Y-%m-%d"

# Configure the logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Attach the handler to the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def verify_and_log_aws_identity():
    """
    Retrieves the AWS caller identity, masks only the Account ID, 
    and logs the full username for clarity.
    """
    sts = boto3.client('sts')

    try:
        identity = sts.get_caller_identity()
        account_id = identity['Account']
        arn = identity['Arn']

        # Mask the Account ID
        masked_account = f"{'*' * 8}{account_id[-4:]}"

        # Mask the ARN's Account ID segment, but keep the username
        parts = arn.split(':')
        if len(parts) > 4:
            parts[4] = masked_account  # Replace the 12-digit ID with the mask
        
        masked_arn = ":".join(parts)

        # Log and Print
        logging.info(f"Identity Verified | Account: {masked_account} | ARN: {masked_arn}")
        
        print(f"Proceeding on account ID: {masked_account}")
        print(f"Using ARN: {masked_arn}")

    except Exception as e:
        logging.error(f"Failed to verify AWS identity: {e}")
        print(f"Error: {e}")

def list_my_buckets():
    # Create session to AWS account
    s3 = boto3.client('s3')

    logging.info("Starting S3 bucket list request...")
    
    try:
        response = s3.list_buckets()
        print("--- Your S3 Buckets ---")
        
        for bucket in response['Buckets']:
            name = bucket['Name']
            print(f"Bucket Name: {name}")
            logging.info(f"Found bucket: {name}")
            
    except Exception as e:
        error_msg = f"Error connecting to AWS: {e}"
        print(error_msg)
        logging.error(error_msg)

if __name__ == "__main__":
    verify_and_log_aws_identity()
    list_my_buckets()