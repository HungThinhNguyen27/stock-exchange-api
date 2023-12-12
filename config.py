import os
from dotenv import load_dotenv


class Config(object):

    SECRET_KEY = os.environ.get("KEY")
    MYSQL_HOST = os.environ.get("MYSQL_HOST")
    MYSQL_USER = os.environ.get("MYSQL_USER")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    MYSQL_DB = os.environ.get("MYSQL_DB")
    MYSQL_PORT = os.environ.get("MYSQL_PORT")
