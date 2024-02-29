import traceback

from data_layer.transaction.utils import TransUtils


class BuyTransaction(TransUtils):

    def buy_now_trans(self, current_user_name, coin_user_using):
        check_balance = self.check_balance_coins(current_user_name,
                                                 coin_user_using)
        current_user_id = self.get_by_name(current_user_name)
        if not check_balance:
            return None
        try:
            self.session.begin()
            asa_received = 0
            coin_spent = 0

            while coin_user_using > 0:
                lowest_price_data = self.get_lowest_price_sell()

                for min_price, seller_id_list, quantity_asa in lowest_price_data:
                    asa_can_buy = coin_user_using // min_price
                    total_coin_market = min_price * quantity_asa
                    if coin_user_using >= total_coin_market:
                        coin_user_using -= total_coin_market
                        coin_spent += total_coin_market
                        asa_received += quantity_asa
                        seller_ids = self.get_seller_ids_and_asa_by_highest_price(min_price
                                                                                  )

                        for seller_id, amount_asa in seller_ids:
                            coin_plus = min_price * amount_asa
                            self.update_coins_user(seller_id,
                                                   coin_plus)
                            self.add_record_trans_market(min_price,
                                                         seller_id,
                                                         coin_plus,
                                                         amount_asa,
                                                         taker_type="sell")

                        self.add_record_trans_market(min_price,
                                                     current_user_id,
                                                     total_coin_market,
                                                     quantity_asa,
                                                     taker_type="buy")
                        self.delete_book_order_by_min_price(min_price)
                    else:
                        coin_spent += coin_user_using
                        asa_received += asa_can_buy
                        seller_ids_and_asa = self.get_earliest_user_id_and_asa_by_price(min_price,
                                                                                        seller_id_list,
                                                                                        taker_type="sell")
                        seller_ids = [item[0]
                                      for item in seller_ids_and_asa]

                        coin_plus = coin_user_using // len(seller_ids
                                                           )
                        asa = coin_plus // min_price

                        for seller_id, amount_asa in seller_ids_and_asa:
                            self.update_coins_user(seller_id,
                                                   coin_plus)
                            self.add_record_trans_market(min_price,
                                                         seller_id,
                                                         coin_plus,
                                                         asa,
                                                         taker_type="sell")

                        self.add_record_trans_market(min_price,
                                                     current_user_id,
                                                     coin_user_using,
                                                     asa_can_buy,
                                                     taker_type="buy")

                        self.update_book_orders(min_price, asa_can_buy)
                        coin_user_using = 0
                        break

                    self.update_account_buyer(current_user_name,
                                              asa_received,
                                              coin_spent)
                    self.session.commit()

                return asa_received, coin_spent
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            self.session.rollback()
            return None
        finally:
            self.session.close()

    def buy_limit_trans(self, current_user_name, astra_price, coins_quantity):
        """

        buy asa -> received asa and minus coins
        1. input price_asa and coin_using => system calculate asa_quantity_received = price_asa * coin_using

        2.  add new record book_order -> taker is buy 
            insert current_user_id, astra_price, asa_quantity_received, coins_quantity,  

        3. update account buyer is "current_user_name" minus coins 

        """

        check_balance = self.check_balance_coins(current_user_name,
                                                 coins_quantity)
        if not check_balance:
            return None
        current_user_id = self.get_by_name(current_user_name)
        try:
            self.session.begin()
            asa_quantity_received = coins_quantity // astra_price
            self.add_record_book_orders(current_user_id,
                                        astra_price,
                                        asa_quantity_received,
                                        coins_quantity,
                                        taker_type="buy"
                                        )
            self.update_account_buy_limit(current_user_name,
                                          coins_quantity)

            self.session.commit()

            return astra_price, coins_quantity, asa_quantity_received

        except Exception as e:
            print(f"Error: {e}")
            self.session.rollback()
            return None
