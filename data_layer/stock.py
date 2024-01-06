
from model.stock import StockPrice, BookOrders, MarketTransaction, Orders
from typing import List, Optional, Tuple
from data_layer.mysql_connect import MySqlConnect
from sqlalchemy.orm import aliased
from sqlalchemy import asc
from sqlalchemy import func


class Stock(MySqlConnect):

    def get_stock_data(self) -> List[StockPrice]:
        stock_data = self.session.query(StockPrice).all()
        return stock_data

    def paging_book_orders(self, offset, per_page) -> List[BookOrders]:
        return self.session.query(BookOrders).limit(per_page).offset(offset).all()

    def get_market_transaction_data(self) -> List[MarketTransaction]:
        return self.session.query(MarketTransaction).all()

    def get_book_orders_id(self, id) -> List[BookOrders]:
        existing_book_order = self.session.query(BookOrders).filter_by(
            book_order_id=id).first()
        return existing_book_order

    def add(self, data) -> None:
        self.session.add(data)
        self.commit()

    def commit(self) -> None:
        self.session.commit()

    def get_book_order_asc(self):
        return self.session.query(BookOrders).order_by(asc(BookOrders.price)).all()

    def sum_total_by_taker_type(self, taker_type, offset, limit):
        result = (
            self.session.query(BookOrders.price, func.sum(
                BookOrders.total).label('total'))
            .filter(BookOrders.taker_type == taker_type)
            .group_by(BookOrders.price)
            .order_by(asc(BookOrders.price))
            .offset(offset)
            .limit(limit)
            .all()
        )

        return result

    def count_distinct_prices(self, taker_type):
        query = (
            self.session.query(func.count(func.distinct(BookOrders.price)))
            .filter(BookOrders.taker_type == taker_type)
        )

        book_order_count = query.scalar()

        return book_order_count


a = Stock()
b = a.get_stock_data()

df = pd.DataFrame([(i.time_stamp, i.open_price, i.close_price, i.high_price, i.low_price, i.volume) for i in b],
                  columns=['time_stamp', 'open_price', 'close_price', 'high_price', 'low_price', 'volume'])

# Chuyển cột time_stamp sang kiểu datetime
df['time_stamp'] = pd.to_datetime(df['time_stamp'])

# Xác định giờ mở và đóng cửa chính thức
official_open_time = datetime.strptime('09:30', '%H:%M').time()
official_close_time = datetime.strptime('16:00', '%H:%M').time()

# Lọc dữ liệu theo giờ mở và đóng cửa chính thức
df = df[(df['time_stamp'].dt.time >= official_open_time) &
        (df['time_stamp'].dt.time <= official_close_time)]

# Nhóm dữ liệu theo ngày và tính toán giá trị giá mở, đóng, cao, thấp trung bình
grouped_data = df.groupby(df['time_stamp'].dt.date).agg({
    'open_price': 'mean',
    'close_price': 'mean',
    'high_price': 'mean',
    'low_price': 'mean',
    'volume': 'sum'
}).reset_index()

# Hiển thị kết quả
print(grouped_data)
