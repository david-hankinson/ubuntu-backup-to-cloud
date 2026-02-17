import os
import logging
import threading
import disk_utils
from pathlib import Path
from tqdm import tqdm
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig

logger = logging.getLogger(__name__)

class ProgressPercentage(object):
    """
    Callback class to update a progress bar during an S3 upload.
    """
    def __init__(self, filename, size):
        self._filename = filename
        self._size = size
        self._seen_so_far = 0
        self._lock = threading.Lock()
        # Create a progress bar for this specific file
        self.pbar = tqdm(
            total=self._size, 
            unit='B', 
            unit_scale=True, 
            desc=f"Uploading {filename[:20]}...",
            leave=False
        )

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            self.pbar.update(bytes_amount)
            if self._seen_so_far >= self._size:
                self.pbar.close()

def ensure_secure_bucket(s3_client, bucket):
    """Checks if bucket exists; creates it with private policies if not."""
    try:
        s3_client.head_bucket(Bucket=bucket)
        logger.info(f"Bucket '{bucket}' already exists.")
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            # FIX: Get region to avoid IllegalLocationConstraintException
            region = s3_client.meta.region_name
            logger.warning(f"Creating private bucket '{bucket}' in {region}...")
            try:
                if region == 'us-east-1':
                    s3_client.create_bucket(Bucket=bucket)
                else:
                    s3_client.create_bucket(
                        Bucket=bucket,
                        CreateBucketConfiguration={'LocationConstraint': region}
                    )
                
                s3_client.put_public_access_block(
                    Bucket=bucket,
                    PublicAccessBlockConfiguration={
                        'BlockPublicPolicy': True,
                        'RestrictPublicBuckets': True
                    }
                )
                s3_client.put_bucket_acl(Bucket=bucket, ACL='private')
            except ClientError as create_error:
                logger.error(f"Failed to create bucket: {create_error}")
                raise create_error
        else:
            raise e

def backup_to_s3(s3_client, bucket, homepath=None):
    """
    Iterates through the home directory and uploads files to S3.
    """
    if homepath is None:
        homepath = disk_utils.get_home_path()
    
    # Multipart configuration for large files (important for your 41GB!)
    config = TransferConfig(
        multipart_threshold=1024 * 50,  # 50MB
        max_concurrency=10,
        use_threads=True
    )

    home_path_obj = Path(homepath)
    
    for root, dirs, files in os.walk(homepath):
        # Filter out excluded directories to speed up the process
        dirs[:] = [d for d in dirs if d not in disk_utils.EXCLUDE_DIRS and not d.startswith('.')]
        
        for file in files:
            if file.startswith('.'):
                continue
                
            local_path = os.path.join(root, file)
            # Create a relative path for the S3 Key (e.g., Documents/file.txt)
            s3_key = str(Path(local_path).relative_to(home_path_obj))
            file_size = os.path.getsize(local_path)

            try:
                # Initialize progress callback
                progress = ProgressPercentage(s3_key, file_size)
                
                s3_client.upload_file(
                    local_path, 
                    bucket, 
                    s3_key,
                    Config=config,
                    Callback=progress
                )
            except ClientError as e:
                logger.error(f"Failed to upload {s3_key}: {e}")