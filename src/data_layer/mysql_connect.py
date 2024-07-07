# from config import Config
from src.config import Config
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from src.utils.telegram_bot import send_error_to_telegram


MYSQL_HOST = Config.MYSQL_HOST
MYSQL_USER = Config.MYSQL_USER
MYSQL_PASSWORD = Config.MYSQL_PASSWORD
MYSQL_DB = Config.MYSQL_DB
MYSQL_PORT = Config.MYSQL_PORT

metadata = MetaData()
Base = declarative_base(metadata=metadata)

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
            send_error_to_telegram(error_message)
            raise  

# export PYTHONPATH=$PYTHONPATH:/Users/lap01743/Desktop/WorkSpace/stock-exchange-api/src/data_layer
# export PYTHONPATH=$PYTHONPATH:/Users/lap01743/Desktop/WorkSpace/stock-exchange-api/src/config.py
