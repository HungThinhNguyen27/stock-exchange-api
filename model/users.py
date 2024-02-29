
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DECIMAL
)
from sqlalchemy.orm import relationship
from data_layer.mysql_connect import Base


class User(Base):

    """Class representing users table."""

    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    full_name = Column(String(200), nullable=False)
    date_of_birth = Column(Date)
    email = Column(String(200), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    country = Column(String(200))
    quantity_coin = Column(Integer, nullable=False)
    quantity_astra = Column(Integer, nullable=False)
    role = Column(String(50), nullable=False)

    orders = relationship('Orders', back_populates='user')
    book_orders = relationship('BookOrders', back_populates='user')
    market_transactions = relationship(
        'MarketTransaction', back_populates='user')
