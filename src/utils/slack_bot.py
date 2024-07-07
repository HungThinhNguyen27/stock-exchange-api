# notifications.py

import slack
import json
import certifi
import ssl
import traceback
from src.config import Config

ssl_context = ssl.create_default_context(cafile=certifi.where())


SLACK_TOKEN = Config.SLACK_TOKEN
client = slack.WebClient(token=SLACK_TOKEN, ssl=ssl_context)

def send_error_to_slack(error_message):
    try:
        client.chat_postMessage(channel='#error-checking', text=f"Error occurred:\n```{error_message}```")
        print("Error message sent to Slack successfully.")
    except Exception as e:
        print(f"Failed to send error message to Slack: {e}")
        traceback.print_exc()
