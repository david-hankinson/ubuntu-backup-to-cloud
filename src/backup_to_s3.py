import logging
from botocore.exceptions import ClientError

# Assuming logger_config.py is imported elsewhere or setup_logging() was called
logger = logging.getLogger(__name__)

def ensure_secure_bucket(s3_client, bucket):
    """
    Checks if bucket exists; creates it with private policies if not.
    Uses the logging format defined in logger_config.py.
    """
    try:
        s3_client.head_bucket(Bucket=bucket)
        logger.info(f"Bucket '{bucket}' already exists.") # Replaced print
    except ClientError as e:
        error_code = e.response['Error']['Code']
        
        if error_code == '404':
            logger.warning(f"Bucket '{bucket}' not found. Creating private bucket...") # Replaced print
            try:
                # Create bucket
                s3_client.create_bucket(Bucket=bucket)
                
                # 1. Block all public access (Best Practice)
                s3_client.put_public_access_block(
                    Bucket=bucket,
                    PublicAccessBlockConfiguration={
                        'BlockPublicAcls': True,
                        'IgnorePublicAcls': True,
                        'BlockPublicPolicy': True,
                        'RestrictPublicBuckets': True
                    }
                )
                
                # 2. Ensure ACL is private
                s3_client.put_bucket_acl(Bucket=bucket, ACL='private')
                logger.info(f"Successfully created and secured bucket: {bucket}")
                
            except ClientError as create_error:
                logger.error(f"Failed to create or secure bucket '{bucket}': {create_error}")
                raise create_error
        else:
            logger.error(f"Unexpected error checking bucket '{bucket}': {e}")
            raise e