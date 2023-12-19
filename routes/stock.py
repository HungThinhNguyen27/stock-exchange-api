from flask import Flask, Blueprint, jsonify, request
from controllers.stock import StockControllers, CrawlStockController


class StockRoutes:

    def __init__(self) -> None:
        self.stock_controllers = StockControllers()
        self.crawl_stock_controllers = CrawlStockController()

        self.blueprint = Blueprint('stock', __name__)
        self.blueprint.add_url_rule("/stock-candles", 'get_stock_info',
                                    self.get_stock_info, methods=["GET"])
        self.blueprint.add_url_rule("/book-orders", 'get_book_orders',
                                    self.get_book_orders, methods=["GET"])
        self.blueprint.add_url_rule("/market_trans", 'get_market_trans',
                                    self.get_market_trans, methods=["GET"])
        self.blueprint.add_url_rule("/crawl_book_orders_data", 'crawl_book_orders_data',
                                    self.crawl_book_orders_data, methods=["POST"])
        self.blueprint.add_url_rule("/crawl_stock_price_data", 'crawl_stock_price_data',
                                    self.crawl_stock_price_data, methods=["POST"])

    def get_stock_info(self):
        resonponse, status_code = self.stock_controllers.stock_info()
        return jsonify(resonponse), status_code

    def get_book_orders(self):
        resonponse, status_code = self.stock_controllers.book_orders_info()
        return jsonify(resonponse), status_code

    def get_market_trans(self):
        resonponse, status_code = self.stock_controllers.market_trans_info()
        return jsonify(resonponse), status_code

    def crawl_book_orders_data(self):
        resonponse, status_code = self.crawl_stock_controllers.crawl_book_orders()
        return jsonify(resonponse), status_code

    def crawl_stock_price_data(self):
        resonponse, status_code = self.crawl_stock_controllers.crawl_stock_price()
        return jsonify(resonponse), status_code

    def buy_stock_now(self):
        request_data = request.get_json()
        respone_data, status_code = self.user_controllers.buy_stock_now(
            request_data)
        return jsonify(respone_data), status_code

    def buy_stock_limit(self):
        request_data = request.get_json()
        respone_data, status_code = self.user_controllers.buy_stock_limit(
            request_data)
        return jsonify(respone_data), status_code
