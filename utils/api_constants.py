

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

    def book_order_constant(self):
        url = "https://api.tiki.vn/sandseel/api/v2/public/markets/asaxu/trades"
        params = {'limit': '50'}
        headers = self.headers_constant()
        return url, params, headers

    def stock_price_constant(self):
        url = "https://api.tiki.vn/rally/markets/asaxu/klines"
        params = {
            'period': '5',
            'time_from': '1702667569',
            'time_to': '1702817569'
        }
        headers = self.headers_constant()
        return url, params, headers
