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
    price = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    market = Column(String(20), nullable=False)
    created_at = Column(DateTime, nullable=False)
    taker_type = Column(String(20), nullable=False)
    user = relationship('User', back_populates='book_orders')
    market_transaction = relationship(
        'MarketTransaction', back_populates='book_order')


class MarketTransaction(Base):

    """ Class representing Market Transaction table. """
    __tablename__ = "market_transaction"

    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    book_order_id = Column(Integer, ForeignKey('book_orders.book_order_id'))
    quantity_coin = Column(Integer, nullable=False)
    quantity_astra = Column(DECIMAL(10, 3), nullable=False)
    transaction_date = Column(DATETIME)

    book_order = relationship(
        'BookOrders', back_populates='market_transaction')


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
