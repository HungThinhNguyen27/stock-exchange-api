from services.user import User
from flask import jsonify
from services.user import UserService


class UserControllers:

    def __init__(self) -> None:
        self.user_services = UserService()

    def create_user(self, request_data):
        user_info = {
            "user_name": request_data.get("user_name"),
            "password": request_data.get("password"),
            "full_name": request_data.get("full_name"),
            "date_of_birth": request_data.get("date_of_birth"),
            "email": request_data.get("email"),
            "phone": request_data.get("phone"),
            "country": request_data.get("country"),
            "role": request_data.get("role")
        }
        self.user_services.create_user(user_info)
        return {'Create account successfully ': user_info['user_name']}, 200

    def login(self, request_data):
        user_name = request_data.get('username')
        password = request_data.get('password')

        if not user_name or not password:
            return {'error': 'Missing username or password'}, 400
        token_user = self.user_services.login(user_name, password)
        if token_user:
            return {"access_token": token_user}, 200
        else:
            return {'error': 'Invalivd username or password'}, 400

    def get_balance_account(self, current_user):
        account = self.user_services.get_account_by_username(current_user)
        return {
            "account": account.username,
            "quantity_coin": account.quantity_coin,
            "quantity_astra": account.quantity_astra,
        }, 200

    def create_transaction(self, current_user, request_data):

        taker_type = str(request_data.get("taker_type"))
        type = str(request_data.get("type"))
        input_value = int(request_data.get("quantity"))

        if taker_type not in ["buy", "sell"] or type not in ["now", "limit"]:
            return {"status": "error",
                    "message": "Please enter taker_type as [buy or sell] and type as [now or limit]"}, 400

        if type == "now":
            astra_price = int(request_data.get("astra_price", 0))
            if input_value == 0:
                return {"status": "error",
                        "message": "Please enter quantity "}, 400
        else:
            astra_price = int(request_data.get("astra_price"))
            if astra_price == 0 or input_value == 0:
                return {"status": "error",
                        "message": "Please enter astra_price for type 'limit' and quantity "}, 400

        if type == "limit":
            data_trans = self.user_services.create_transaction_limit(current_user,
                                                                     astra_price,
                                                                     input_value,
                                                                     taker_type)
        else:
            data_trans = self.user_services.create_transaction_now(current_user,
                                                                   input_value,
                                                                   taker_type)
        if data_trans:
            return {"message": f"Transaction {taker_type} {type} completed successfully.",
                    "status": "success",
                    "data": data_trans}, 200
        else:
            return {"message": "Insufficient funds for the transaction.",
                    "status": "error",
                    "data": data_trans}, 400
