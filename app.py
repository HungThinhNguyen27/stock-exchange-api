from flask import Flask
from routes.stock import StockRoutes
from routes.user import UserRoutes

app = Flask(__name__)

stock_routes = StockRoutes()
user_routes = UserRoutes()
app.register_blueprint(stock_routes.blueprint)
app.register_blueprint(user_routes.blueprint)

if __name__ == '__main__':
    app.run(debug=True)
