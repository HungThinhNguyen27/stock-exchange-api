from model.users import User
from data_layer.mysql_connect import MySqlConnect
from decimal import Decimal


class UserData(MySqlConnect):

    def add(self, user: str) -> None:
        self.session.add(user)
        self.commit()

    def get(self):
        return self.session.query(User).all()

    def get_by_id(self, input_id):
        user = self.session.query(User).filter_by(user_id=input_id).first()
        return user

    def update_quantity_coin(self, user, quantity_coin):
        user.quantity_coin += quantity_coin
        self.commit()

    def update_account_buyer(self, buyer_id, price_coins, quantity_astra):

        buyer_account = self.get_by_id(buyer_id)
        buyer_account.quantity_coin -= price_coins * quantity_astra
        buyer_account.quantity_astra += quantity_astra
        self.commit()

    def update_account_seller(self, seller_id, price_coins, quantity_astra):
        seller_account = self.get_by_id(seller_id)
        seller_account.quantity_coin += price_coins * quantity_astra
        self.commit()

    def update_account_balance(self, user_id, coin, astra):
        account = self.session.query(User).filter_by(user_id=user_id).first()
        account.quantity_coin = coin
        account.quantity_astra = astra

    def commit(self) -> None:
        self.session.commit()
