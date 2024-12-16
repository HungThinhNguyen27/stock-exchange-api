from src.model.users import User
from src.data_layer.mysql_connect import MySqlConnect
from decimal import Decimal


class UserData(MySqlConnect):

    def add(self, user: str) -> None:
        self.session.add(user)
        self.session.commit()

    def get(self):
        return self.session.query(User).all()

    def get_by_name(self, user_name):
        user = self.session.query(User).filter_by(username=user_name).first()
        return user

    def get_by_id(self, user_id):
        user = self.session.query(User).filter_by(user_id=user_id).first()
        return user

    def update_balance_buyers_or_sellers(self, id, value, taker_type):
        account = self.get_by_id(id)
        if taker_type == "buy":
            account.quantity_astra += value
        else:
            account.quantity_coin += value
        self.session.commit()

    def update_balance_traders_trans_limit(self, user_id, quantity, transaction_type):
        account = self.get_by_id(user_id)
        if transaction_type == "buy":
            account.quantity_coin -= quantity
        elif transaction_type == "sell":
            account.quantity_astra -= quantity
        self.session.commit()

    def update_balance_traders_trans_now(self, user_id, total_received, total_spent, taker_type):
        account = self.get_by_id(user_id)
        if taker_type == "sell":
            account.quantity_coin += total_received
            account.quantity_astra -= total_spent
        else:
            account.quantity_coin -= total_spent
            account.quantity_astra += total_received
        self.session.commit()
