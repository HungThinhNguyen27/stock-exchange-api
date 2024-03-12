
from model.stock import BookOrders
from typing import List
from data_layer.mysql_connect import MySqlConnect
from sqlalchemy import asc, func, distinct, and_, desc
from datetime import datetime


class BookOrdersDL(MySqlConnect):

    def get_asc_price(self):
        return self.session.query(BookOrders).order_by(asc(BookOrders.price_coins)).all()

    def paging(self, offset, per_page) -> List[BookOrders]:
        return self.session.query(BookOrders).limit(per_page).offset(offset).all()

    def get_by_id(self, id) -> List[BookOrders]:
        return self.session.query(BookOrders).filter_by(book_order_id=id).first()

    def get_by_user_id(self, id):
        return self.session.query(BookOrders).filter_by(user_id=id).first()

    def get_book_order_id_by_min_price(self, price):

        results = (
            self.session.query(BookOrders.book_order_id)
            .filter(BookOrders.taker_type == 'sell')
            .filter(BookOrders.price_coins == price)
            .order_by(BookOrders.price_coins.asc())
        )
        book_order_ids = [item[0] for item in results]
        return book_order_ids

    def get_book_order_id_by_highest_price(self, price):

        results = (
            self.session.query(BookOrders.book_order_id)
            .filter(BookOrders.taker_type == 'buy')
            .filter(BookOrders.price_coins == price)
            .order_by(BookOrders.price_coins.desc())
        )
        book_order_ids = [item[0] for item in results]
        return book_order_ids

    def get_lowest_price_sell(self):
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
            .first()
        )
        price, quantity_asaa, seller_id = lowest_price_info
        min_price = int(price)
        quantity_asa = int(quantity_asaa)
        seller_id_list = [int(seller_id)
                          for seller_id in seller_id.split(',') if seller_id]
        return [(min_price, seller_id_list, quantity_asa)]

        # return lowest_price_data

    def get_highest_price_buy(self):
        highest_price_info = (
            self.session.query(
                BookOrders.price_coins,
                func.sum(BookOrders.amount_asa),
                func.group_concat(
                    distinct(BookOrders.user_id)).label('user_ids'),

            )
            .filter(BookOrders.taker_type == "buy")
            .group_by(BookOrders.price_coins)
            .order_by(desc(BookOrders.price_coins))
            .first()
        )
        price, quantity_asaa, buyer_id = highest_price_info
        highest_price = int(price)
        quantity_asa = int(quantity_asaa)
        buyer_id_list = [int(seller_id)
                         for seller_id in buyer_id.split(',') if seller_id]
        return [(highest_price, buyer_id_list, quantity_asa)]

    def get_book_order_id_by_min_price(self, price):

        results = (
            self.session.query(BookOrders.book_order_id)
            .filter(BookOrders.taker_type == 'sell')
            .filter(BookOrders.price_coins == price)
            .order_by(BookOrders.price_coins.asc())
        )
        book_order_ids = [item[0] for item in results]
        return book_order_ids

    def get_book_order_id_by_highest_price(self, price):

        results = (
            self.session.query(BookOrders.book_order_id)
            .filter(BookOrders.taker_type == 'buy')
            .filter(BookOrders.price_coins == price)
            .order_by(BookOrders.price_coins.desc())
        )
        book_order_ids = [item[0] for item in results]
        return book_order_ids

    def get_earliest_user_id_and_asa_by_price(self, price, seller_id_list, taker_type):

        earliest_date_subq = self.session.query(
            func.min(BookOrders.created_at).label('earliest_date')
        ).filter(
            BookOrders.price_coins == price
        ).subquery()

        earliest_sellers = self.session.query(
            BookOrders.user_id,
            BookOrders.amount_asa
        ).filter(
            BookOrders.user_id.in_(seller_id_list),
            BookOrders.price_coins == price,
            BookOrders.taker_type == taker_type,
            BookOrders.created_at == earliest_date_subq.c.earliest_date
        ).order_by(
            BookOrders.user_id
        ).all()

        user_list = [(user_id, amount_asa)
                     for user_id, amount_asa in earliest_sellers]
        return user_list

    def get_seller_ids_and_asa_by_min_price(self, min_price):

        earliest_sellers = self.session.query(
            BookOrders.user_id,
            func.min(BookOrders.amount_asa)
        ).filter(
            BookOrders.price_coins == min_price,
            BookOrders.taker_type == 'sell'
        ).group_by(
            BookOrders.user_id
        ).all()

        user_list = [(user_id, amount_asa)
                     for (user_id, amount_asa) in earliest_sellers]

        return user_list

    def get_buyer_ids_and_asa_by_highest_price(self, highest_price):

        # Lấy user_id của những người bán có giá thấp nhất
        earliest_sellers = self.session.query(
            BookOrders.user_id,
            func.min(BookOrders.amount_asa)
        ).filter(
            BookOrders.price_coins == highest_price,
            BookOrders.taker_type == 'buy'
        ).group_by(
            BookOrders.user_id
        ).all()

        user_list = [(user_id, amount_asa)
                     for (user_id, amount_asa) in earliest_sellers]

        return user_list

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

    def sum_total_by_taker_type(self, taker_type, offset, limit):
        return (self.session.query(BookOrders.price_coins, func.sum(BookOrders.amount_asa).label('total'))
                .filter(BookOrders.taker_type == taker_type)
                .group_by(BookOrders.price_coins)
                .order_by(asc(BookOrders.price_coins))
                .offset(offset)
                .limit(limit)
                .all()
                )

    def count_distinct_prices(self, taker_type):
        return (self.session.query(func.count(func.distinct(BookOrders.price_coins)))
                .filter(BookOrders.taker_type == taker_type)
                .scalar())

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
        self.session.commit()

    def delete_book_order_by_min_price(self, min_price):
        book_order_id_list = self.get_book_order_id_by_min_price(min_price
                                                                 )
        for book_order_id in book_order_id_list:
            book_order = self.get_by_id(book_order_id)
            if book_order:
                self.session.delete(book_order)
        self.session.commit()

    def delete_book_order_by_highest_price(self, highest_price):
        book_order_id_list = self.get_book_order_id_by_highest_price(highest_price
                                                                     )
        for book_order_id in book_order_id_list:
            book_order = self.get_by_id(book_order_id)
            if book_order:
                self.session.delete(book_order)
        self.session.commit()

    def update_minus_astra_by_min_price(self, min_price, asa_spent):

        book_order_id_list = self.get_book_order_id_by_min_price(min_price
                                                                 )
        remaining_asa = asa_spent

        while remaining_asa > 0 and book_order_id_list:
            earliest_book_order_id = self.get_book_order_earliest(book_order_id_list)[0
                                                                                      ]
            book_order = self.get_by_id(earliest_book_order_id)

            if remaining_asa >= book_order.amount_asa:
                remaining_asa -= book_order.amount_asa
                self.session.delete(book_order)
                book_order_id_list.remove(earliest_book_order_id)
            else:
                book_order.amount_asa -= remaining_asa
                remaining_asa = 0

        self.session.commit()

    def update_by_highest_price(self, highest_price, asa_spent):
        book_order_id_list = self.get_book_order_id_by_highest_price(highest_price
                                                                     )
        remaining_asa = asa_spent

        while remaining_asa > 0 and book_order_id_list:
            earliest_book_order_id = self.get_book_order_earliest(book_order_id_list)[0
                                                                                      ]
            book_order = self.get_by_id(earliest_book_order_id)

            if remaining_asa >= book_order.amount_asa:
                remaining_asa -= book_order.amount_asa
                self.session.delete(book_order)
                book_order_id_list.remove(earliest_book_order_id)
            else:
                book_order.amount_asa -= remaining_asa
                remaining_asa = 0

        self.session.commit()
