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
from model.users import User
from data_layer.mysql_connect import Base


class StockPrice(Base):

    """ Class representing Stock Price table. """
    __tablename__ = "stock_price"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time_stamp = Column(DateTime, nullable=False)
    open_price = Column(DECIMAL(10, 2))
    close_price = Column(DECIMAL(10, 2))
    high_price = Column(DECIMAL(10, 2))
    low_price = Column(DECIMAL(10, 2))
    volume = Column(Integer)


class BookOrders(Base):

    """ Class representing Book Orders table. """
    __tablename__ = "book_orders"

    book_order_id = Column(Integer, primary_key=True, autoincrement=True)
    quantity_coin = Column(DECIMAL(17, 3), nullable=False)
    quantity_astra = Column(DECIMAL(10, 3), nullable=False)
    order_types = Column(String(20))
    status = Column(String(20))


class MarketTransaction(Base):

    """ Class representing Market Transaction table. """
    __tablename__ = "market_transaction"

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    book_order_id = Column(Integer, ForeignKey('book_orders.book_order_id'))
    quantity_coin = Column(DECIMAL(17, 0), nullable=False)
    quantity_astra = Column(DECIMAL(10, 3), nullable=False)
    transaction_date = Column(DATETIME)


class Order(Base):

    """ Class representing Order table. """

    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    order_type = Column(String(20))
    direction = Column(String(20))
    quantity = Column(Integer)
    price = Column(DECIMAL(18, 4))
    status = Column(String(20))
    order_date = Column(DATETIME)

    user = relationship('User', back_populates='orders')
