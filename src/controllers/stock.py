from services.stock import StockService
from flask import request, jsonify
from typing import List
import json
from data_layer.redis_connect import RedisConnect


class StockControllers:

    def __init__(self) -> None:
        self.stock_service = StockService()
        self.redis_connect = RedisConnect()

    def dowload_stock_info(self, request) -> dict:
        interval = int(request.get("period", 5))
        page = int(request.get("page", 1))
        limit = int(request.get("limit", 10))
        type_file = str(request.get("type-file"))

        if type_file not in ['json', 'csv']:
            return {"status": "Please choose type-file as json or csv !."}, 400

        file_data = self.stock_service.dowload_stock_by_period(interval,
                                                          type_file,
                                                          limit,
                                                          page)
        return file_data, 200

    def get_stock_price_by_period(self, request) -> dict:

        interval = int(request.get("period", 1))
        page = int(request.get("page", 1))
        limit = int(request.get("limit", 10))
        if page <= 0:
            return {"message": "This page does not exist"}, 404

        result= self.stock_service.get_stock_by_period(interval,
                                                                page,
                                                                limit)
        if page > result["metadata"]["total_pages"]:
            return {"message": "Page {} does not exist".format(page)}, 404
        status_code = 200

        return result, status_code

    def get_book_orders_by_taker_type(self, page, limit, taker_type):

        if page <= 0:
            return {"message": "Page {} does not exist".format(page)}

        book_order_list, book_order_count = self.stock_service.get_book_orders_by_taker_type(page,
                                                                                             limit,
                                                                                             taker_type)
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

    def get_market_trans_by_taker_type(self, page, limit, taker_type):

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
            if market_trans.taker_type == taker_type:
                market_trans_dict_sell = {
                    "price ": market_trans.price,
                    "quantity_astra": market_trans.quantity_astra,
                    "transaction_date": market_trans.transaction_date,
                    "taker_type": market_trans.taker_type,
                }
                market_trans_sell_data.append(market_trans_dict_sell)

        result = {"metadata": metadata,
                  "nearest_price": nearest_price,
                  "book_orders": market_trans_sell_data}
        return result, 200
