
# from data_layer.user import UserData
# from data_layer.stock import Stock
from sqlalchemy import and_
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
        lowest_price_info = (
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
        lowest_price_data = []
        for price, quantity_asaa, seller_id in lowest_price_info:

            min_price = int(price)
            quantity_asa = int(quantity_asaa)
            seller_id_list = [int(seller_id)
                              for seller_id in seller_id.split(',') if seller_id]

            lowest_price_data.append((min_price, seller_id_list, quantity_asa))
        return lowest_price_data

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

    def get_earliest_seller(self, min_price, seller_id_list):

        earliest_date_subq = self.session.query(
            func.min(BookOrders.created_at).label('earliest_date')
        ).filter(
            BookOrders.price_coins == min_price
        ).subquery()

        earliest_sellers = self.session.query(
            BookOrders.user_id
        ).filter(
            BookOrders.user_id.in_(seller_id_list),
            BookOrders.price_coins == min_price,
            BookOrders.created_at == earliest_date_subq.c.earliest_date
        ).order_by(
            BookOrders.user_id
        ).all()

        user_id_list = [user_id for (user_id,) in earliest_sellers]
        return user_id_list

    def get_seller_by_min_price(self, min_price):

        # Lấy user_id của những người bán có giá thấp nhất
        earliest_sellers = self.session.query(
            BookOrders.user_id
        ).filter(
            BookOrders.price_coins == min_price
        ).group_by(
            BookOrders.user_id
        ).all()

        user_id_list = [user_id for (user_id,) in earliest_sellers]
        return user_id_list

    def get_book_order_earliest(self, book_order_id_list):

        earliest_date_subq = self.session.query(
            func.min(BookOrders.created_at).label('earliest_date')
        ).filter(
            BookOrders.book_order_id.in_(book_order_id_list)
        ).subquery()

        earliest_book_orders = self.session.query(
            BookOrders.book_order_id,
            BookOrders.created_at
        ).filter(
            and_(
                BookOrders.book_order_id.in_(book_order_id_list),
                BookOrders.created_at == earliest_date_subq.c.earliest_date
            )
        ).order_by(
            BookOrders.book_order_id
        ).all()

        book_order_list = [book_order[0]
                           for book_order in earliest_book_orders]
        return book_order_list

    def update_account_buyer(self, current_user, asa_received, quantity_coin):
        buyer_account = self.user_data_layer.get_by_name(current_user)
        buyer_account.quantity_coin -= quantity_coin
        buyer_account.quantity_astra += asa_received
        self.session.merge(buyer_account)

    def update_coins_earliest_seller(self, min_price, seller_id_list, quantity_coin):

        seller_earliest_list_id = self.get_earliest_seller(min_price,
                                                           seller_id_list)

        coin_minus = quantity_coin // len(seller_earliest_list_id)

        for seller_id in seller_earliest_list_id:

            user = self.get_user_by_id(seller_id)
            user.quantity_coin += coin_minus

    def update_coins_seller_min_price(self, min_price, quantity_coin):

        seller_id_list = self.get_seller_by_min_price(min_price)

        coin_minus = quantity_coin // len(seller_id_list)

        for seller_id in seller_id_list:

            user = self.get_user_by_id(seller_id)
            print(user)
            user.quantity_coin += coin_minus

    def update_book_orders(self, min_price, asa_received_by_buyer):

        book_order_id_list = self.get_book_order_id_by_min_price(min_price)
        book_order_earliest_list_id = self.get_book_order_earliest(book_order_id_list
                                                                   )
        asa_minus = asa_received_by_buyer // len(book_order_earliest_list_id
                                                 )
        for book_order_id in book_order_earliest_list_id:
            book_order = self.get_book_order_by_id(book_order_id)
            book_order.amount_asa -= asa_minus

    def delete_book_order(self, min_price):
        book_order_id_list = self.get_book_order_id_by_min_price(min_price)
        for book_order_id in book_order_id_list:
            book_order = self.get_book_order_by_id(book_order_id)
            if book_order:
                self.session.delete(book_order)

    def buy_now_trans(self, current_user, coin_user_using):
        check_balance = self.check_balance(current_user, coin_user_using)
        if not check_balance:
            return None

        try:
            with self.session.begin():
                asa_received = 0
                coin_spent = 0
                index = 0
                try:

                    while coin_user_using > 0:
                        lowest_price_data = self.get_lowest_price()
                        min_price, seller_id_list, quantity_asa = lowest_price_data[index]
                        index += 1
                        print("min_price", min_price)
                        asa_can_buy = coin_user_using // min_price
                        # print("asa_can_buy", asa_can_buy)
                        total_coin_market = min_price * quantity_asa
                        print("total_coin_market", total_coin_market)

                        if coin_user_using >= total_coin_market:
                            coin_user_using = coin_user_using - total_coin_market
                            print("coin remaing", coin_user_using)
                            coin_spent += total_coin_market
                            print("coin_user_using_1", coin_spent)
                            asa_received += quantity_asa
                            self.update_coins_seller_min_price(min_price,
                                                               total_coin_market)
                            # self.delete_book_order(min_price)

                        else:
                            coin_spent += coin_user_using
                            print("coin_user_using_2", coin_user_using)
                            asa_received += asa_can_buy
                            self.update_coins_earliest_seller(min_price, seller_id_list,
                                                              coin_user_using)
                            self.update_book_orders(min_price, asa_can_buy)
                            coin_user_using = coin_user_using - coin_user_using

                        print("coin_spent_total", coin_spent)

                    self.update_account_buyer(current_user,
                                              asa_received,
                                              coin_spent)
                    self.session.commit()

                    return asa_received, coin_spent, coin_user_using
                except:
                    # Rollback the transaction explicitly on exception
                    self.session.rollback()
                    raise

        except Exception as e:
            print(f"Error: {e}")
            self.session.rollback()
            return None


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


# case 1
# coin using -> 20000  và + 20000 coin đó cho user 4 và user 3
# xoá lệnh bán của user 4 và 3
# còn 2000 coins sẽ mua price 19 được 105 asa + 2000coins cho user 5


# coin 2513 và asa 495
# tính remaing coin để maatch với lệnh mua tiếp theo
# tỏng asa nhận được là 1105 coins
# update_coins_seller(self, min_price, seller_id_list, quantity_coin):

av = BuyTransaction()
c = [25, 26, 27, 28, 29]
d = [3, 4, 5]
b = av.get_seller_by_min_price(20)
user = av.get_user_by_id(b)


# zz = a(1)


# # Gọi hàm a với formatted_lowest_price_info
# lowest_price_info = av.get_lowest_price()


# def transform_output(output):
#     result = []
#     for item in output:
#         price_coins, amount_asa, user_ids = item
#         user_ids_list = [int(user_id) for user_id in user_ids.split(',')]
#         result.append((price_coins, int(amount_asa), user_ids_list))
#     return result


# def aac(coin_user_using):
#     index = 0
#     asa_received = 0
#     coin_spent = 0

#     while coin_user_using > 0:
#         lowest_price_data = av.get_lowest_price()
#         min_price, seller_id_list, quantity_asa = lowest_price_data[index]
#         index += 1
#         print("min_price", min_price)
#         asa_can_buy = coin_user_using // min_price
#         total_coin_market = min_price * quantity_asa
#         print("total_coin_market", total_coin_market)
#         if coin_user_using >= total_coin_market:
#             coin_user_using = coin_user_using - total_coin_market
#             print("coin_user_using_1", coin_user_using)
#             coin_spent += total_coin_market
#             asa_received += quantity_asa
#         else:
#             coin_spent += coin_user_using
#             print("coin_user_using_2", coin_user_using)
#             coin_user_using = coin_user_using - coin_user_using
#             asa_received += asa_can_buy

#     return min_price


# acxz = aac(10000)
# print(acxz)
