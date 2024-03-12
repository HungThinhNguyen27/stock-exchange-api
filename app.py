from flask import Flask
from routes.stock import StockRoutes
from routes.user import UserRoutes
from config import Config
from flask_jwt_extended import JWTManager
from services.stock import CrawlDataStockService
import threading

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

crawl_stock = CrawlDataStockService()
stock_routes = StockRoutes()
user_routes = UserRoutes()
app.register_blueprint(stock_routes.blueprint)
app.register_blueprint(user_routes.blueprint)

if __name__ == '__main__':
    everyday_thread = threading.Thread(target=crawl_stock.run_everyday())
    everyday_thread.start()
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=True)
    # app.run(host='0.0.0.0', debug=True)  # docker
