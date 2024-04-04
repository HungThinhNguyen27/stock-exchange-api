from collections import defaultdict
from flask import request
import math


class StockUtils:

    def pagination(self, page_param):
        per_page = 10
        offset = (page_param - 1) * per_page
        return per_page, offset

    def group_and_sum_book_orders_buy(self, book_order_list):
        price_asa_map = defaultdict(float)
        for book_order in book_order_list:
            price = book_order.price
            total = book_order.total
            taker_type = book_order.taker_type

            if taker_type == 'buy':
                price_asa_map[price] += total
        return price_asa_map

    def group_and_sum_book_orders_sell(self, book_order_list):
        price_asa_map = defaultdict(float)
        for book_order in book_order_list:
            price = book_order.price
            total = book_order.total
            taker_type = book_order.taker_type

            if taker_type == 'sell':
                price_asa_map[price] += total
        return price_asa_map

    def page_param(self, count_result, page, limit):

        total_pages = (count_result + limit - 1) // limit
        next_page_url = None
        if page < total_pages:
            next_page_url = (
                f"{request.base_url}?page={page + 1}&limit={limit}"
            )
        return next_page_url, total_pages

    def format_data(self, records):
        stock_data = []
        for record in records:
            # Explicitly converting minutes to an integer
            minutes = int(float(record[2]))
            datetime_string = f"{record[0].strftime('%Y-%m-%d')} {str(record[1]).zfill(2)}:{str(minutes).zfill(2)}"
            stock_dict = {
                "time_stamp": datetime_string,
                "open_price": record[3],
                "close_price": record[4],
                "high_price": record[5],
                "low_price": record[6],
                "volume": int(record[7])
            }
            stock_data.append(stock_dict)
        return stock_data
