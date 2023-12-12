import hashlib
from model.users import User
# import jwt
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

    # def generate_tokens(self, paylaod):
    #     return jwt.encode(
    #         paylaod, Config.SECRET_KEY, algorithm="HS256")
