from services.user import User
from flask import jsonify
from services.user import UserService


class UserControllers:

    def __init__(self) -> None:
        self.user_services = UserService()

    def create_user(self, user_info):
        user_info = {
            "user_name": user_info.get("user_name"),
            "password": user_info.get("password"),
            "full_name": user_info.get("full_name"),
            "date_of_birth": user_info.get("date_of_birth"),
            "email": user_info.get("email"),
            "phone": user_info.get("phone"),
            "country": user_info.get("country"),
            "role": user_info.get("role")
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
            return {'error': 'Invalid username or password'}, 401

    def deposite_coin(self, request_data):

        user_id = request_data.get('user_id')
        quantity_coin = request_data.get('quantity_coin')

        self.user_services.deposite_coin(user_id, quantity_coin)

        return {'Your account has been added': quantity_coin}, 200

    def get_account_balance(self, id):

        user = self.user_services.get_account_balance(id)
        if user:
            user_data = {
                'user_id': user.user_id,
                'username': user.username,
                'quantity_coin': user.quantity_coin,
                'quantity_astra': user.quantity_astra
            }
            return user_data, 200

    # ----------------------- fix output

    def buy_stock_now(self, current_user, request_data):

        input_coins = int(request_data.get('quantity_coin'))

        data_trans = self.user_services.buy_stock_now(current_user,
                                                      input_coins)
        if data_trans:
            return {"message": "Transaction completed successfully.",
                    "status": "success",
                    "data": data_trans}, 200
        else:
            return {"message": "Insufficient funds for the transaction.",
                    "status": "error",
                    "data": data_trans}, 200

    def sell_stock_now(self, current_user, request_data):

        input_asa = int(request_data.get('quantity_asa'))

        data_trans = self.user_services.sell_stock_now(current_user,
                                                       input_asa)

        if data_trans:
            return {"message": "Transaction completed successfully.",
                    "status": "success",
                    "data": data_trans}, 200
        else:
            return {"message": "Insufficient funds for the transaction.",
                    "status": "error",
                    "data": data_trans}, 200

    def buy_stock_limit(self, current_user, request_data):

        astra_price = int(request_data.get('astra_price'))

        coins_quantity = int(request_data.get('coins_quantity'))

        data_trans = self.user_services.buy_stock_limit(current_user,
                                                        astra_price,
                                                        coins_quantity)

        if data_trans:

            data = {
                "Astra Price": data_trans[0],
                "The number of Coins you used": data_trans[1],
                "Amount of Asa will receive": data_trans[2],
            }
            return {"status": "success",
                    "message": "Transaction completed successfully.",
                    "data": data}, 200
        else:
            return {"message": "Insufficient funds for the transaction.",
                    "status": "error"}, 200

    def sell_stock_limit(self, current_user, request_data):

        astra_price = int(request_data.get('astra_price'))
        asa_quantity = int(request_data.get('asa_quantity'))

        data_trans = self.user_services.sell_stock_limit(current_user,
                                                         astra_price,
                                                         asa_quantity)

        if data_trans:
            data = {
                "Astra Price": data_trans[0],
                "The number of Astra you used": data_trans[1],
                "Amount of Coins will receive": data_trans[2],
            }

            return {"status": "success",
                    "message": "Transaction completed successfully.",
                    "data": data}, 200
        else:
            return {"message": "Insufficient funds for the transaction.",
                    "status": "error"}, 200
