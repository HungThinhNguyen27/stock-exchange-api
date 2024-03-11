from model.users import User
from data_layer.mysql_connect import MySqlConnect
from decimal import Decimal


class UserData(MySqlConnect):

    def add(self, user: str) -> None:
        self.session.add(user)

    def get(self):
        return self.session.query(User).all()

    def get_by_name(self, user_name):
        user = self.session.query(User).filter_by(username=user_name).first()
        return user

    def get_by_id(self, user_id):
        user = self.session.query(User).filter_by(user_id=user_id).first()
        return user

    def check_balance_coins(self, user_id, coins_using):
        user = self.get_by_id(user_id)
        if user.quantity_coin >= coins_using:
            return True

    def check_balance_asa(self, user_id, asa_using):
        user = self.get_by_id(user_id)
        if user.quantity_astra >= asa_using:
            return True

    def update_plus_coin(self, id, quantity_coin):
        account = self.get_by_id(id)
        account.quantity_coin += quantity_coin
        self.session.commit()

    def update_minus_coin(self, id, quantity_coin):
        account = self.get_by_id(id)
        account.quantity_coin -= quantity_coin
        self.session.commit()

    def update_plus_astra(self, id, quantity_astra):
        account = self.get_by_id(id)
        account.quantity_astra += quantity_astra
        self.session.commit()

    def update_minus_atrsa(self, id, quantity_astra):
        account = self.get_by_id(id)
        account.quantity_astra += quantity_astra
        self.session.commit()

    def update_account_buyer(self, account, asa_received, quantity_coin):
        account.quantity_coin -= quantity_coin
        account.quantity_astra += asa_received
        self.session.commit()

    def update_account_seller(self, account, coin_received, quantity_asa):
        account.quantity_coin += coin_received
        account.quantity_astra -= quantity_asa
        self.session.commit()

    def update_account_buy_limit(self, current_user, quantity_coins):
        account = self.get_by_name(current_user)
        account.quantity_coin -= quantity_coins
        self.session.commit()

    def update_account_sell_limit(self, current_user, quantity_asa):
        account = self.get_by_name(current_user)
        account.quantity_astra -= quantity_asa
        self.session.commit()
