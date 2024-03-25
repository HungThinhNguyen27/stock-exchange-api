from services.stock import StockService, CrawlDataStockService
from flask import jsonify
from flask import request
from typing import List
import json
from data_layer.redis_connect import RedisConnect


class StockControllers:

    def __init__(self) -> None:
        self.stock_service = StockService()
        self.redis_connect = RedisConnect()

    def stock_info(self, page, limit, type) -> dict:

        if page <= 0:
            return {"message": "This page does not exist"}, 404

        stock_list, next_page_url, total_pages = self.stock_service.get_stock_candles(page,
                                                                                      limit,
                                                                                      type)
        stock_data = []

        if page > total_pages:
            return {"message": "This page does not exist"}, 404

        metadata = {
            "page_number": page,
            "total_pages": total_pages

        }

        for stock in stock_list:
            if type == "1D":
                time = stock.time_stamp.strftime("%Y-%m-%d")
            else:
                time = stock.time_stamp.strftime("%Y-%m-%d %H:%M")
            stock_dict = {
                "close_price": stock.close_price,
                "high_price": stock.high_price,
                "low_price": stock.low_price,
                "open_price": stock.open_price,
                "time_stamp": time,
                "volume": stock.volume
            }
            stock_data.append(stock_dict)

        result = {"stock_candles": stock_data,
                  "metadata": metadata}

        return result, 200

    def book_orders_buy_info(self, page, limit):

        if page <= 0:
            return {"message": "This page does not exist"}, 404

        book_order_list, book_order_count = self.stock_service.get_book_orders_buy(page,
                                                                                   limit)
        next_page_url, total_pages = self.stock_service.page_param(book_order_count,
                                                                   page,
                                                                   limit)
        if page > total_pages:
            return {"message": "This page does not exist"}, 404

        metadata = {
            "page_number": page,
            "total_pages": total_pages,
        }

        book_order_data = [
            {"price": price,
             "total_asa": int(total_asa)}

            for price, total_asa in book_order_list
        ]
        result = {"metadata": metadata,
                  "book_order_data": book_order_data}
        return result, 200

    def book_orders_sell_info(self, page, limit):

        if page <= 0:
            return {"message": "This page does not exist"}, 404

        book_order_list, book_order_count = self.stock_service.get_book_orders_sell(
            page, limit)

        next_page_url, total_pages = self.stock_service.page_param(book_order_count,
                                                                   page,
                                                                   limit)
        if page > total_pages:
            return {"message": "This page does not exist"}, 404

        metadata = {
            "page_number": page,
            "total_pages": total_pages
        }

        book_order_data = [
            {"price": price,
             "total_asa": int(total_asa)}

            for price, total_asa in book_order_list
        ]
        result = {"metadata": metadata,
                  "book_order_data": book_order_data}
        return result, 200

    def market_trans_sold_info(self, page, limit):

        if page <= 0:
            return {"message": "This page does not exist"}, 404

        market_trans_list, next_page_url, total_pages, nearest_price = self.stock_service.get_market_transaction(page,
                                                                                                                 limit)
        market_trans_sell_data = []

        if page > total_pages:
            return {"message": "This page does not exist"}, 404

        metadata = {
            "page_number": page,
            "total_page": total_pages,
        }

        for market_trans in market_trans_list:
            if market_trans.taker_type == "sold":
                market_trans_dict_sell = {
                    "price ": market_trans.price,
                    "quantity_astra": market_trans.quantity_astra,
                    "transaction_date": market_trans.transaction_date,
                    "Taker_type": market_trans.taker_type,
                }
                market_trans_sell_data.append(market_trans_dict_sell)

        result = {"metadata": metadata,
                  "nearest_price": nearest_price,
                  "book_order_sold": market_trans_sell_data}
        return result, 200

    def market_trans_bought_info(self, page, limit):

        if page <= 0:
            return {"message": "This page does not exist"}, 404

        market_trans_list, next_page_url, total_pages, nearest_price = self.stock_service.get_market_transaction(page,
                                                                                                                 limit)
        market_trans_buy_data = []

        if page > total_pages:
            return {"message": "This page does not exist"}, 404

        metadata = {
            "page_number": page,
            "total_page": total_pages,
        }

        for market_trans in market_trans_list:
            if market_trans.taker_type == "bought":
                market_trans_dict_buy = {
                    "price": market_trans.price,
                    "quantity_astra": market_trans.quantity_astra,
                    "transaction_date": market_trans.transaction_date,
                    "Taker_type": market_trans.taker_type,
                }
                market_trans_buy_data.append(market_trans_dict_buy)

        result = {"metadata": metadata,
                  "nearest_price": nearest_price,
                  "book_order_bought": market_trans_buy_data}
        return result, 200


class CrawlStockController:

    def __init__(self) -> None:
        self.crawl_stock_service = CrawlDataStockService()

    def crawl_stock_price(self):
        self.crawl_stock_service.crawl_stock_price_data()
        return {'message': 'Crawl stock data successful'}, 200
