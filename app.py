from flask import Flask
from routes.stock import Stock
from routes.user import UserRoutes
from config import Config
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from static.config import swaggerui_blueprint, SWAGGER_URL

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

app.register_blueprint(Stock().blueprint)
app.register_blueprint(UserRoutes().blueprint)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=True)
    # app.run(host='0.0.0.0', debug=True)  # docker
