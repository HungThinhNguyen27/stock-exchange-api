from flask import Blueprint, jsonify, request, send_from_directory, send_file
from controllers.stock import StockControllers
from data_layer.redis_connect import RedisConnect
import json


class Stock:

    def __init__(self) -> None:
        super().__init__()
        self.stock_controllers = StockControllers()
        self.redis_connect = RedisConnect()

        self.blueprint = Blueprint('stock', __name__)

        self.blueprint.add_url_rule("/stock-candles", 'get_stock_info',
                                    self.get_stock_info, methods=["GET"])

        self.blueprint.add_url_rule("/download-stock-candles", 'dowload_file_stock_price',
                                    self.dowload_file_stock_price, methods=["GET"])

        self.blueprint.add_url_rule("/book-orders", 'get_book_orders',
                                    self.get_book_orders, methods=["GET"])

        self.blueprint.add_url_rule("/market_trans", 'get_market_trans',
                                    self.get_market_trans, methods=["GET"])

    def dowload_file_stock_price(self):
        request_args = request.args
        resonponse, status_code = self.stock_controllers.dowload_stock_info(request_args
                                                                            )
        return jsonify(resonponse), status_code

    def get_stock_info(self):
        request_args = request.args
        resonponse, status_code = self.stock_controllers.get_stock_price_by_period(request_args
                                                                                   )
        return jsonify(resonponse), status_code

    def get_book_orders(self):
        taker_type = str(request.args.get("taker_type"))
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        resonponse, status_code = self.stock_controllers.get_book_orders_by_taker_type(page,
                                                                                       limit,
                                                                                       taker_type)
        return jsonify(resonponse), status_code

    def get_market_trans(self):
        taker_type = str(request.args.get("taker_type"))
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        resonponse, status_code = self.stock_controllers.get_market_trans_by_taker_type(page,
                                                                                        limit,
                                                                                        taker_type)
        return jsonify(resonponse), status_code
