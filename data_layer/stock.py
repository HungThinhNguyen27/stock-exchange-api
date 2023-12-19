
from model.stock import StockPrice, BookOrders, MarketTransaction, Orders
from typing import List, Optional, Tuple
from data_layer.mysql_connect import MySqlConnect
from sqlalchemy.orm import aliased
import datetime


class Stock(MySqlConnect):

    def get_stock_data(self) -> List[StockPrice]:
        stock_data = self.session.query(StockPrice).all()
        return stock_data

    def get_book_orders_data(self) -> List[BookOrders]:
        return self.session.query(BookOrders).all()

    def get_market_transaction_data(self) -> List[MarketTransaction]:
        return self.session.query(MarketTransaction).all()

    def get_book_orders_id(self, id) -> List[BookOrders]:
        existing_book_order = self.session.query(BookOrders).filter_by(
            book_order_id=id).first()
        return existing_book_order

    # book_orders_alias = aliased(BookOrders)  # xem lai tại sao dùng
    def get_book_order_by_lowest_coins(self):  # xem lai tại sao dùng
        sell_orders = self.session.query(BookOrders).\
            filter(BookOrders.taker_type == 'sell').\
            order_by(BookOrders.price.desc()).\
            first()
        return sell_orders

    def add_new_buy_order(self, buyer_id, price_coins, quantity_astra):
        completed_transaction = Orders(
            user_id=buyer_id,
            order_type='buy',
            direction='completed',
            price_coins=price_coins,
            quantity_astra=price_coins*quantity_astra,
            status='completed',
            order_date=datetime.utcnow()
        )
        self.session.add(completed_transaction)

    def add_new_sell_order(self, seller_id, price_coins, quantity_astra):
        completed_transaction = Orders(
            user_id=seller_id,
            order_type='buy',
            direction='completed',
            price_coins=price_coins,
            quantity_astra=price_coins*quantity_astra,
            status='completed',
            order_date=datetime.utcnow()
        )
        self.session.add(completed_transaction)

    def delete_book_order_by_id(self, id):
        order = self.get_book_orders_id(id)
        self.session.delete(order)
        self.commit()

    def update_book_order_by_id(self, id, quantity_astra):
        order = self.get_book_orders_id(id)
        order.amount -= quantity_astra
        self.commit()

    def add(self, data) -> None:
        self.session.add(data)
        self.commit()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self):
        self.session.rollback()
        raise

    def close(self):
        self.session.close()


a = Stock()
b = a.get_book_order_by_lowest_coins()
print(b)
