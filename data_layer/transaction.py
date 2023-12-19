
from typing import List, Optional, Tuple
from data_layer.user import UserData
from data_layer.stock import Stock


class PurchaseTransaction():
    def __init__(self):
        self.user_data_layer = UserData()
        self.stock_data_layer = Stock()

    def buy_now_trans(self, buyer_id, price_coins, quantity_astra):
        buyer_valid = self.user_data_layer.get_by_id(buyer_id)
        try:
            if buyer_valid and buyer_valid.quantity_coin >= price_coins * quantity_astra:
                while True:
                    lowest_order = self.stock_data_layer.get_book_order_by_lowest_coins()
                    if not lowest_order:
                        break

                    if price_coins * quantity_astra >= lowest_order.total:

                        self.stock_data_layer.delete_book_order_by_id(
                            lowest_order.book_order_id)
                    else:

                        self.stock_data_layer.update_book_order_by_id(
                            lowest_order.book_order_id)

                    self.user_data_layer.update_account_buyer(
                        buyer_id, price_coins, quantity_astra)

                    self.user_data_layer.update_account_seller(
                        lowest_order.user_id, price_coins, quantity_astra)

                    self.stock_data_layer.add_new_buy_order(
                        buyer_id, price_coins, quantity_astra)

                    self.stock_data_layer.add_new_sell_order(
                        lowest_order.user_id, price_coins, quantity_astra)
            else:
                print("ko du coins")
        except Exception as e:
            self.stock_data_layer.rollback()
            raise

        finally:
            self.stock_data_layer.close()


a = PurchaseTransaction()

# Example usage
b = a.buy_now_trans(1, 100, 100)
print(b)
