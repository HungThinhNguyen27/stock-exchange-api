from functools import wraps
from flask_jwt_extended import jwt_required
from flask import request, Flask
from config import Config
import jwt
from flask import jsonify

app = Flask(__name__)
app.config.from_object(Config)


class JwtAuthentication:

    def __init__(self) -> None:
        pass

    @staticmethod
    def jwt_required_authentication(func):
        @wraps(func)
        @jwt_required()
        def decorated(*args, **kwargs):
            token = request.headers.get("Authorization")
            if token:
                token = token.split(" ")[1]
                try:
                    data = jwt.decode(
                        token, app.config["SECRET_KEY"], algorithms=["HS256"])
                    return func(*args, **kwargs)
                except jwt.ExpiredSignatureError:
                    return jsonify({"message": "Token expired"}), 401
                except jwt.InvalidTokenError:
                    return jsonify({"message": "Token invalid"}), 401
            else:
                return jsonify({"error": "No token provided"}), 400
        return decorated
