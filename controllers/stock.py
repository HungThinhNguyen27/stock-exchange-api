from services.stock import StockService, CrawlDataStockService
from flask import jsonify
from flask import request
from collections import defaultdict
from typing import List


class StockControllers:

    def __init__(self) -> None:
        self.stock_service = StockService()

    def stock_info(self) -> dict:
        stock_list = self.stock_service.get_stock_candles()
        stock_data = []

        for stock in stock_list:
            stock_dict = {
                "close_price": stock.close_price,
                "high_price": stock.high_price,
                "low_price": stock.low_price,
                "open_price": stock.open_price,
                "time_stamp": stock.time_stamp,
                "volume": stock.volume
            }
            stock_data.append(stock_dict)

        result = {"data": stock_data}
        return result, 200

    # def stock_info(self) -> List[dict]:
    #     stock_daily_values = self.stock_service.get_stock_candles()

    #     # result = {
    #     #     'dates': [date.day.strftime('%Y-%m-%d') for date in stock_daily_values],
    #     #     'open_prices': [price.open_price for price in stock_daily_values],
    #     #     'close_prices': [price.close_price for price in stock_daily_values],
    #     #     'high_prices': [price.high_price for price in stock_daily_values],
    #     #     'low_prices': [price.low_price for price in stock_daily_values],
    #     #     'volumes': [volume.volume for volume in stock_daily_values]
    #     # }

    #     return stock_daily_values, 200

    def book_orders_buy_info(self, page, limit):

        book_order_list, book_order_count = self.stock_service.get_book_orders_buy(
            page, limit)
        next_page_url, total_pages = self.stock_service.page_param(book_order_count,
                                                                   page,
                                                                   limit)

        metadata = {
            "page_number": page,
            "current_url": request.url,
            "total_pages": total_pages,
            "next_page_url": next_page_url
        }

        book_order_data = [
            {"price": price,
             "total_asa": total_asa}

            for price, total_asa in book_order_list
        ]

        return book_order_data, metadata, 200

    def book_orders_sell_info(self, page, limit):

        book_order_list, book_order_count = self.stock_service.get_book_orders_sell(
            page, limit)

        next_page_url, total_pages = self.stock_service.page_param(book_order_count,
                                                                   page,
                                                                   limit)

        metadata = {
            "page_number": page,
            "current_url": request.url,
            "total_pages": total_pages,
            "next_page_url": next_page_url
        }

        book_order_data = [
            {"price": price,
             "total_asa": total_asa}

            for price, total_asa in book_order_list
        ]

        return book_order_data, metadata, 200

    def market_trans_info(self):

        market_trans_list = self.stock_service.get_market_trans()
        market_trans_data = []
        for market_trans in market_trans_list:
            market_trans_dict = {
                "quantity_coin": market_trans.quantity_coin,
                "quantity_astra": market_trans.quantity_astra,
                "transaction_date": market_trans.transaction_date
            }
            market_trans_data.append(market_trans_dict)
        return market_trans_data, 200


class CrawlStockController:

    def __init__(self) -> None:
        self.crawl_stock_service = CrawlDataStockService()

    def crawl_stock_price(self):
        self.crawl_stock_service.crawl_stock_price_data()
        return {'message': 'Crawl stock data successful'}, 200
