from data_layer.mysql_connect import MySqlConnect
from data_layer.table.book_orders import BookOrdersDL
from data_layer.table.user import UserData
from data_layer.table.market_trans import MarketTransactionDL
from datetime import datetime


class Exchange(MySqlConnect):

    def __init__(self, user_id, value, astra_price, taker_type) -> None:
        super().__init__()
        self.BookOrdersDL = BookOrdersDL()
        self.UserData = UserData()
        self.MarketTransactionDL = MarketTransactionDL()
        self.user_id = user_id
        self.value = value
        self.astra_price = astra_price
        self.taker_type = taker_type

    def transaction_limit(self):
        try:
            self.session.begin()

            if self.taker_type == "buy":
                value_reived = self.value // self.astra_price
            else:  # taker_type == "sell"
                value_reived = self.value * self.astra_price

            self.BookOrdersDL.add_record_book_orders(self.user_id,
                                                     self.astra_price,
                                                     value_reived,
                                                     self.value,
                                                     self.taker_type)

            self.UserData.update_balance_traders_trans_limit(self.user_id,
                                                             self.value,
                                                             self.taker_type)

            if self.taker_type == "buy":
                return {
                    "Astra Price": self.astra_price,
                    "The number of Coins you used": self.value,
                    "Amount of Asa will receive": value_reived, }
            else:
                return {
                    "Astra Price": self.astra_price,
                    "The number of Astra you used":  self.value,
                    "Amount of Coins will receive": value_reived, }

        except Exception as e:
            print(f"Error: {e}")
            self.session.rollback()
            return None

    def transaction_now(self):
        trans_count = 0
        total_spent = 0
        total_received = 0
        transactions_list = []
        try:
            self.session.begin()
            while self.value > 0:
                trans_count += 1
                taker_type = "buy" if self.taker_type == "sell" else "sell"
                price_data = self.BookOrdersDL.get_price(taker_type)
                for price, user_id_list, quantity_astra in price_data:
                    if self.taker_type == "buy":
                        asa_can_buy = min(self.value // price,
                                          quantity_astra)
                    if self.taker_type == "sell":
                        total_market = quantity_astra  # total astra in market
                        volume = total_market * price  # quantity coins
                    else:
                        total_market = price * quantity_astra  # total coins in market
                        volume = quantity_astra  # quantity astra

                    if self.value >= total_market:
                        self.value, total_spent, total_received = self.process_trans_full(self.value,
                                                                                          price,
                                                                                          volume,
                                                                                          total_market,
                                                                                          total_spent,
                                                                                          total_received,
                                                                                          self.user_id)
                        coins = volume if self.taker_type == "sell" else total_spent
                        astra = total_spent if self.taker_type == "sell" else total_received
                    else:
                        coins = self.value * price if self.taker_type == "sell" else self.value
                        astra = coins // price

                        self.value, total_spent, total_received = self.process_trans_partial(self.value,
                                                                                             price,
                                                                                             asa_can_buy if self.taker_type == "buy" else coins,
                                                                                             total_spent,
                                                                                             total_received,
                                                                                             user_id_list)
                transaction_details = {
                    'transaction': trans_count,
                    'price': price,
                    'coin_spent': coins,
                    'asa_received': astra,
                    'timestamp': datetime.now()}
                transactions_list.append(transaction_details)
            self.UserData.update_balance_traders_trans_now(self.user_id,
                                                           total_received,
                                                           total_spent,
                                                           self.taker_type)
            return transactions_list

        except Exception as e:
            print(f"Error: {e}")
            self.session.rollback()
            return None

    def process_trans_full(self, value_user_using, price, volume, total_market, spent, received, current_user_id):
        value_user_using -= total_market
        spent += total_market
        received += volume

        user_ids = self.BookOrdersDL.get_user_ids_and_asa_by_min_price(price,
                                                                       self.taker_type)
        for id, amount_asa in user_ids:
            coin_plus = price * amount_asa

            self.UserData.update_balance_buyers_or_sellers(id,
                                                           coin_plus,
                                                           self.taker_type)

            self.MarketTransactionDL.add_record(price,
                                                id,
                                                coin_plus,
                                                amount_asa,
                                                taker_type="sold" if self.taker_type == "buy" else "bought")

        self.MarketTransactionDL.add_record(price,
                                            current_user_id,
                                            total_market,
                                            volume,
                                            taker_type="bought" if self.taker_type == "buy" else "sold")

        self.BookOrdersDL.delete_book_order_by_price(price, self.taker_type)
        return value_user_using, spent, received

    def process_trans_partial(self, value_user_using, price, value_received, spent, received, user_id_list):
        spent += value_user_using
        received += value_received
        user_ids = self.BookOrdersDL.get_earliest_user_id_and_asa_by_price(price,
                                                                           user_id_list,
                                                                           taker_type='sell' if self.taker_type == "buy" else 'buy')

        value_plus = value_user_using // len(user_ids)
        asa = value_plus // price
        coin = value_plus * price

        for id, _ in user_ids:

            self.UserData.update_balance_buyers_or_sellers(id,  # plus value(coins/astra) for seller if you buy and .....
                                                           value_plus,
                                                           taker_type='sell' if self.taker_type == "buy" else 'buy')

            self.MarketTransactionDL.add_record(price,
                                                id,
                                                value_plus if self.taker_type == "buy" else coin,
                                                asa if self.taker_type == "buy" else value_plus,
                                                taker_type='sold' if self.taker_type == "buy" else 'bought')

        self.MarketTransactionDL.add_record(price,
                                            self.user_id,
                                            value_user_using if self.taker_type == "buy" else received,
                                            received if self.taker_type == "buy" else value_user_using,
                                            taker_type='bought' if self.taker_type == "buy" else 'sold')

        self.BookOrdersDL.update_minus_astra_by_min_price(price,
                                                          value_received if self.taker_type == "buy" else spent,
                                                          taker_type="sell" if self.taker_type == "buy" else "buy")
        value_user_using = 0
        return value_user_using, spent, received
