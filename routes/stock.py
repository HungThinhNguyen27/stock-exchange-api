from flask import Flask, Blueprint, jsonify, request
from controllers.stock import StockControllers, CrawlStockController
from middlewares.authentication import JwtAuthentication


class StockRoutes:

    def __init__(self) -> None:
        self.stock_controllers = StockControllers()
        self.crawl_stock_controllers = CrawlStockController()

        self.blueprint = Blueprint('stock', __name__)
        self.blueprint.add_url_rule("/stock-candles/<string:type>", 'get_stock_info',
                                    self.get_stock_info, methods=["GET"])

        self.blueprint.add_url_rule("/book-orders-buy", 'get_book_orders_buy',
                                    self.get_book_orders_buy, methods=["GET"])

        self.blueprint.add_url_rule("/book-orders-sell", 'get_book_orders_sell',
                                    self.get_book_orders_sell, methods=["GET"])

        self.blueprint.add_url_rule("/market_trans_bought", 'get_market_trans_bought',
                                    self.get_market_trans_bought, methods=["GET"])

        self.blueprint.add_url_rule("/market_trans_sold", 'get_market_trans_sold',
                                    self.get_market_trans_sold, methods=["GET"])

        self.blueprint.add_url_rule("/crawl_stock_price_data", 'crawl_stock_price_data',
                                    self.crawl_stock_price_data, methods=["POST"])

    def get_stock_info(self, type):
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        resonponse, status_code = self.stock_controllers.stock_info(
            page, limit, type)
        return jsonify(resonponse), status_code

    def get_book_orders_buy(self):
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        resonponse, status_code = self.stock_controllers.book_orders_buy_info(
            page, limit)

        return jsonify(resonponse), status_code

    def get_book_orders_sell(self):
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        resonponse, status_code = self.stock_controllers.book_orders_sell_info(
            page, limit)
        return jsonify(resonponse), status_code

    def get_market_trans_bought(self):
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        resonponse, status_code = self.stock_controllers.market_trans_bought_info(
            page, limit)
        return jsonify(resonponse), status_code

    def get_market_trans_sold(self):
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        resonponse, status_code = self.stock_controllers.market_trans_sold_info(
            page, limit)
        return jsonify(resonponse), status_code

    def crawl_stock_price_data(self):
        resonponse, status_code = self.crawl_stock_controllers.crawl_stock_price()
        return jsonify(resonponse), status_code
