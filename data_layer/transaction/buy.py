import traceback
from data_layer.mysql_connect import MySqlConnect
from data_layer.table.user import UserData
from data_layer.table.book_orders import BookOrdersDL
from data_layer.table.market_trans import MarketTransactionDL

from datetime import datetime


class BuyTransaction(MySqlConnect):
    def __init__(self):
        super().__init__()
        self.book_order_dl = BookOrdersDL()
        self.user_dl = UserData()
        self.market_trans_dl = MarketTransactionDL()

    def calculate_market_details(self, coin_user_using, min_price, quantity_asa):
        asa_can_buy = min(coin_user_using // min_price, quantity_asa)
        total_coin_market = min_price * quantity_asa
        return asa_can_buy, total_coin_market

    def process_full_buy(self, coin_user_using, min_price, quantity_asa, total_coin_market, coin_spent, asa_received, current_user_id):
        coin_user_using -= total_coin_market
        coin_spent += total_coin_market
        asa_received += quantity_asa

        seller_ids = self.book_order_dl.get_seller_ids_and_asa_by_min_price(min_price
                                                                            )
        for seller_id, amount_asa in seller_ids:
            coin_plus = min_price * amount_asa
            self.user_dl.update_plus_coin(seller_id, coin_plus)
            self.market_trans_dl.add_record(min_price,
                                            seller_id,
                                            coin_plus,
                                            amount_asa,
                                            taker_type="sold")

        self.market_trans_dl.add_record(min_price,
                                        current_user_id,
                                        total_coin_market,
                                        quantity_asa,
                                        taker_type="bought")

        self.book_order_dl.delete_book_order_by_min_price(min_price)
        return coin_user_using, coin_spent, asa_received

    def process_partial_buy(self, coin_user_using, min_price, asa_can_buy, coin_spent, asa_received, current_user_id, seller_id_list):
        coin_spent += coin_user_using
        asa_received += asa_can_buy
        seller_ids_and_asa = self.book_order_dl.get_earliest_user_id_and_asa_by_price(min_price,
                                                                                      seller_id_list,
                                                                                      taker_type="sell")
        coin_plus = coin_user_using // len(seller_ids_and_asa)
        asa = coin_plus // min_price

        for seller_id, _ in seller_ids_and_asa:
            self.user_dl.update_plus_coin(seller_id, coin_plus)
            self.market_trans_dl.add_record(min_price,
                                            seller_id,
                                            coin_plus,
                                            asa,
                                            taker_type="sold")

        self.market_trans_dl.add_record(min_price,
                                        current_user_id,
                                        coin_user_using,
                                        asa_can_buy,
                                        taker_type="bought")

        self.book_order_dl.update_by_min_price(min_price, asa_can_buy)
        coin_user_using = 0
        return coin_user_using, coin_spent, asa_received

    def process_transactions(self, coin_user_using, current_user_id):
        asa_total_received = 0
        coin_total_spent = 0
        trans_count = 0
        transactions_list = []
        while coin_user_using > 0:

            trans_count += 1
            lowest_price_data = self.book_order_dl.get_lowest_price_sell()

            for min_prices, seller_id_list, quantity_asa in lowest_price_data:
                asa_can_buy, total_coin_market = self.calculate_market_details(coin_user_using,
                                                                               min_prices,
                                                                               quantity_asa)
                if coin_user_using >= total_coin_market:
                    coin_user_using, coin_total_spent, asa_total_received = self.process_full_buy(coin_user_using,
                                                                                                  min_prices,
                                                                                                  quantity_asa,
                                                                                                  total_coin_market,
                                                                                                  coin_total_spent,
                                                                                                  asa_total_received,
                                                                                                  current_user_id)
                    coins = coin_total_spent
                    asa = asa_total_received
                else:
                    coins = coin_user_using
                    asa = coins // min_prices
                    coin_user_using, coin_total_spent, asa_total_received = self.process_partial_buy(coin_user_using,
                                                                                                     min_prices,
                                                                                                     asa_can_buy,
                                                                                                     coin_total_spent,
                                                                                                     asa_total_received,
                                                                                                     current_user_id,
                                                                                                     seller_id_list)

                transaction_details = {
                    'transaction': trans_count,
                    'price': min_prices,
                    'coin_spent': coins,
                    'asa_received': asa,
                    'timestamp': datetime.now()

                }
                transactions_list.append(transaction_details)
                break

        return transactions_list, asa_total_received, coin_total_spent

    def buy_now_trans(self, current_user_name, coin_user_using):
        user = self.user_dl.get_by_name(current_user_name)

        check_balance = self.user_dl.check_balance_coins(user.user_id,
                                                         coin_user_using)

        if check_balance is None:
            return None
        try:
            self.session.begin()

            transactions_list, asa_received_total, coin_spent_total = self.process_transactions(coin_user_using,
                                                                                                user.user_id)
            self.user_dl.update_account_buyer(user,
                                              asa_received_total,
                                              coin_spent_total)
            return transactions_list

        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            self.session.rollback()
            return None

    def buy_limit_trans(self, current_user_name, astra_price, coins_quantity):
        """

        buy asa -> received asa and minus coins
        1. input price_asa and coin_using => system calculate asa_quantity_received = price_asa * coin_using

        2.  add new record book_order -> taker is buy 
            insert current_user_id, astra_price, asa_quantity_received, coins_quantity,  

        3. update account buyer is "current_user_name" minus coins 

        """
        user = self.user_dl.get_by_name(current_user_name)
        check_balance = self.user_dl.check_balance_coins(user.user_id,
                                                         coins_quantity)
        if check_balance is None:
            return None
        try:
            self.session.begin()
            asa_quantity_received = coins_quantity // astra_price
            self.book_order_dl.add_record_book_orders(user.user_id,
                                                      astra_price,
                                                      asa_quantity_received,
                                                      coins_quantity,
                                                      taker_type="buy"
                                                      )
            self.user_dl.update_account_buy_limit(current_user_name,
                                                  coins_quantity)

            self.session.commit()
            return astra_price, coins_quantity, asa_quantity_received

        except Exception as e:
            print(f"Error: {e}")
            self.session.rollback()
            return None
