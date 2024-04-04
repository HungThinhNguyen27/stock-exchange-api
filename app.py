from flask import Flask
from routes.stock import StockRoutes
from routes.user import UserRoutes
from config import Config
from flask_jwt_extended import JWTManager
from services.stock import CrawlDataStockService
from flask_swagger_ui import get_swaggerui_blueprint
from pytz import timezone

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.yaml'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Stock Exchange APIs application"
    },
)

crawl_stock = CrawlDataStockService()
stock_routes = StockRoutes()
user_routes = UserRoutes()
app.register_blueprint(stock_routes.blueprint)
app.register_blueprint(user_routes.blueprint)
app.register_blueprint(swaggerui_blueprint)


if __name__ == '__main__':

    # app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=True)
    app.run(host='0.0.0.0', debug=True)  # docker
