from data_layer.user import UserData
from data_layer.transaction import PurchaseTransaction
from model.users import User
from utils.account import Account
from datetime import datetime, timedelta
from decimal import Decimal


class UserService:

    def __init__(self) -> None:
        self.user_data_layer = UserData()
        self.account_utils = Account()
        self.transaction_data_layer = PurchaseTransaction()

    def create_user(self, user_info):
        users = self.user_data_layer.get()
        user_name = [user.username for user in users]
        if user_name == user_info['user_name']:
            return None
        hashing_password = self.account_utils.hash_password(
            user_info['password'])

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

    def login(self, username, password):
        users = self.user_data_layer.get()
        authenticated_user = None
        access_token_payload = {}

        for user in users:
            if username == user.username and self.account_utils.verify_password(password, user.hashed_password):
                authenticated_user = user
                access_token_payload = {
                    "sub": username,
                    "role": authenticated_user.role,
                    "exp": datetime.utcnow() + timedelta(minutes=15),
                }
                break
        access_token = None
        if authenticated_user:
            access_token = self.account_utils.generate_tokens(
                access_token_payload)
        return access_token

    def deposite_coin(self, user_id_input, quantity_coin):
        user = self.user_data_layer.get_by_id(user_id_input)

        if user:
            quantity_coin_decimal = Decimal(quantity_coin)
            self.user_data_layer.update_quantity_coin(user,
                                                      quantity_coin_decimal)

    def buy_stock_now(self, current_user, quantity_coin):

        transaction_process = self.transaction_data_layer.buy_now_trans(current_user,
                                                                        quantity_coin)

        # min_price, quantity_asa, seller_id = self.transaction_data_layer.get_lowest_price()

        # asa_received = quantity_coin // min_price
        # remaining_coin = quantity_coin % min_price

        return transaction_process

    def check_balance(self, current_user, quantity_coin):
        quantity_coin_value = int(quantity_coin[0])
        get_balance_account = self.user_data_layer.get_account_balance(current_user
                                                                       )

        if get_balance_account >= quantity_coin_value:
            return get_balance_account
        else:
            return None
