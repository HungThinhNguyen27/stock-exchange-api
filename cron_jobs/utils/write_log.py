import logging
import os


dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'crawling_log.log')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(filename)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


def log_record(record):
    logger.info("Record: %s", record)