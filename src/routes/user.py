from flask import Flask, Blueprint, jsonify, request
from src.controllers.user import UserControllers
from src.middlewares.authentication import JwtAuthentication
from flask_jwt_extended import jwt_required, get_jwt_identity


class UserRoutes:

    def __init__(self) -> None:

        self.user_controllers = UserControllers()
        self.jwt_ath = JwtAuthentication()
        self.blueprint = Blueprint('users', __name__)
        self.blueprint.add_url_rule("/account", 'create_account',
                                    self.create, methods=["POST"])
        self.blueprint.add_url_rule("/login", 'login',
                                    self.login, methods=["POST"])
        self.blueprint.add_url_rule("/account-balance", 'get_account_balance',
                                    self.jwt_ath.jwt_required_authentication(self.get_balance), methods=["GET"])
        self.blueprint.add_url_rule("/transactions", 'transactions',
                                    self.jwt_ath.jwt_required_authentication(self.create_transactions), methods=["POST"])

    def create(self):
        request_data = request.get_json()
        response_data, status_code = self.user_controllers.create_user(request_data
                                                                       )
        return jsonify(response_data), status_code

    def login(self):
        request_data = request.get_json()
        response_data, status_code = self.user_controllers.login(request_data)
        return jsonify(response_data), status_code

    def get_balance(self):
        current_user = get_jwt_identity()
        response_data, status_code = self.user_controllers.get_balance_account(current_user
                                                                               )
        return jsonify(response_data), status_code

    def create_transactions(self):
        current_user = get_jwt_identity()
        request_data = request.get_json()
        respone_data, status_code = self.user_controllers.create_transaction(current_user,
                                                                             request_data)
        return jsonify(respone_data), status_code
