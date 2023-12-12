from services.stock import StockService
from flask import jsonify


class StockControllers:

    def __init__(self) -> None:
        self.stock_service = StockService()

    def stock_info(self):

        stock_list = self.stock_service.get_stock_candles()
        stock_data = []

        for stock in stock_list:
            stock_dict = {
                "id": stock.id,
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
                "quantity_coin": book_order.quantity_coin,
                "quantity_astra": book_order.quantity_astra,
                "order_types": book_order.order_types
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
        user_id = request_data.get('user_id')
        quantity_astra = request_data.get('quantity_astra')

        if quantity_astra <= 0:
            return {'error': 'The number of astra must be greater than 0'}, 400
        else:
            return {'message': 'buy successful'}, 200

    def buy_stock_limt(self, request_data):
        pass
