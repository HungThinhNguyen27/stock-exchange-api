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

    def commit(self) -> None:
        self.session.commit()
