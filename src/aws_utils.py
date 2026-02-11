import boto3
import logging

logger = logging.getLogger(__name__)

def verify_and_log_aws_identity():
    sts = boto3.client('sts')
    try:
        identity = sts.get_caller_identity()
        account_id = identity['Account']
        arn = identity['Arn']

        masked_account = f"{'*' * 8}{account_id[-4:]}"
        parts = arn.split(':')
        if len(parts) > 4:
            parts[4] = masked_account
        
        masked_arn = ":".join(parts)

        logging.info(f"Identity Verified | Account: {masked_account} | ARN: {masked_arn}")
        print(f"Proceeding on account ID: {masked_account}")
        print(f"Using ARN: {masked_arn}")
        return True
    except Exception as e:
        logging.error(f"Failed to verify AWS identity: {e}")
        print(f"Error: {e}")
        return False

def list_my_buckets():
    s3 = boto3.client('s3')
    logging.info("Starting S3 bucket list request...")
    try:
        response = s3.list_buckets()
        print("\n--- Your S3 Buckets ---")
        for bucket in response['Buckets']:
            name = bucket['Name']
            print(f"Bucket Name: {name}")
            logging.info(f"Found bucket: {name}")
    except Exception as e:
        logging.error(f"Error connecting to AWS: {e}")
        print(f"Error connecting to AWS: {e}")