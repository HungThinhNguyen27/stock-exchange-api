
from data_layer.mysql_connect import MySqlConnect
from sqlalchemy import func
from data_layer.table.user import UserData
from data_layer.table.book_orders import BookOrdersDL
from model.stock import MarketTransaction
from model.stock import BookOrders
from datetime import datetime


class TransUtils(MySqlConnect):
    def __init__(self):
        super().__init__()
        self.book_order_dl = BookOrdersDL()
        self.user_dl = UserData()

    def get_by_name(self, user_name):
        return self.user_dl.get_by_name(user_name)

    def get_book_order_by_id(self, id):
        return self.book_order_dl.get_book_orders_id(id)

    def get_book_order_by_user_id(self, id):
        return self.book_order_dl.get_book_order_by_user_id(id)

    def get_earliest_user_id_and_asa_by_price(self, id, min_price, taker_type):
        return self.book_order_dl.get_earliest_user_id_and_asa_by_price/(id, min_price, taker_type)

    def get_seller_ids_and_asa_by_highest_price(self, min_price):
        return self.book_order_dl.get_seller_ids_and_asa_by_highest_price(min_price
                                                                          )

    def get_buyer_ids_and_asa_by_highest_price(self, highest_price):
        return self.book_order_dl.get_buyer_ids_and_asa_by_highest_price(highest_price
                                                                         )

    def get_lowest_price_sell(self):
        return self.book_order_dl.get_lowest_price_sell()

    def get_highest_price_buy(self):
        return self.book_order_dl.get_highest_price_buy()

    def check_balance_coins(self, current_user, coins_using):
        self.user_dl.get_user_coins(current_user) >= coins_using
        return True

    def check_balance_asa(self, current_user, asa_using):
        self.user_dl.get_user_asa(current_user) >= asa_using
        return True

    def update_account_buyer(self, current_user, asa_received, quantity_coin):
        account = self.user_dl.get_by_name(current_user)
        account.quantity_coin -= quantity_coin
        account.quantity_astra += asa_received
        self.session.merge(account)

    def update_account_seller(self, current_user, coin_received, quantity_asa):
        account = self.user_dl.get_by_name(current_user)
        account.quantity_coin += coin_received
        account.quantity_astra -= quantity_asa
        self.session.merge(account)

    def update_coins_user(self, id, coin_minus):

        user = self.user_dl.get_by_id(id)
        user.quantity_coin += coin_minus

    def update_asa_user(self, id, asa_received):

        user = self.user_dl.get_by_id(id)
        user.quantity_astra += asa_received

    def update_account_buy_limit(self, current_user, quantity_coins):
        account = self.user_dl.get_by_name(current_user)
        account.quantity_coin -= quantity_coins

    def update_account_sell_limit(self, current_user, quantity_asa):
        account = self.user_dl.get_by_name(current_user)
        account.quantity_astra -= quantity_asa

    def update_book_orders(self, min_price, asa_received_by_buyer):

        book_order_id_list = self.book_order_dl.get_book_order_id_by_min_price(
            min_price)
        book_order_earliest_list_id = self.book_order_dl.get_book_order_earliest(book_order_id_list
                                                                                 )
        asa_minus = asa_received_by_buyer // len(book_order_earliest_list_id
                                                 )
        for book_order_id in book_order_earliest_list_id:
            book_order = self.get_book_order_by_id(book_order_id)
            book_order.amount_asa -= asa_minus

    def delete_book_order_by_min_price(self, min_price):
        book_order_id_list = self.book_order_dl.get_book_order_id_by_min_price(min_price
                                                                               )
        for book_order_id in book_order_id_list:
            book_order = self.get_book_order_by_id(book_order_id)
            if book_order:
                self.session.delete(book_order)

    def delete_book_order_by_highest_price(self, highest_price):
        book_order_id_list = self.book_order_dl.get_book_order_id_by_highest_price(highest_price
                                                                                   )
        for book_order_id in book_order_id_list:
            book_order = self.get_book_order_by_id(book_order_id)
            if book_order:
                self.session.delete(book_order)

    def calculate_coin_minus(self, sell_all, coin_user_used, price, amount_asa, seller_count):
        if sell_all:
            return price * amount_asa
        else:
            return coin_user_used // seller_count if seller_count > 0 else 0

    def calculate_asa_minus(self, sell_all, coin_user_used, price, amount_asa, seller_count):
        if sell_all:
            return amount_asa
        else:
            asa_quantity = coin_user_used // price
            return asa_quantity // seller_count if seller_count > 0 else 0

    def add_record_trans_market(self, price, buyer_id, coin_used, asa_remain, taker_type):

        self.session.add(MarketTransaction(
            user_id=buyer_id,
            quantity_coin=coin_used,
            quantity_astra=asa_remain,
            transaction_date=datetime.now(),
            taker_type=taker_type,
            price=price
        ))

    def add_record_book_orders(self, user_id, price, amount_asa, total_coins, taker_type):
        market = "asa"
        self.session.add(BookOrders(
            user_id=user_id,
            price_coins=price,
            amount_asa=amount_asa,
            total_coins=total_coins,
            market=market,
            created_at=datetime.now(),
            taker_type=taker_type
        )
        )
