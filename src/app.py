from flask import Flask, jsonify, request
import traceback
from src.routes.stock import Stock
from src.routes.user import UserRoutes
from src.config import Config
from flask_jwt_extended import JWTManager
from src.static.config import swaggerui_blueprint, SWAGGER_URL
from src.utils.telegram_bot import send_error_to_telegram

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

app.register_blueprint(Stock().blueprint)
app.register_blueprint(UserRoutes().blueprint)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.errorhandler(Exception)
def handle_error(e):
    send_error_to_telegram(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=True)
    # app.run(host='0.0.0.0', debug=True, use_reloader=True) #docker 



# source /Users/lap01743/Desktop/WorkSpace/stock-exchange-api/env/bin/activate
