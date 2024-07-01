from config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from mysql.connector import connect
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy

MYSQL_HOST = Config.MYSQL_HOST
MYSQL_USER = Config.MYSQL_USER
MYSQL_PASSWORD = Config.MYSQL_PASSWORD
MYSQL_DB = Config.MYSQL_DB
MYSQL_PORT = Config.MYSQL_PORT
Base = sqlalchemy.orm.declarative_base()

port = 3306
host = "mysql" # dọcker


class MySqlConnect:
    def __init__(self):
        self.engine = create_engine(
            f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{host}:{port}/{MYSQL_DB}",
            echo=False,
            isolation_level="READ COMMITTED"
        )

        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
