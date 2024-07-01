# from config import Config
from config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from mysql.connector import connect
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from utils.slack_bot import send_error_to_slack

MYSQL_HOST = Config.MYSQL_HOST
MYSQL_USER = Config.MYSQL_USER
MYSQL_PASSWORD = Config.MYSQL_PASSWORD
MYSQL_DB = Config.MYSQL_DB
MYSQL_PORT = Config.MYSQL_PORT
Base = sqlalchemy.orm.declarative_base()

port = 3306
host = "mysql"


class MySqlConnect:
    def __init__(self):
        self.engine = create_engine(
            f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{host}:{port}/{MYSQL_DB}",
            echo=False,
            isolation_level="READ COMMITTED"
        )

        try:
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
        except sqlalchemy.exc.SQLAlchemyError as e:
            error_message = f"SQLAlchemy error occurred: {str(e)}"
            send_error_to_slack(error_message)
            raise  # Re-raise the exception after sending to Slack

# export PYTHONPATH=$PYTHONPATH:/Users/macos/Downloads/WORKSPACE/stock_project/data_layer
