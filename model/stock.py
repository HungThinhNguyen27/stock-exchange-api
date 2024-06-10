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
    __tablename__ = "stock_price_new"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time_stamp = Column(DateTime, nullable=False)
    open_price = Column(Integer, nullable=False)
    close_price = Column(Integer, nullable=False)
    high_price = Column(Integer, nullable=False)
    low_price = Column(Integer, nullable=False)
    volume = Column(Integer, nullable=False)


class BookOrders(Base):

    """ Class representing Book Orders table. """
    __tablename__ = "book_orders"

    book_order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    price_coins = Column(Integer, nullable=False)
    amount_asa = Column(Integer, nullable=False)
    total_coins = Column(Integer, nullable=False)
    market = Column(String(20), nullable=False)
    created_at = Column(DateTime, nullable=False)
    taker_type = Column(String(20), nullable=False)
    user = relationship('User', back_populates='book_orders')


class MarketTransaction(Base):
    """ Class representing Market Transaction table. """
    __tablename__ = "market_transaction"

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    quantity_coin = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    quantity_astra = Column(Integer, nullable=False)
    transaction_date = Column(DATETIME)
    taker_type = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))

    # Relationship with the User table
    user = relationship('User', back_populates='market_transactions')


class Orders(Base):

    """ Class representing Order table. """

    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    order_type = Column(String(20))
    direction = Column(String(20))
    price_coins = Column(Integer)
    quantity_astra = Column(Integer)
    status = Column(String(20))
    order_date = Column(DATETIME)

    user = relationship('User', back_populates='orders')
