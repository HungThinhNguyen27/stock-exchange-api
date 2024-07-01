import hashlib
from model.users import User
import jwt
from config import Config


class Account:
    def __init__(self) -> None:
        pass

    def hash_password(self, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def verify_password(self, input_password, hashed_password):
        hashed_input_password = self.hash_password(input_password)
        return hashed_input_password == hashed_password

    def generate_tokens(self, payload):
        return jwt.encode(
            payload, Config.SECRET_KEY, algorithm="HS256")

    def check_balance_account(self, user, value, taker_type):  # đưa lên services
        if taker_type == 'buy' and user.quantity_coin >= value:
            return True
        elif taker_type == 'sell' and user.quantity_astra >= value:
            return True
        return False
