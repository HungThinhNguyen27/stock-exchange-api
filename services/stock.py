import pandas as pd
from datetime import datetime
from data_layer.stock import Stock
from utils.crawl_stock_data import CrawlData
from model.stock import BookOrders, StockPrice
from data_layer.user import UserData
from flask import request
from datetime import datetime
from collections import defaultdict
from utils.stock_utils import StockUtils
from typing import List, Tuple


class StockService:

    def __init__(self) -> None:
        self.stock_data_layers = Stock()
        self.user_data_layers = UserData()
        self.stock_utils = StockUtils()

    def get_stock_candles(self, page: int, limit: int) -> Tuple[List['StockPrice'], str, int]:
        """
        Get stock candles based on pagination parameters.

        Args:
            - page (int): Page number.
            - limit (int): Number of items per page.
        """

        offset = (page - 1) * limit
        stock_list = self.stock_data_layers.get_stock_data(limit, offset)
        stock_count = self.stock_data_layers.count_stock_data()
        next_page_url, total_pages = self.page_param(
            stock_count, page, limit)

        return stock_list, next_page_url, total_pages

    def get_book_orders_buy(self, page: int, limit: int) -> Tuple[List['BookOrders'], int]:
        """

        """
        offset = (page - 1) * limit
        taker_type = 'buy'
        book_order_list = self.stock_data_layers.sum_total_by_taker_type(taker_type,
                                                                         offset,
                                                                         limit)
        book_order_count = self.stock_data_layers.count_distinct_prices(
            taker_type)
        return book_order_list, book_order_count

    def get_book_orders_sell(self, page: int, limit: int) -> Tuple[List['BookOrders'], int]:
        """

        """
        offset = (page - 1) * limit
        taker_type = 'sell'
        book_order_list = self.stock_data_layers.sum_total_by_taker_type(taker_type,
                                                                         offset,
                                                                         limit)
        book_order_count = self.stock_data_layers.count_distinct_prices(
            taker_type)
        return book_order_list, book_order_count

    def page_param(self, price_list_count, page, limit):
        next_page_url, total_pages = self.stock_utils.page_param(
            price_list_count, page, limit)
        return next_page_url, total_pages

    def get_market_trans(self, page, limit):
        offset = (page - 1) * limit
        market_transactions = self.stock_data_layers.get_market_transaction(
            limit, offset)

        total_count = self.stock_data_layers.count_market_transactions()
        next_page_url, total_pages = self.page_param(
            total_count, page, limit)

        return market_transactions, next_page_url, total_pages


class CrawlDataStockService:

    def __init__(self) -> None:
        self.stock = Stock()
        self.crawl_data = CrawlData()

    def crawl_stock_price_data(self):
        stock_price_data_list = self.crawl_data.crawl_stock_price()

        for stock_price_data in stock_price_data_list:
            created_at = self.crawl_data.change_timestamp(
                stock_price_data.get('time_stamp'))

            stock_entity = StockPrice(
                time_stamp=created_at,
                open_price=stock_price_data.get('open_price'),
                close_price=stock_price_data.get('close_price'),
                high_price=stock_price_data.get('high_price'),
                low_price=stock_price_data.get('low_price'),
                volume=stock_price_data.get('volume')
            )
            self.stock.add(stock_entity)
