
from src.config import Config
import requests


TELEGRAM_TOKEN = Config.TELEGRAM_TOKEN
CHAT_ID_TELEGRAM = Config.CHAT_ID_TELEGRAM


def send_error_to_telegram(error_message):
    try:
        text = f"Notification:\n```{error_message}```"
        base_url = 'https://api.telegram.org/bot{}/SendMessage?chat_id={}&text="{}"'.format(TELEGRAM_TOKEN, CHAT_ID_TELEGRAM,text)
        requests.get(base_url)
        print("Error message sent to Telegram successfully.")
    except Exception as e:
        print(f"Failed to send error message to Telegram: {e}")

