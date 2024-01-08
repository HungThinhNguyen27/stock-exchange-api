
# from data_layer.user import UserData
# from data_layer.stock import Stock
from data_layer.mysql_connect import MySqlConnect
from sqlalchemy import asc, func,  distinct, and_, desc
from data_layer.user import UserData
from data_layer.stock import Stock, BookOrders
from utils.stock_utils import StockUtils
from collections import defaultdict
from model.users import User


class BuyTransaction(MySqlConnect):
    def __init__(self):
        super().__init__()
        self.stock_data_layer = Stock()
        self.stock_utils = StockUtils()
        self.user_data_layer = UserData()

    def get_lowest_price(self):
        lowest_price = (
            self.session.query(
                BookOrders.price_coins,
                func.sum(BookOrders.amount_asa),
                func.group_concat(
                    distinct(BookOrders.user_id)).label('user_ids'),

            )
            .filter(BookOrders.taker_type == "sell")
            .group_by(BookOrders.price_coins)
            .order_by(asc(BookOrders.price_coins))
            .all()
        )
        min_price, quantity_asaa, seller_id = lowest_price[0]
        seller_id_list = [int(user_id)
                          for user_id in seller_id.split(',') if user_id]

        quantity_asa = int(quantity_asaa)
        return min_price, quantity_asa, seller_id_list

    def get_user_by_id(self, user_id):
        user = self.session.query(User).filter_by(user_id=user_id).first()
        return user

    def get_book_order_by_id(self, id):
        book_order = self.session.query(
            BookOrders).filter_by(book_order_id=id).first()
        return book_order

    def get_book_order_id_by_min_price(self, price):

        results = (
            self.session.query(BookOrders.book_order_id)
            .filter(BookOrders.taker_type == 'sell')
            .filter(BookOrders.price_coins == price)
            .order_by(BookOrders.price_coins.asc())
        )
        book_order_ids = [item[0] for item in results]
        return book_order_ids

    def check_balance(self, current_user, quantity_coin):
        self.user_data_layer.get_user_asa(current_user) >= quantity_coin
        return True

    def get_longest_seller(self, seller_id_list):

        sellers = self.session.query(BookOrders.user_id,
                                     func.max(BookOrders.created_at)
                                     ).filter(
            BookOrders.user_id.in_(seller_id_list)
        ).group_by(
            BookOrders.user_id
        ).having(
            func.count(BookOrders.user_id) > 1
        ).order_by(
            func.max(BookOrders.created_at).desc()
        ).all()

        seller_list = [seller[0] for seller in sellers]
        return seller_list

    def update_account_buyer(self, current_user, asa_received, quantity_coin):
        buyer_account = self.user_data_layer.get_by_name(current_user)
        buyer_account.quantity_coin -= quantity_coin
        buyer_account.quantity_astra += asa_received
        self.session.merge(buyer_account)

    def update_account_seller(self, seller_id_list, quantity_coin, quantity_asa):

        longest_seller_list = self.get_longest_seller(seller_id_list)
        coin_received = quantity_coin // len(longest_seller_list)
        asa_received = quantity_asa // len(longest_seller_list)

        for seller in longest_seller_list:
            user = self.get_user_by_id(seller)
            user.quantity_coin += coin_received
            user.quantity_astra -= asa_received

    def update_book_orders(self, min_price, asa_received_by_buyer):
        book_order_id_list = self.get_book_order_id_by_min_price(min_price)

        for book_order_id in book_order_id_list:
            book_order = self.get_book_order_by_id(book_order_id)

            book_order.amount_asa -= asa_received_by_buyer
            book_order.total_coins -= asa_received_by_buyer * min_price

    def delete_book_order(self, min_price):
        book_order_id_list = self.get_book_order_id_by_min_price(min_price)
        for book_order_id in book_order_id_list:
            book_order = self.get_book_order_by_id(book_order_id)
            if book_order:
                self.session.delete(book_order)

    def buy_now_trans(self, current_user, quantity_coin):
        check_balance = self.check_balance(current_user, quantity_coin)

        try:
            with self.session.begin():
                if check_balance is True:
                    min_price, quantity_asa, seller_id_list = self.get_lowest_price()
                    asa_received = quantity_coin // min_price
                    remaining_coin = quantity_coin % min_price
                    total_coin_using = quantity_coin - remaining_coin

                    self.update_account_buyer(current_user,
                                              asa_received,
                                              total_coin_using)

                    self.update_account_seller(seller_id_list,
                                               total_coin_using,
                                               asa_received)

                    self.update_book_orders(min_price,
                                            asa_received)

                    self.session.commit()
                    return asa_received, remaining_coin, min_price
                else:
                    return None

        except Exception as e:
            print(f"Error: {e}")
            self.session.rollback()

    # def buy_now_trans(self, current_user, coin_using):
    #     check_balance = self.check_balance(current_user, coin_using)

    #     try:
    #         with self.session.begin():
    #             if check_balance is True:
    #                 min_price, quantity_asa, seller_id_list = self.get_lowest_price()
    #                 asa_received = coin_using // min_price
    #                 remaining_coin = coin_using - (min_price * quantity_asa)

    #                 if remaining_coin > 0:

    #                     remain_coin = coin_using - (min_price * quantity_asa)

    #                     self.update_account_buyer(current_user,
    #                                               quantity_asa,
    #                                               min_price * quantity_asa)

    #                     self.update_account_seller(seller_id_list,
    #                                                min_price * quantity_asa,
    #                                                quantity_asa)

    #                     if asa_received >= quantity_asa:
    #                         self.delete_book_order(min_price)

    #                     # if remain_coin > 0:
    #                         min_price_next, quantity_asa_next, seller_id_list_next = self.get_lowest_price()
    #                         asa_received_next = remain_coin // min_price_next

    #                         self.update_account_buyer(current_user,
    #                                                   asa_received_next,
    #                                                   remain_coin)

    #                         self.update_account_seller(seller_id_list_next,
    #                                                    remain_coin,
    #                                                    asa_received_next)

    #                         self.update_book_orders(min_price_next,
    #                                                 asa_received_next)

    #                     my_tuple = (asa_received_next,
    #                                 min_price_next, min_price, asa_received)
    #                     print(my_tuple)
    #                     self.session.commit()
    #                     return my_tuple

    #                 self.update_account_buyer(current_user,
    #                                           asa_received,
    #                                           coin_using)

    #                 self.update_account_seller(seller_id_list,
    #                                            coin_using,
    #                                            asa_received)

    #                 self.update_book_orders(min_price,
    #                                         asa_received)

    #                 self.session.commit()
    #                 return min_price, asa_received

    #             else:
    #                 return None

    #     except Exception as e:
    #         print(f"Error: {e}")
    #         self.session.rollback()


class SellTransactions(MySqlConnect):

    def __init__(self):
        super().__init__()
        self.stock_data_layer = Stock()
        self.stock_utils = StockUtils()
        self.user_data_layer = UserData()

    def get_highest_price(self):
        lowest_price = (
            self.session.query(
                BookOrders.price_coins,
                func.sum(BookOrders.total_coins),
                func.group_concat(
                    distinct(BookOrders.user_id)),

            )
            .filter(BookOrders.taker_type == "sell")
            .group_by(BookOrders.price_coins)
            .order_by(desc(BookOrders.price_coins))
            .all()
        )
        highest_price, quantity_asaa, seller_id = lowest_price[0]
        seller_id_list = [int(user_id)
                          for user_id in seller_id.split(',') if user_id]

        quantity_asa = int(quantity_asaa)
        return highest_price, quantity_asa, seller_id_list

    def check_asa_balance(self, current_user, quantity_asa):
        return self.user_data_layer.get_user_asa(current_user) >= quantity_asa

    def get_user_by_id(self, user_id):
        user = self.session.query(User).filter_by(user_id=user_id).first()
        return user

    def get_longest_buyer(self, seller_id_list):

        sellers = self.session.query(BookOrders.user_id,
                                     func.max(BookOrders.created_at)
                                     ).filter(
            BookOrders.user_id.in_(seller_id_list)
        ).group_by(
            BookOrders.user_id
        ).having(
            func.count(BookOrders.user_id) > 1
        ).order_by(
            func.max(BookOrders.created_at).desc()
        ).all()

        buyer_list = [seller[0] for seller in sellers]
        return buyer_list

    def update_account_seller(self, current_user, asa_for_sale, quantity_coin):

        buyer_account = self.user_data_layer.get_by_name(current_user)
        buyer_account.quantity_astra -= asa_for_sale
        buyer_account.quantity_coin += quantity_coin
        self.session.merge(buyer_account)

    def update_account_buyer(self, seller_id_list, quantity_coin, quantity_asa):

        longest_buyer_list = self.get_longest_buyer(seller_id_list)
        asa_received = quantity_asa // len(longest_buyer_list)
        coin_received = quantity_coin // len(longest_buyer_list)

        for buyer in longest_buyer_list:
            user = self.get_user_by_id(buyer)
            user.quantity_astra += asa_received
            user.quantity_astra -= coin_received

    def get_book_order_by_id(self, id):
        book_order = self.session.query(
            BookOrders).filter_by(book_order_id=id).first()
        return book_order

    def get_book_order_id_by_min_price(self, price):
        results = (
            self.session.query(BookOrders.book_order_id)
            .filter(BookOrders.taker_type == 'buy')
            .filter(BookOrders.price_coins == price)
            .order_by(BookOrders.price_coins.desc())
        )
        book_order_ids = [item[0] for item in results]
        return book_order_ids

    def update_book_orders(self, highest_price, coins_received_by_seller):
        book_order_id_list = self.get_book_order_id_by_min_price(highest_price)

        for book_order_id in book_order_id_list:
            book_order = self.get_book_order_by_id(book_order_id)
            book_order.amount_asa -= coins_received_by_seller

    def sell_now_trans(self, current_user, asa_for_sale):
        check_balance = self.check_asa_balance(current_user, quantity_asa)
        try:
            with self.session.begin():
                if check_balance is True:
                    highest_price, quantity_asa, seller_id_list = self.get_highest_price()

                    coin_seller_received = highest_price * quantity_asa

                    self.update_account_seller(current_user,
                                               asa_for_sale,
                                               coin_seller_received)

                    self.update_account_seller(seller_id_list,
                                               coin_seller_received,
                                               asa_for_sale)

                    self.update_book_orders(highest_price,
                                            coin_seller_received)

                    self.session.commit()
                    return coin_seller_received, highest_price
                else:
                    return None

        except Exception as e:
            print(f"Error: {e}")
            self.session.rollback()
