from model.stock import StockPrice
from utils.crawl_stock_data import CrawlData
from data_layer.table.stock import StockPriceDL
import logging
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'crawling_log.log')

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(filename)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

crawl_data = CrawlData()
stock_price_dl = StockPriceDL()


def crawl_stock_price_data():
    data_dict = crawl_data.crawl_stock_price()
    for record in data_dict:
        stock_entity = StockPrice(
            time_stamp=record.get('time_stamp'),
            open_price=record.get('open_price'),
            close_price=record.get('close_price'),
            high_price=record.get('high_price'),
            low_price=record.get('low_price'),
            volume=record.get('volume'),
        )
        stock_price_dl.add(stock_entity)
        logger.info("Record: %s", record)
        # print(record)


if __name__ == '__main__':
    crawl_stock_price_data()

# PYTHONPATH=/Users/macos/Projects:/Users/macos/Projects/data_layer:/Users/macos/Projects/model:/Users/macos/Projects/utils:/Users/macos/Projects/config.yaml
# * * * * * /opt/homebrew/bin/python3.11 /Users/macos/Projects/cron_jobs/crawl_data.py >> /Users/macos/Projects/cron_jobs/crawl_log.log 2>&1
# * * * * * /opt/homebrew/bin/python3.11 /Users/macos/Projects/cron_jobs/crawl_data.py
