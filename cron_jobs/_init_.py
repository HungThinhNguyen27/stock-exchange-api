from utils.write_log import log_record
from utils.crawl_stock_data import CrawlData


from src.model.stock import StockPrice
from datetime import datetime, timezone, timedelta
from src.utils.telegram_bot import send_error_to_telegram
import schedule
import time



print("Script started")

crawl_data = CrawlData()

def crawl_stock_price_data():
    try:
        print("Crawling data...")
        data_dict = crawl_data.crawl_stock_price()
        if not data_dict:
            text = "No data crawled"
            print(text)
            log_record(text)
            send_error_to_telegram(str(e))
            return
        for record in data_dict:
            print(record)
            time_stamp = record.get('time_stamp')
            open_price = record.get('open_price')
            close_price =record.get('close_price')
            high_price = record.get('high_price')
            low_price = record.get('low_price')
            volume = record.get('volume')           
            crawl_data.add_record_to_database(time_stamp,
                                              open_price,
                                              close_price,
                                              high_price,
                                              low_price,
                                              volume)
            log_record(record)
    except Exception as e:
        send_error_to_telegram(str(e))
        print(f"Error during crawl: {e}")

schedule.every(1).minutes.do(crawl_stock_price_data)
if __name__ == '__main__':
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(f"Error in main loop: {e}")
            send_error_to_telegram(str(e))