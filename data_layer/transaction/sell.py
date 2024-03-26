import traceback
from data_layer.mysql_connect import MySqlConnect
from data_layer.table.user import UserData
from data_layer.table.book_orders import BookOrdersDL
from data_layer.table.market_trans import MarketTransactionDL
from datetime import datetime


class SellTransaction(MySqlConnect):

    def __init__(self):
        super().__init__()
        self.book_order_dl = BookOrdersDL()
        self.user_dl = UserData()
        self.market_trans_dl = MarketTransactionDL()

    def process_full_sell(self, astra_user_using, highest_price, quantity_coins,  total_astra_market, astra_spent, coins_received, current_user_id):
        astra_user_using -= total_astra_market
        astra_spent += total_astra_market
        coins_received += quantity_coins

        buyer_ids = self.book_order_dl.get_buyer_ids_and_asa_by_highest_price(highest_price
                                                                              )
        for buyer_id, amount_asa in buyer_ids:
            coin_minus = amount_asa * highest_price
            self.user_dl.update_plus_astra(buyer_id, amount_asa)
            self.market_trans_dl.add_record(highest_price,
                                            buyer_id,
                                            coin_minus,
                                            amount_asa,
                                            taker_type="bought")

        self.market_trans_dl.add_record(highest_price,
                                        current_user_id,
                                        quantity_coins,
                                        total_astra_market,
                                        taker_type="sold")

        self.book_order_dl.delete_book_order_by_highest_price(highest_price)
        return astra_user_using, astra_spent, coins_received

    def process_partial_sell(self, astra_user_using, highest_price, coins_can_received, asa_spent, coins_received, current_user_id, buyer_id_list):
        asa_spent += astra_user_using
        coins_received += coins_can_received
        buyer_ids_and_asa = self.book_order_dl.get_earliest_user_id_and_asa_by_price(highest_price,
                                                                                     buyer_id_list,
                                                                                     taker_type="buy")
        astra_plus = astra_user_using // len(buyer_ids_and_asa)
        coin = astra_plus * highest_price

        for buyer_id, asa in buyer_ids_and_asa:
            self.user_dl.update_plus_astra(buyer_id, astra_plus)
            self.market_trans_dl.add_record(highest_price,
                                            buyer_id,
                                            coin,
                                            astra_plus,
                                            taker_type="bought")

        self.market_trans_dl.add_record(highest_price,
                                        current_user_id,
                                        coins_received,
                                        astra_user_using,
                                        taker_type="sold")

        self.book_order_dl.update_by_highest_price(highest_price,
                                                   asa_spent)
        astra_user_using = 0
        return astra_user_using, asa_spent, coins_received

    def process_transactions(self, astra_user_using, current_user_id):
        coins_total_received = 0
        astra_total_spent = 0
        trans_count = 0
        transactions_list = []

        while astra_user_using > 0:
            trans_count += 1
            highest_price_data = self.book_order_dl.get_highest_price_buy()

            for highest_price, buyer_id_list, quantity_asa in highest_price_data:
                total_asa_market = quantity_asa
                if astra_user_using >= total_asa_market:
                    quantity_coins = total_asa_market * highest_price
                    astra_user_using, astra_total_spent, coins_total_received = self.process_full_sell(astra_user_using,
                                                                                                       highest_price,
                                                                                                       quantity_coins,
                                                                                                       total_asa_market,
                                                                                                       astra_total_spent,
                                                                                                       coins_total_received,
                                                                                                       current_user_id)
                    coins_can_received = quantity_coins
                    asa = astra_total_spent
                else:
                    coins_can_received = astra_user_using * highest_price
                    asa = coins_can_received // highest_price
                    astra_user_using, astra_total_spent, coins_total_received = self.process_partial_sell(astra_user_using,
                                                                                                          highest_price,
                                                                                                          coins_can_received,
                                                                                                          astra_total_spent,
                                                                                                          coins_total_received,
                                                                                                          current_user_id,
                                                                                                          buyer_id_list)
                transaction_details = {
                    'transaction': trans_count,
                    'price': highest_price,
                    'coin_received': coins_can_received,
                    'asa_spent': asa,
                    'timestamp': datetime.now()

                }
                transactions_list.append(transaction_details)
                break
        return transactions_list, coins_total_received, astra_total_spent

    def sell_now_trans(self, current_user_name, asa_user_using):
        user = self.user_dl.get_by_name(current_user_name)

        check_balance = self.user_dl.check_balance_asa(user.user_id,
                                                       asa_user_using)
        if check_balance is None:
            return None
        try:
            self.session.begin()
            transactions_list, coins_total_received, astra_total_spent = self.process_transactions(asa_user_using,
                                                                                                   user.user_id)

            self.user_dl.update_account_seller(user,
                                               coins_total_received,
                                               astra_total_spent)
            return transactions_list

        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            self.session.rollback()
            return None

    def sell_limit_trans(self, current_user_name, astra_price, asa_quantity):
        """

        sell asa -> received coins and minus asa
        1. inpu:t price_asa and asa_quantity => system calculate coins_received = price_asa * asa_quantity
        2. add new record book_order -> taker is sell 
            insert current_user_id, astra_price, asa_quantity, coins_received, 
        3. update account seller is "current_user_name" minus asa 

        """
        user = self.user_dl.get_by_name(current_user_name)
        check_balance = self.user_dl.check_balance_asa(user.user_id,
                                                       asa_quantity)
        if check_balance is None:
            return None
        try:
            with self.session.begin():
                coins_received = astra_price * asa_quantity
                self.book_order_dl.add_record_book_orders(user.user_id,
                                                          astra_price,
                                                          asa_quantity,
                                                          coins_received,
                                                          taker_type="sell"
                                                          )
            self.user_dl.update_account_sell_limit(current_user_name,
                                                   asa_quantity)
            self.session.commit()
            return astra_price, asa_quantity, coins_received

        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            self.session.rollback()
            return None
