
from data_layer.stock import Stock
from model.users import User


class StockService:

    def __init__(self) -> None:
        self.stock = Stock()

    def get_stock_candles(self):
        stock_list = self.stock.get_stock_data()
        return stock_list

    def get_book_orders(self):
        return self.stock.get_book_orders_data()

    def get_market_trans(self):
        return self.stock.get_market_transaction_data()
