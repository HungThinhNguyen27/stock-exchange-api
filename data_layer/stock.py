
from model.stock import StockPrice, BookOrders, MarketTransaction
from typing import List, Optional, Tuple
from data_layer.mysql_connect import MySqlConnect


class Stock(MySqlConnect):

    def get_stock_data(self) -> List[StockPrice]:
        stock_data = self.session.query(StockPrice).all()
        return stock_data

    def get_book_orders_data(self) -> List[BookOrders]:
        return self.session.query(BookOrders).all()

    def get_market_transaction_data(self) -> List[MarketTransaction]:
        return self.session.query(MarketTransaction).all()

    def commit(self) -> None:
        self.session.commit()
