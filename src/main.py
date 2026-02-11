#!/usr/bin/env python3
import logger_config
from aws_utils import verify_and_log_aws_identity, list_my_buckets

def main():
    # Initialize the logger
    logger_config.setup_logging()
    
    # Run the identity check
    if verify_and_log_aws_identity():
        # Only list buckets if identity is verified
        list_my_buckets()

if __name__ == "__main__":
    main()