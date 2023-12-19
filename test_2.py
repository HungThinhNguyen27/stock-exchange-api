import requests
import json


def crawl_book_order(base_url, params, headers):
    page = 1
    data_list = []
    max_records = 2000
    while len(data_list) < max_records:
        current_params = params.copy()
        current_params['page'] = page
        response = requests.get(
            base_url, params=current_params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if not data:
                break
            data_list.extend(data)
            print(f"Page {page} - Fetched {len(data)} records")
            for record in data:
                print(f"Record: {record}")
            page += 1
        else:
            print(
                f"Failed to fetch data from page {page}, Status code: {response.status_code}")
            break

    # Chọn tối đa max_records bản ghi
    data_list = data_list[:max_records]

    formatted_data = [
        {
            'id': record.get('id'),
            'price': record.get('price'),
            'amount': record.get('amount'),
            'total': record.get('total'),
            'market': record.get('market'),
            'created_at': record.get('created_at'),
            'taker_type': record.get('taker_type')
        }
        for record in data_list
    ]

    return formatted_data


# Example usage
url = "https://api.tiki.vn/sandseel/api/v2/public/markets/asaxu/trades"
params = {'limit': '50'}
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

crawl_book_order(url, params, headers)
