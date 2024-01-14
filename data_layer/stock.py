
from model.stock import StockPrice, BookOrders, MarketTransaction, Orders
from typing import List, Optional, Tuple
from data_layer.mysql_connect import MySqlConnect
from sqlalchemy.orm import aliased
from sqlalchemy import asc, func, desc
from collections import defaultdict


class Stock(MySqlConnect):

    def get_stock_data(self) -> List[StockPrice]:
        stock_data = self.session.query(StockPrice).all()
        return stock_data

    def paging_book_orders(self, offset, per_page) -> List[BookOrders]:
        return self.session.query(BookOrders).limit(per_page).offset(offset).all()

    def get_market_transaction_data(self) -> List[MarketTransaction]:
        return self.session.query(MarketTransaction).all()

    def get_book_orders_id(self, id) -> List[BookOrders]:
        existing_book_order = self.session.query(BookOrders).filter_by(
            book_order_id=id).first()
        return existing_book_order

    def add(self, data) -> None:
        self.session.add(data)
        self.commit()

    def commit(self) -> None:
        self.session.commit()

    def get_book_order_asc(self):
        return self.session.query(BookOrders).order_by(asc(BookOrders.price_coins)).all()

    def sum_total_by_taker_type(self, taker_type, offset, limit):
        result = (
            self.session.query(BookOrders.price_coins, func.sum(
                BookOrders.amount_asa).label('total'))
            .filter(BookOrders.taker_type == taker_type)
            .group_by(BookOrders.price_coins)
            .order_by(asc(BookOrders.price_coins))
            .offset(offset)
            .limit(limit)
            .all()
        )

        return result

    def count_distinct_prices(self, taker_type):
        query = (
            self.session.query(func.count(
                func.distinct(BookOrders.price_coins)))
            .filter(BookOrders.taker_type == taker_type)
        )

        book_order_count = query.scalar()

        return book_order_count
