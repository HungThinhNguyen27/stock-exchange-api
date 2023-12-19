from services.stock import StockService, CrawlDataStockService
from flask import jsonify


class StockControllers:

    def __init__(self) -> None:
        self.stock_service = StockService()

    def stock_info(self):

        stock_list = self.stock_service.get_stock_candles()
        stock_data = []

        for stock in stock_list:
            stock_dict = {
                # "id": stock.id,
                "time_stamp": stock.time_stamp,
                "open_price": stock.open_price,
                "close_price": stock.close_price,
                "high_price": stock.high_price,
                "low_price": stock.low_price,
                "volume": stock.volume
            }
            stock_data.append(stock_dict)

        return stock_data, 200

    def book_orders_info(self):

        book_order_list = self.stock_service.get_book_orders()
        book_order_data = []
        for book_order in book_order_list:
            book_order_dict = {
                "book_order_id": book_order.book_order_id,
                "user_id": book_order.user_id,
                "price": book_order.price,
                "total": book_order.total,
                "market": book_order.market,
                "created_at": book_order.created_at,
                "taker_type": book_order.taker_type,

            }
            book_order_data.append(book_order_dict)

        return book_order_data, 200

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

    def buy_stock_now(self, request_data):

        price = request_data.get('quantity_coin'),

        buy_now_status = self.stock_service.buy_stock_now(price)
        if buy_now_status:
            return {"Buy Success": buy_now_status}, 200
        else:
            return {"error": "not enough coins"}, 404

    def buy_stock_limit(self, reqsuest_data):
        pass


class CrawlStockController:

    def __init__(self) -> None:
        self.crawl_stock_service = CrawlDataStockService()

    def crawl_book_orders(self):
        self.crawl_stock_service.crawl_book_orders_data()
        return {'message': 'Crawl data successful'}, 200

    def crawl_stock_price(self):
        self.crawl_stock_service.crawl_stock_price_data()
        return {'message': 'Crawl stock data successful'}, 200
