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


class StockService:

    def __init__(self) -> None:
        self.stock_data_layers = Stock()
        self.user_data_layers = UserData()
        self.stock_utils = StockUtils()

    def get_stock_candles(self):
        """

        """
        stock_list = self.stock_data_layers.get_stock_data()
        df = pd.DataFrame([(stock.time_stamp, stock.open_price, stock.close_price, stock.high_price, stock.low_price, stock.volume) for stock in stock_list],
                          columns=['time_stamp', 'open_price', 'close_price', 'high_price', 'low_price', 'volume'])
        df['time_stamp'] = pd.to_datetime(df['time_stamp'])

        # Determine official opening and closing hours
        official_open_time = datetime.strptime('09:30', '%H:%M').time()
        official_close_time = datetime.strptime('16:00', '%H:%M').time()

        df = df[(df['time_stamp'].dt.time >= official_open_time) &
                (df['time_stamp'].dt.time <= official_close_time)]

        grouped_data = df.groupby(df['time_stamp'].dt.date).agg({
            'open_price': 'mean',
            'close_price': 'mean',
            'high_price': 'mean',
            'low_price': 'mean',
            'volume': 'sum'
        }).reset_index()

        return grouped_data

    def get_book_orders_buy(self, page, limit):
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

    def get_book_orders_sell(self, page, limit):
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

    def get_market_trans(self):
        return self.stock_data_layers.get_market_transaction_data()


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
