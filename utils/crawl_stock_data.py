import requests
import json
from utils.api_constants import ApiConstant
from data_layer.table.stock import StockPrice
from datetime import datetime


class CrawlData:

    def __init__(self) -> None:
        self.api_constant = ApiConstant()

    def crawl_stock_price(self):
        data_list = []

        base_url, params_list, headers = self.api_constant.stock_price_constant()

        response = requests.get(base_url, params=params_list,
                                headers=headers)

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
