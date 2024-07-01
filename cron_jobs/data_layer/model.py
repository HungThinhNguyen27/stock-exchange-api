from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    DECIMAL,
    String,
    ForeignKey,
    DATETIME
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from data_layer.mysql_connect import Base

class StockPrice(Base):

    """ Class representing Stock Price table. """
    __tablename__ = "stock_price_new"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time_stamp = Column(DateTime, nullable=False)
    open_price = Column(Integer, nullable=False)
    close_price = Column(Integer, nullable=False)
    high_price = Column(Integer, nullable=False)
    low_price = Column(Integer, nullable=False)
    volume = Column(Integer, nullable=False)