
from data_layer.mysql_connect import MySqlConnect
from data_layer.model import StockPrice
from sqlalchemy import desc


class StockPriceDL(MySqlConnect):

    def add(self, record) -> None:
        self.session.add(record)
        self.session.commit()

    def get_one_latest_record(self):
        return self.session.query(StockPrice.time_stamp).order_by(
            desc(StockPrice.time_stamp)).first()
