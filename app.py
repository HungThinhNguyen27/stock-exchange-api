from flask import Flask
from routes.stock import StockRoutes
from routes.user import UserRoutes
from config import Config
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

stock_routes = StockRoutes()
user_routes = UserRoutes()
app.register_blueprint(stock_routes.blueprint)
app.register_blueprint(user_routes.blueprint)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
    # app.run(host='0.0.0.0', debug=True)  # docker
