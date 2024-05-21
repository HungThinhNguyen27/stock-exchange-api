import logging
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'test_log.log')

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(filename)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)


def crawl_data():
    print("Crawling data...")


def do_logging():
    logger.info("Crawling data started")
    crawl_data()
    logger.info("Crawling data finished")


if __name__ == '__main__':
    do_logging()


#  * * * * * cd /Users/macos/Projects/ && /opt/homebrew/bin/python3.11 /Users/macos/Projects/cron_jobs/crawl_data.py >> /Users/macos/Projects/cron_jobs/crawl_log.log 2>&1
#  * * * * * /opt/homebrew/bin/python3.11 /Users/macos/Projects/cron_jobs/crawl_data.py >> /Users/macos/Projects/cron_jobs/crawl_log.log 2>&1
