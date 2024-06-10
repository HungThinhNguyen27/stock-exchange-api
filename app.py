from flask import Flask, jsonify, request
import traceback
from routes.stock import Stock
from routes.user import UserRoutes
from config import Config
from flask_jwt_extended import JWTManager
from static.config import swaggerui_blueprint, SWAGGER_URL
from utils.slack_bot import send_slack_notification

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

app.register_blueprint(Stock().blueprint)
app.register_blueprint(UserRoutes().blueprint)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.errorhandler(404)
def page_not_found(e):
    # Gửi logs vào Slack khi user truy cập vào resource không tồn tại
    message = f"404 Error: {request.url} does not exist."
    send_slack_notification(message)
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(Exception)
def handle_exception(e):
    # Gửi logs vào Slack khi server gặp lỗi hoặc sập
    trace = traceback.format_exc()
    message = f"Internal Server Error: {str(e)}\n{trace}"
    send_slack_notification(message)
    return jsonify({"error": "Internal Server Error"}), 500


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=True)
        send_slack_notification("Server started successfully.")
    except Exception as e:
        send_slack_notification(f"Server started failed with Error: {e}")


# source /Users/lap01743/Downloads/WorkSpace/stock-exchange-api/env/bin/activate
