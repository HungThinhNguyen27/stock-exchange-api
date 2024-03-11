from data_layer.mysql_connect import MySqlConnect
from model.stock import MarketTransaction
from typing import List
from sqlalchemy import asc, func
from datetime import datetime


class MarketTransactionDL(MySqlConnect):

    def get(self, limit, offset) -> List[MarketTransaction]:
        return self.session.query(MarketTransaction).order_by(MarketTransaction.transaction_date.desc()
                                                              ).limit(limit).offset(offset).all()

    def count(self):
        return self.session.query(func.count(MarketTransaction.transaction_id)).scalar()

    def add_record(self, price, buyer_id, coin_used, asa_remain, taker_type):
        self.session.add(MarketTransaction(
            user_id=buyer_id,
            quantity_coin=coin_used,
            quantity_astra=asa_remain,
            transaction_date=datetime.now(),
            taker_type=taker_type,
            price=price
        ))
        self.session.commit()
