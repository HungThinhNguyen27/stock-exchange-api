import traceback

from data_layer.transaction.utils import TransUtils


class SellTransaction(TransUtils):

    def sell_now_trans(self, current_user_name, asa_user_using):
        check_balance = self.check_balance_asa(current_user_name,
                                               asa_user_using)
        current_user_id = self.get_by_name(current_user_name)
        if not check_balance:
            return None
        try:
            with self.session.begin():
                coins_received = 0
                asa_spent = 0
                while asa_user_using > 0:
                    highest_price_data = self.get_highest_price_buy()

                    for highest_price, buyer_ids, quantity_asa_market in highest_price_data:
                        coins_obtained = asa_user_using // highest_price
                        if asa_user_using >= quantity_asa_market:
                            asa_user_using -= quantity_asa_market
                            asa_spent += quantity_asa_market
                            coins_received += coins_obtained
                            buyer_ids_and_asa = self.get_buyer_ids_and_asa_by_highest_price(
                                highest_price)

                            for buyer_id, asa in buyer_ids_and_asa:
                                plus_asa_for_buyer = asa
                                minus_coins_for_buyer = plus_asa_for_buyer // highest_price
                                self.update_asa_for_buyer(
                                    buyer_id, plus_asa_for_buyer)
                                self.add_record_trans_market(highest_price,
                                                             buyer_id,
                                                             minus_coins_for_buyer,
                                                             plus_asa_for_buyer,
                                                             taker_type="buy")

                            self.add_record_trans_market(highest_price,
                                                         current_user_id,
                                                         coins_received,
                                                         quantity_asa_market,
                                                         taker_type="sell")
                            self.delete_book_order_by_highest_price(
                                highest_price)
                        else:
                            asa_spent += asa_user_using
                            coins_received += coins_obtained
                            buyer_ids_and_asa = self.get_earliest_user_id_and_asa_by_price(highest_price,
                                                                                           buyer_ids,
                                                                                           taker_type="buy")
                            buyer_ids = [item[0]for item in buyer_ids_and_asa]
                            asa_plus = asa_user_using // len(buyer_ids)
                            coin = asa_plus * highest_price

                            for buyer_id, amount_asa in buyer_ids_and_asa:
                                self.update_asa_user(buyer_id, asa_plus)
                                self.add_record_trans_market(highest_price,
                                                             buyer_id,
                                                             coin,
                                                             asa_plus,
                                                             taker_type="sell")
                            self.add_record_trans_market(highest_price,
                                                         current_user_id,
                                                         coins_received,
                                                         asa_spent,
                                                         taker_type="buy")
                            asa_user_using = 0
                            break
                    self.update_account_seller(current_user_name,
                                               coins_received,
                                               asa_spent)
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            self.session.rollback()
            return None
        finally:
            self.session.close()

    def sell_limit_trans(self, current_user_name, astra_price, asa_quantity):
        """

        sell asa -> received coins and minus asa
        1. inpu:t price_asa and asa_quantity => system calculate coins_received = price_asa * asa_quantity
        2. add new record book_order -> taker is sell 
            insert current_user_id, astra_price, asa_quantity, coins_received, 
        3. update account seller is "current_user_name" minus asa 

        """
        check_balance = self.check_balance_asa(current_user_name,
                                               asa_quantity)
        current_user_id = self.get_by_name(current_user_name)
        if not check_balance:
            return None
        try:
            with self.session.begin():
                coins_received = astra_price * asa_quantity
                self.add_record_book_orders(current_user_id,
                                            astra_price,
                                            asa_quantity,
                                            coins_received,
                                            taker_type="sell"
                                            )
            self.update_account_sell_limit(current_user_name,
                                           asa_quantity)
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            self.session.rollback()
            return None
        finally:
            self.session.close()
