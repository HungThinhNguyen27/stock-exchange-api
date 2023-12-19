import requests
import json
from utils.api_constants import ApiConstant
from data_layer.stock import Stock
from datetime import datetime


class CrawlData:

    def __init__(self) -> None:
        self.api_constant = ApiConstant()
        self.stock_data_layer = Stock()

    def change_timestamp(self, time):
        created_at = datetime.utcfromtimestamp(
            time).strftime('%Y-%m-%d %H:%M:%S')
        return created_at

    def check_book_order_id_dup(self, input_id):
        book_order_list = self.stock_data_layer.get_book_orders_data()
        for book_order in book_order_list:
            if book_order.book_order_id == input_id:
                return book_order
        return None

    def crawl_book_order(self):
        data_list = []
        base_url, params, headers = self.api_constant.book_order_constant()

        response = requests.get(
            base_url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            data_list.extend(data)
            for record in data:
                print(f"Record: {record}")

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

    def crawl_stock_price(self):
        data_list = []
        base_url, params, headers = self.api_constant.stock_price_constant()
        response = requests.get(base_url, params=params, headers=headers)

        if response.status_code == 200:
            data = response.json()
            data_list.extend(data)
            for record in data:
                print(f"Record: {record}")

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
        return formatted_data


# a = CrawlData()

# output = a.crawl_stock_price()
# print(output)
