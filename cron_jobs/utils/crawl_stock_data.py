
from datetime import datetime, timezone, timedelta
import requests
import pytz
from src.data_layer.table.stock import StockPriceDL
from src.utils.telegram_bot import send_error_to_telegram
import traceback


class CrawlData:
    def __init__(self) -> None:
        self.StockPriceDL = StockPriceDL()

    def latest_stock_record(self):
        record = self.StockPriceDL.get_one_latest_record()
        return record.time_stamp
    
    def add_record_to_database(self, time_stamp, open_price, close_price, high_price, low_price, volume): 
        
        self.StockPriceDL.add(time_stamp, 
                              open_price, 
                              close_price, 
                              high_price, 
                              low_price, 
                              volume)

    def api_constant(self):

        period = "1"
        utc_now = datetime.now(pytz.utc)
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        current_date = utc_now.astimezone(vietnam_tz)
        current_timestamp = int(current_date.timestamp())
        print("current_date", current_date)




        latest_date = self.latest_stock_record()
        start_date = latest_date + timedelta(minutes=1)
        start_timestamp = int(start_date.timestamp())

        print("start_date", start_date)

        # start_date = datetime(2024, 5, 1, 0, 0, 0)
        # start_date_vietnam = vietnam_tz.localize(start_date)
        # start_timestamp = int(start_date_vietnam.timestamp())

        url = "https://api.tiki.vn/rally/markets/asaxu/klines"

        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7',
            'Cache-Control': 'no-cache',
            'Origin': 'https://exchange.tiki.vn',
            'Pragma': 'no-cache',
            'Referer': 'https://exchange.tiki.vn/',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"macOS"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        params_list = {
            'period': period,
            'time_from': start_timestamp,
            'time_to': current_timestamp
        }
        return url, params_list, headers

    def convert_timestamp_to_vietnam(self, data_list):
        vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')

        for record in data_list:
            normal_time = datetime.utcfromtimestamp(record['time_stamp'])
            vietnam_time = normal_time.replace(
                tzinfo=pytz.utc).astimezone(vietnam_timezone)
            record['time_stamp'] = vietnam_time.strftime('%Y-%m-%d %H:%M')
        return data_list

    def crawl_stock_price(self):
        formatted_data = []  
        try: 
            data_list = []
            base_url, params_list, headers = self.api_constant()
            response = requests.get(base_url, params=params_list,
                                    headers=headers)

            if response.status_code == 200:
                data = response.json()
                data_list.extend(data)
            else: 
                text = " Sending request to tiki exchange failed!"
                print(text)
                send_error_to_telegram(str(text))
            formatted_data = [
                {
                    'time_stamp': record[0],
                    'open_price': record[1],
                    'close_price': record[4],
                    'high_price': record[2],
                    'low_price': record[3],
                    'volume': record[5]
                }
                for record in data_list
            ]
        except Exception as e:
            error_message = f"Error during crawl in utils folder: {e}\n\nTraceback:\n{traceback.format_exc()}"
            print(error_message)            
            send_error_to_telegram(str(e))
        return self.convert_timestamp_to_vietnam(formatted_data)
