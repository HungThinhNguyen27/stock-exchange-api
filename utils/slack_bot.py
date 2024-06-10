# notifications.py

import requests
import json

def send_slack_notification(message):
    webhook = "https://hooks.slack.com/services/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"
    data = {
        "text": message
    }
    response = requests.post(webhook, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    if response.status_code != 200:
        raise ValueError(f'Request to Slack returned an error {response.status_code}, the response is:\n{response.text}')