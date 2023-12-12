from data_layer.user import UserData
from model.users import User
from utils.account import Account
from datetime import datetime, timedelta
from decimal import Decimal


class UserService:

    def __init__(self) -> None:
        self.user_data_layer = UserData()
        self.account = Account()

    def create_user(self, user_info):
        users = self.user_data_layer.get()
        user_name = [user.username for user in users]
        if user_name == user_info['user_name']:
            return None
        hashing_password = self.account.hash_password(user_info['password'])

        new_user = User(username=user_info['user_name'],
                        hashed_password=hashing_password,
                        full_name=user_info['full_name'],
                        date_of_birth=user_info['date_of_birth'],
                        email=user_info['email'],
                        phone=user_info['phone'],
                        country=user_info['country'],
                        quantity_coin=0,
                        quantity_astra=0,
                        role=user_info['role']
                        )

        add_user = self.user_data_layer.add(new_user)
        return add_user

    def login(self, username, password):
        users = self.user_data_layer.get()

        for user in users:
            if username == user.username and self.account.verify_password(password, user.hashed_password):
                return user
                break

        # if user_obj:
        #     access_token_payload = {
        #         "sub": username,
        #         "role": user.role,
        #         "exp": datetime.utcnow() + timedelta(minutes=3),
        #     }
        # acces_token = self.account.generate_tokens(access_token_payload)
        # return acces_token

    def deposite_coin(self, user_id_input, quantity_coin):
        user = self.user_data_layer.get_by_id(user_id_input)

        if user:
            quantity_coin_decimal = Decimal(quantity_coin)
            self.user_data_layer.update_quantity_coin(
                user, quantity_coin_decimal)

    def get_account_balance(self, id):
        return self.user_data_layer.get_by_id(id)
