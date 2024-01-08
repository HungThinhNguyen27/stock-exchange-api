import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta


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

    params_list = [
        {"period": 5, "time_from": 1704564195, "time_to": 1704714195},
        {"period": 15, "time_from": 1704264195, "time_to": 1704714195},
        {"period": 30, "time_from": 1703814195, "time_to": 1704714195},
        {"period": 60, "time_from": 1702914195, "time_to": 1704714195},
        {"period": 240, "time_from": 1697514195, "time_to": 1704714195},
        {"period": 1440, "time_from": 1661514195, "time_to": 1704714195},
        {"period": 10080, "time_from": 1402314195, "time_to": 1704714195},
        {"period": 5, "time_from": 1704564256, "time_to": 1704714256},
        {"period": 15, "time_from": 1704264256, "time_to": 1704714256},
        {"period": 30, "time_from": 1703814256, "time_to": 1704714256},
        {"period": 60, "time_from": 1702914256, "time_to": 1704714256},
        {"period": 240, "time_from": 1697514256, "time_to": 1704714256},
        {"period": 1440, "time_from": 1661514256, "time_to": 1704714256},
        {"period": 10080, "time_from": 1402314256, "time_to": 1704714256},
        {"period": 5, "time_from": 1704564479, "time_to": 1704714479},
        {"period": 15, "time_from": 1704264479, "time_to": 1704714479},
        {"period": 30, "time_from": 1703814479, "time_to": 1704714479},
        {"period": 60, "time_from": 1702914479, "time_to": 1704714479},
        {"period": 240, "time_from": 1697514479, "time_to": 1704714479},
        {"period": 1440, "time_from": 1661514479, "time_to": 1704714479},
        {"period": 10080, "time_from": 1402314479, "time_to": 1704714479}
    ]

    def stock_price_constant(self):
        url = "https://api.tiki.vn/rally/markets/asaxu/klines"

        params_list = self.params_list

        headers = self.headers_constant()
        return url, params_list, headers
