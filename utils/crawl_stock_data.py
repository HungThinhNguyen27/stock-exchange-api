
from datetime import datetime, timezone, timedelta
import requests


class CrawlData:

    def api_constant(self):

        # period = 10080
        period = 10_080
        start_date = datetime(2023, 11, 1, tzinfo=timezone.utc)
        start_timestamp = int(start_date.timestamp())
        url = "https://api.tiki.vn/rally/markets/asaxu/klines"
        current_date = datetime.utcnow()
        current_timestamp = int(current_date.timestamp())

        # start_date = current_date - timedelta(days=1)
        # start_timestamp = int(start_date.timestamp())

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

    def convert_timestamp(self, data_list):
        for record in data_list:
            normal_time = datetime.utcfromtimestamp(
                record['time_stamp']).strftime('%Y-%m-%d %H:%M')
            record['time_stamp'] = normal_time
        return data_list

    def crawl_stock_price(self):
        data_list = []
        base_url, params_list, headers = self.api_constant()
        response = requests.get(base_url, params=params_list,
                                headers=headers)

        if response.status_code == 200:
            data = response.json()
            data_list.extend(data)

        formatted_data = [
            {
                'time_stamp': record[0],
                'open_price': record[1],
                'close_price': record[4],
                'high_price': record[2],
                'low_price': record[3],
                'volume': record[5],
            }
            for record in data_list
        ]
        return self.convert_timestamp(formatted_data)


# a = CrawlData()
# b = a.crawl_stock_price()
# print(b)
