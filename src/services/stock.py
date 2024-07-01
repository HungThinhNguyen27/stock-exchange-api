
from data_layer.table.stock import StockPriceDL
from data_layer.table.book_orders import BookOrdersDL
from data_layer.table.market_trans import MarketTransactionDL
from data_layer.table.user import UserData
from flask import request
from utils.stock_utils import StockUtils
from typing import List, Tuple
from model.stock import BookOrders, StockPrice
from data_layer.redis_connect import RedisConnect
import json


class StockService:

    def __init__(self) -> None:
        self.stock_data_layers = StockPriceDL()
        self.user_data_layers = UserData()
        self.stock_utils = StockUtils()
        self.book_orders_dl = BookOrdersDL()
        self.market_trans_dl = MarketTransactionDL()
        self.redis_connect = RedisConnect()

    def dowload_stock_by_period(self, period: int, file_type: str, limit: int, page: int)  -> Tuple[List['StockPrice'], str, int]:

        cache_key = f"stock_data:{period}:{page}:{limit}"
        cached_data = self.redis_connect.get_from_cache(cache_key)
        time_to_live = period*60
        if cached_data:
            file_data = json.loads(cached_data)

        stock_list_period = self.stock_data_layers.get_by_period_and_limit(period,
                                                                            limit,
                                                                            page)
        file_data = self.stock_utils.format_data(stock_list_period)
        self.redis_connect.add_to_cache(cache_key, 
                                        json.dumps(file_data), 
                                        time_to_live)

        return self.stock_utils.download_file(file_type,
                                              file_data,
                                              period)

    def get_stock_by_period(self, period, page: int, limit: int) -> Tuple[List['StockPrice'], str, int]:
        """
        Get stock candles based on pagination parameters.

        Args:
            - page (int): Page number.
            - limit (int): Number of items per page.
        """
        cache_key = f"stock_data:{period}:{page}:{limit}"
        cached_data = self.redis_connect.get_from_cache(cache_key)
        time_to_live = period*60
        if cached_data:
            return json.loads(cached_data)
            
        stock_list = self.stock_data_layers.get_by_period_and_limit(period,
                                                                    limit,
                                                                    page)
        stock_count = self.stock_data_layers.calculate_count(period)

        metadata = {
            "period": period,
            "page_number": page,
            "total_pages": self.stock_utils.calculate_total_pages(stock_count, 
                                                                  limit)
        }
        result = {"stock_candles": self.stock_utils.format_data(stock_list),
                    "metadata": metadata}
        self.redis_connect.add_to_cache(cache_key,
                                        json.dumps(result),
                                        2)

        return result

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

    def get_book_orders_by_taker_type(self, page: int, limit: int, taker_type) -> Tuple[List['BookOrders'], int]:
        """

        """
        offset = (page - 1) * limit
        book_order_list = self.book_orders_dl.sum_total_by_taker_type(taker_type,
                                                                      offset,
                                                                      limit)
        book_order_count = self.book_orders_dl.count_distinct_prices(taker_type
                                                                     )
        return book_order_list, book_order_count

