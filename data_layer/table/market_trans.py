from data_layer.mysql_connect import MySqlConnect
from model.stock import MarketTransaction
from typing import List
from sqlalchemy import asc, func


class MarketTransactionDL(MySqlConnect):

    def get_market_transaction(self, limit, offset) -> List[MarketTransaction]:
        return self.session.query(MarketTransaction).order_by(MarketTransaction.transaction_date.desc()
                                                              ).limit(limit).offset(offset).all()

    def count_market_transactions(self):
        return self.session.query(func.count(MarketTransaction.transaction_id)).scalar()
