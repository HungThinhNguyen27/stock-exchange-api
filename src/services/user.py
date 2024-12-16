from src.data_layer.table.user import UserData

from src.data_layer.exchange import Exchange


from src.model.users import User
from src.utils.account import Account
from datetime import datetime, timedelta
from decimal import Decimal


class UserService:

    def __init__(self) -> None:
        self.user_data_layer = UserData()
        self.account_utils = Account()

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

        self.user_data_layer.add(new_user)

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

    def get_account_by_username(self, user_name):
        account = self.user_data_layer.get_by_name(user_name)
        return account

    def create_transaction_now(self, user_name, value, taker_type):

        # Get user by name
        user = self.user_data_layer.get_by_name(user_name)
        if not self.account_utils.check_balance_account(user, value, taker_type):
            return None
        # Perform transaction
        exchange_instance = Exchange(user.user_id,
                                     value,
                                     0,
                                     taker_type)

        return exchange_instance.transaction_now()

    def create_transaction_limit(self, user_name, astra_price, value, taker_type):

        # Get user by name
        user = self.user_data_layer.get_by_name(user_name)
        # Check user balance
        if not self.account_utils.check_balance_account(user, value, taker_type):
            return None
        # Perform transaction
        exchange_instance = Exchange(user.user_id,
                                     value,
                                     astra_price,
                                     taker_type)
        return exchange_instance.transaction_limit()
