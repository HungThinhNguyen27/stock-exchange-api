from utils.write_log import log_record
from utils.crawl_stock_data import CrawlData
from data_layer.model import StockPrice
from data_layer.stock import StockPriceDL
from datetime import datetime, timezone, timedelta

import schedule
import time



print("Script started")

crawl_data = CrawlData()
stock_price_dl = StockPriceDL()

def crawl_stock_price_data():
    try:
        print("Crawling data...")
        data_dict = crawl_data.crawl_stock_price()
        if not data_dict:
            print("No data crawled")
            log_record("No data crawled")
            return
        for record in data_dict:
            print(record)
            stock_entity = StockPrice(
                time_stamp=record.get('time_stamp'),
                open_price=record.get('open_price'),
                close_price=record.get('close_price'),
                high_price=record.get('high_price'),
                low_price=record.get('low_price'),
                volume=record.get('volume'),
            )
            stock_price_dl.add(stock_entity)
            log_record(record)
    except Exception as e:
        print(f"Error during crawl: {e}")

schedule.every(1).minutes.do(crawl_stock_price_data)
if __name__ == '__main__':
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(f"Error in main loop: {e}")