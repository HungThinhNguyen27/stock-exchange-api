import os
from dotenv import load_dotenv
import yaml


class Config(object):
    with open(os.path.join(os.path.dirname(__file__), "config.yaml"), 'r') as stream:
        config = yaml.safe_load(stream)

    SECRET_KEY = config['KEY']
    MYSQL_HOST = config['MYSQL_HOST']
    MYSQL_PORT = config['MYSQL_PORT']
    MYSQL_USER = config['MYSQL_USER']
    MYSQL_PASSWORD = config['MYSQL_PASSWORD']
    MYSQL_DB = config['MYSQL_DB']

    REDIS_PORT = config['REDIS_PORT']
    REDIS_HOST = config['REDIS_HOST']
    SLACK_TOKEN = config['SLACK_TOKEN']

    TELEGRAM_TOKEN = config['TELEGRAM_TOKEN']
    CHAT_ID_TELEGRAM = config['CHAT_ID_TELEGRAM']
    