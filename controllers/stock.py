from services.stock import StockService, CrawlDataStockService
from flask import jsonify
from flask import request
from collections import defaultdict
from typing import List


class StockControllers:

    def __init__(self) -> None:
        self.stock_service = StockService()

    def stock_info(self, page, limit) -> dict:

        if page <= 0:
            return {"message": "This page does not exist"}, 400

        stock_list, next_page_url, total_pages = self.stock_service.get_stock_candles(
            page, limit)
        stock_data = []

        if page > total_pages:
            return {"message": "This page does not exist"}, 400

        metadata = {
            "page_number": page,
            "total_pages": total_pages

        }

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

        result = {"stock_candles": stock_data,
                  "metadata": metadata}
        return result, 200

    def book_orders_buy_info(self, page, limit):

        if page <= 0:
            return {"message": "This page does not exist"}, 400

        book_order_list, book_order_count = self.stock_service.get_book_orders_buy(
            page, limit)
        next_page_url, total_pages = self.stock_service.page_param(book_order_count,
                                                                   page,
                                                                   limit)
        if page > total_pages:
            return {"message": "This page does not exist"}, 400

        metadata = {
            "page_number": page,
            "current_url": request.url,
            "total_pages": total_pages,
            "next_page_url": next_page_url
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

        # if page <= 0:
        #     return {"message": "This page does not exist"}, 400

        book_order_list, book_order_count = self.stock_service.get_book_orders_sell(
            page, limit)

        next_page_url, total_pages = self.stock_service.page_param(book_order_count,
                                                                   page,
                                                                   limit)
        # if page > total_pages:
        #     return {"message": "This page does not exist"}, 400

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

    def market_trans_info(self, page, limit):

        if page <= 0:
            return {"message": "This page does not exist"}, 400

        market_trans_list, next_page_url, total_pages = self.stock_service.get_market_transaction(
            page, limit)
        # print("market_trans_list type", type(market_trans_list))
        market_trans_buy_data = []
        market_trans_sell_data = []

        if page > total_pages:
            return {"message": "This page does not exist"}, 400

        metadata = {
            "page_number": page,
            "total_page": total_pages,
        }

        print(market_trans_list)

        for market_trans in market_trans_list:
            if market_trans.taker_type == "bought":
                market_trans_dict_buy = {
                    "purchased_transaction": {
                        "price": market_trans.price,
                        "quantity_astra": market_trans.quantity_astra,
                        "transaction_date": market_trans.transaction_date,
                        "Taker_type": market_trans.taker_type,
                    }}
                market_trans_buy_data.append(market_trans_dict_buy)
            else:
                market_trans_dict_sell = {
                    "sold_Transaction": {
                        "price ": market_trans.price,
                        "quantity_astra": market_trans.quantity_astra,
                        "transaction_date": market_trans.transaction_date,
                        "Taker_type": market_trans.taker_type,
                    }}
                market_trans_sell_data.append(market_trans_dict_sell)

        result = {"metadata": metadata,
                  "book_order_bought": market_trans_buy_data,
                  "book_order_sold": market_trans_sell_data, }
        return result, 200


class CrawlStockController:

    def __init__(self) -> None:
        self.crawl_stock_service = CrawlDataStockService()

    def crawl_stock_price(self):
        self.crawl_stock_service.crawl_stock_price_data()
        return {'message': 'Crawl stock data successful'}, 200
