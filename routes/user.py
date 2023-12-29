from flask import Flask, Blueprint, jsonify, request
from controllers.user import UserControllers
from middlewares.authentication import JwtAuthentication
from flask_jwt_extended import jwt_required, get_jwt_identity


class UserRoutes:

    def __init__(self) -> None:
        self.user_controllers = UserControllers()
        self.jwt_ath = JwtAuthentication()

        self.blueprint = Blueprint('users', __name__)
        self.blueprint.add_url_rule("/account", 'create_account',
                                    self.create_account, methods=["POST"])
        self.blueprint.add_url_rule("/login", 'login',
                                    self.login, methods=["POST"])
        self.blueprint.add_url_rule("/desposite-coin", 'deposite_coin',
                                    self.jwt_ath.jwt_required_authentication(self.deposite_coin), methods=["PUT"])
        self.blueprint.add_url_rule("/account-balance/<int:id>", 'get_account_balance',
                                    self.jwt_ath.jwt_required_authentication(self.get_account_balance,), methods=["GET"])

        self.blueprint.add_url_rule("/buy-now", 'buy_stock_now',
                                    self.jwt_ath.jwt_required_authentication(self.buy_stock_now), methods=["PUT"])

    def create_account(self):

        user_info = request.get_json()
        response_data, status_code = self.user_controllers.create_user(
            user_info)
        return jsonify(response_data), status_code

    def login(self):

        request_data = request.get_json()
        response_data, status_code = self.user_controllers.login(request_data)

        return jsonify(response_data), status_code

    def deposite_coin(self):
        request_data = request.get_json()
        response_data, status_code = self.user_controllers.deposite_coin(
            request_data)

        return jsonify(response_data), status_code

    def get_account_balance(self, id):

        response_data, status_code = self.user_controllers.get_account_balance(
            id)
        return jsonify(response_data), status_code

    def buy_stock_now(self):

        current_user = get_jwt_identity()
        request_data = request.get_json()
        respone_data, status_code = self.user_controllers.buy_stock_now(current_user,
                                                                        request_data)
        return jsonify(respone_data), status_code
