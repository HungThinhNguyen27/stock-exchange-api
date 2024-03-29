
from model.stock import StockPrice
from typing import List
from data_layer.mysql_connect import MySqlConnect
from sqlalchemy import func


class StockPriceDL(MySqlConnect):

    def add(self, record) -> None:
        self.session.add(record)
        self.session.commit()

    def commit(self) -> None:
        self.session.commit()

    def get_stock_data(self, limit: int, offset: int, type) -> List[StockPrice]:
        return self.session.query(StockPrice)\
            .filter(StockPrice.type == type)\
            .order_by(StockPrice.time_stamp.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()

    def count_stock_data(self, type):
        return self.session.query(func.count(StockPrice.id))\
            .filter(StockPrice.type == type)\
            .scalar()
