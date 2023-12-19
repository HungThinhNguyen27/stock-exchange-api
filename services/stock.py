
from data_layer.stock import Stock
from utils.crawl_stock_data import CrawlData
from model.stock import BookOrders, StockPrice
from data_layer.user import UserData
from datetime import datetime


class StockService:

    def __init__(self) -> None:
        self.stock_data_layers = Stock()
        self.user_data_layers = UserData()

    def get_stock_candles(self):
        stock_list = self.stock_data_layers.get_stock_data()
        return stock_list

    def get_book_orders(self):
        return self.stock_data_layers.get_book_orders_data()

    def get_market_trans(self):
        return self.stock_data_layers.get_market_transaction_data()

    # def buy_stock_now(self, user_id, coins_input):
    #     user = self.user_data_layers.get_by_id(user_id)

    #     # Kiểm tra xem tài khoản có đủ số dư không
    #     if user.quantity_coin >= coins_input:

    #         # kiểm tra xem có lệnh bán ASA nào trên sổ lệnh với giá thấp nhất
    #         #

    #         buy_transaction = BookOrders(user_id=user_id,
    #                                      price=coins_input,
    #                                      amount=a,
    #                                      total=coins_input * a,
    #                                      market="astra",
    #                                      created_at=datetime.now(),
    #                                      taker_type="buy"
    #                                      )


class CrawlDataStockService:

    def __init__(self) -> None:
        self.stock = Stock()
        self.crawl_data = CrawlData()

    def crawl_book_orders_data(self):
        book_order_data_list = self.crawl_data.crawl_book_order()

        for book_order_data in book_order_data_list:

            created_at = self.crawl_data.change_timestamp(
                book_order_data.get('created_at'))

            check_dup = self.crawl_data.check_book_order_id_dup(
                book_order_data.get('id'))

            if check_dup:
                print("Duplicated Post!")
            else:
                book_order_entity = BookOrders(
                    book_order_id=book_order_data.get('id'),
                    user_id=None,
                    price=book_order_data.get('price'),
                    amount=book_order_data.get('amount'),
                    total=book_order_data.get('total'),
                    market=book_order_data.get('market'),
                    created_at=created_at,
                    taker_type=book_order_data.get('taker_type')
                )
                self.stock.add(book_order_entity)

    def crawl_stock_price_data(self):
        stock_price_data_list = self.crawl_data.crawl_stock_price()

        for stock_price_data in stock_price_data_list:
            created_at = self.crawl_data.change_timestamp(
                stock_price_data.get('time_stamp'))

            stock_entity = StockPrice(
                time_stamp=created_at,
                open_price=stock_price_data.get('open_price'),
                close_price=stock_price_data.get('close_price'),
                high_price=stock_price_data.get('high_price'),
                low_price=stock_price_data.get('low_price'),
                volume=stock_price_data.get('volume')
            )
            self.stock.add(stock_entity)
