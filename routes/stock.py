from flask import Flask, Blueprint, jsonify, request
from controllers.stock import StockControllers


class StockRoutes:

    def __init__(self) -> None:
        self.stock_controllers = StockControllers()
        self.blueprint = Blueprint('stock', __name__)
        self.blueprint.add_url_rule("/stock-candles", 'get_stock_info',
                                    self.get_stock_info, methods=["GET"])
        self.blueprint.add_url_rule("/book-orders", 'get_book_orders',
                                    self.get_book_orders, methods=["GET"])
        self.blueprint.add_url_rule("/market_trans", 'get_market_trans',
                                    self.get_market_trans, methods=["GET"])

    def get_stock_info(self):
        resonponse, status_code = self.stock_controllers.stock_info()
        return jsonify(resonponse), status_code

    def get_book_orders(self):
        resonponse, status_code = self.stock_controllers.book_orders_info()
        return jsonify(resonponse), status_code

    def get_market_trans(self):
        resonponse, status_code = self.stock_controllers.market_trans_info()
        return jsonify(resonponse), status_code
