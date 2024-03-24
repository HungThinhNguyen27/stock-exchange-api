
from data_layer.table.stock import StockPriceDL
from data_layer.table.book_orders import BookOrdersDL
from data_layer.table.market_trans import MarketTransactionDL
from utils.crawl_stock_data import CrawlData
from data_layer.table.user import UserData
from flask import request
from utils.stock_utils import StockUtils
from typing import List, Tuple
from model.stock import BookOrders, StockPrice
import schedule
import time
import schedule
import json
import os
import datetime


class StockService:

    def __init__(self) -> None:
        self.stock_data_layers = StockPriceDL()
        self.user_data_layers = UserData()
        self.stock_utils = StockUtils()
        self.book_orders_dl = BookOrdersDL()
        self.market_trans_dl = MarketTransactionDL()

    def get_stock_candles(self, page: int, limit: int, type) -> Tuple[List['StockPrice'], str, int]:
        """
        Get stock candles based on pagination parameters.

        Args:
            - page (int): Page number.
            - limit (int): Number of items per page.
        """

        offset = (page - 1) * limit
        stock_list = self.stock_data_layers.get_stock_data(limit, offset, type)
        stock_count = self.stock_data_layers.count_stock_data(type)
        next_page_url, total_pages = self.stock_utils.page_param(stock_count,
                                                                 page,
                                                                 limit)

        return stock_list, next_page_url, total_pages

    def get_market_transaction(self, page, limit):
        offset = (page - 1) * limit
        market_trans = self.market_trans_dl.get(limit,
                                                offset)
        market_trans_count = self.market_trans_dl.count()
        next_page_url, total_pages = self.stock_utils.page_param(market_trans_count,
                                                                 page,
                                                                 limit)
        nearest_price = self.market_trans_dl.get_nearest_price()

        return market_trans, next_page_url, total_pages, nearest_price

    def get_book_orders_buy(self, page: int, limit: int) -> Tuple[List['BookOrders'], int]:
        """

        """
        offset = (page - 1) * limit
        taker_type = 'buy'
        book_order_list = self.book_orders_dl.sum_total_by_taker_type(taker_type,
                                                                      offset,
                                                                      limit)
        book_order_count = self.book_orders_dl.count_distinct_prices(taker_type
                                                                     )
        return book_order_list, book_order_count

    def get_book_orders_sell(self, page: int, limit: int) -> Tuple[List['BookOrders'], int]:
        """

        """
        offset = (page - 1) * limit
        taker_type = 'sell'
        book_order_list = self.book_orders_dl.sum_total_by_taker_type(taker_type,
                                                                      offset,
                                                                      limit)
        book_order_count = self.book_orders_dl.count_distinct_prices(
            taker_type)
        return book_order_list, book_order_count

    def page_param(self, price_list_count, page, limit):
        next_page_url, total_pages = self.stock_utils.page_param(
            price_list_count, page, limit)
        return next_page_url, total_pages


class CrawlDataStockService:

    def __init__(self) -> None:
        self.stock_data_layers = StockPriceDL()
        self.crawl_data = CrawlData()

    def crawl_stock_price_data(self, type):
        data_dict = self.crawl_data.crawl_stock_price()
        for record in data_dict:
            stock_entity = StockPrice(
                time_stamp=record.get('time_stamp'),
                open_price=record.get('open_price'),
                close_price=record.get('close_price'),
                high_price=record.get('high_price'),
                low_price=record.get('low_price'),
                volume=record.get('volume'),
                type=type
            )
            self.stock_data_layers.add(stock_entity)
            print(record)

    def run_everyday(self) -> None:
        schedule.every().day.at("15:51").do(self.crawl_stock_price_data)
        allow_crawling = True
        start_time = time.time()
        while allow_crawling:
            schedule.run_pending()
            elapsed_time = time.time() - start_time
            if elapsed_time == 30:
                break


# a = CrawlDataStockService()
# type = "5m"
# b = a.crawl_stock_price_data(type)
