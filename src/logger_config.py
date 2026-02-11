import logging
import sys
from logging.handlers import TimedRotatingFileHandler

def setup_logging(log_filename='ubuntu-backup-to-s3.log'):
    # 1. The Format
    log_format = logging.Formatter(
        '%(asctime)s [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s'
    )

    # 2. The File Handler (Daily Rotation)
    file_handler = TimedRotatingFileHandler(
        log_filename, when="midnight", interval=1, backupCount=7
    )
    file_handler.setFormatter(log_format)

    # 3. The Console Handler (So you see logs in your terminal too)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)

    # 4. Root Logger Setup
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Avoid adding handlers multiple times if setup is called twice
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger