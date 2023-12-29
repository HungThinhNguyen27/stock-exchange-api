
# from data_layer.user import UserData
# from data_layer.stock import Stock
from data_layer.mysql_connect import MySqlConnect
from sqlalchemy import asc, func,  distinct, and_
from data_layer.user import UserData
from data_layer.stock import Stock, BookOrders
from utils.stock_utils import StockUtils
from collections import defaultdict
from model.users import User


class PurchaseTransaction(MySqlConnect):
    def __init__(self):
        super().__init__()
        self.stock_data_layer = Stock()
        self.stock_utils = StockUtils()
        self.user_data_layer = UserData()

    def get_lowest_price(self):
        lowest_price = (
            self.session.query(
                BookOrders.price,
                func.sum(BookOrders.total).label('total'),
                func.group_concat(
                    distinct(BookOrders.user_id)).label('user_ids'),
            )
            .filter(BookOrders.taker_type == "sell")
            .group_by(BookOrders.price)
            .order_by(asc(BookOrders.price))
            .all()
        )
        min_price, quantity_asaa, seller_id = lowest_price[0]
        seller_id_list = [int(user_id)
                          for user_id in seller_id.split(',') if user_id]
        quantity_asa = int(quantity_asaa)
        return min_price, quantity_asa, seller_id_list

    def get_by_id(self, user_id):
        user = self.session.query(User).filter_by(user_id=user_id).first()
        return user

    def check_balance(self, current_user, quantity_coin):

        get_balance_account = self.user_data_layer.get_account_balance(current_user
                                                                       )
        if get_balance_account >= quantity_coin:
            return True
        else:
            return None

    def update_account_buyer(self, current_user, asa_received, remaining_coin, quantity_coin):
        buyer_account = self.user_data_layer.get_by_name(current_user)

        buyer_account.quantity_coin -= quantity_coin
        buyer_account.quantity_astra += asa_received
        buyer_account.quantity_coin += remaining_coin
        return buyer_account

    def buy_now_trans(self, current_user, quantity_coin):
        check_balance = self.check_balance(current_user, quantity_coin)

        try:
            with self.session.begin():
                if check_balance is True:
                    min_price, quantity_asa, seller_id_list = self.get_lowest_price()
                    asa_received = quantity_coin // min_price
                    remaining_coin = quantity_coin % min_price
                    update_account_buyer = self.update_account_buyer(current_user,
                                                                     asa_received,
                                                                     remaining_coin,
                                                                     quantity_coin)
                    self.session.merge(update_account_buyer)
                    self.session.commit()
                    return True
                else:
                    return None
        except Exception as e:
            print(f"Error: {e}")
            self.session.rollback()

# a = PurchaseTransaction()
# b, c, d = a.get_lowest_price()

# print(b, c, d)
