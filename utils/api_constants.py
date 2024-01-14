
from datetime import datetime, timezone


class ApiConstant:

    def headers_constant(self):
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
        return headers

    start_date = datetime(2023, 11, 1, tzinfo=timezone.utc)
    start_timestamp = int(start_date.timestamp())

    current_date = datetime.utcnow()
    current_timestamp = int(current_date.timestamp())
    period = 1440

    params_list = {
        'period': period,
        'time_from': start_timestamp,
        'time_to': current_timestamp
    }

    def stock_price_constant(self):
        url = "https://api.tiki.vn/rally/markets/asaxu/klines"

        headers = self.headers_constant()
        return url, self.params_list, headers
