
from sqlalchemy import func, select
from model.stock import StockPrice
from typing import List
from data_layer.mysql_connect import MySqlConnect
from sqlalchemy import func, cast, Integer, desc, Date, and_, text
from sqlalchemy.sql import case
import json
from sqlalchemy.sql.expression import literal
import pandas as pd
from datetime import timedelta
from sqlalchemy.sql import extract
from sqlalchemy import select, func
from sqlalchemy.orm import aliased


class StockPriceDL(MySqlConnect):

    def add(self, record) -> None:
        self.session.add(record)
        self.session.commit()

    def commit(self) -> None:
        self.session.commit()

    def get(self):
        return self.session.query(StockPrice).all()

    def get_one_latest_record(self):
        latest_record = self.session.query(StockPrice.time_stamp).order_by(
            desc(StockPrice.time_stamp)).first()

        return latest_record

    def calculate_count(self, period):  # đẩy lên service
        count_query = self.session.query(func.count(StockPrice.id)).scalar()
        total_count = count_query // period
        return total_count

    def get_limited_time_stamps_by_period(self, period, limit, page):
        limited_time_stamps = self.session.query(StockPrice.time_stamp).order_by(
            StockPrice.time_stamp.desc()).limit(period*(limit)).offset((period*limit)*(page-1))

        return [ts[0] for ts in limited_time_stamps]

    def get_stock_data_by_period(self, period, limited_time_stamps_list):

        subquery = self.session.query(
            case(
                [(period > 1440, func.from_days(func.floor(func.to_days(
                    StockPrice.time_stamp) / (period / 1440)) * (period / 1440)))],
                else_=func.date(StockPrice.time_stamp)
            ).label('inner_date'),
            cast(
                case(
                    [(period > 60, func.floor(
                        func.hour(StockPrice.time_stamp) / (period / 60)) * (period / 60))],
                    else_=func.hour(StockPrice.time_stamp)
                ), Integer
            ).label('inner_hour'),
            case(
                [(period > 60, 0)],
                else_=(func.floor(func.minute(
                    StockPrice.time_stamp) / period) * period)
            ).label('inner_minute'),
            func.max(StockPrice.time_stamp).label('max_ts'),
            func.min(StockPrice.time_stamp).label('min_ts')
        ).filter(
            StockPrice.time_stamp.in_(limited_time_stamps_list)
        ).group_by(
            case(
                [(period > 1440, func.from_days(func.floor(func.to_days(
                    StockPrice.time_stamp) / (period / 1440)) * (period / 1440)))],
                else_=func.date(StockPrice.time_stamp)
            ),
            cast(
                case(
                    [(period > 60, func.floor(
                        func.hour(StockPrice.time_stamp) / (period / 60)) * (period / 60))],
                    else_=func.hour(StockPrice.time_stamp)
                ), Integer
            ),
            case(
                [(period > 60, 0)],
                else_=(func.floor(func.minute(
                    StockPrice.time_stamp) / period) * period)
            )
        ).subquery()

        # Tạo câu truy vấn chính
        query = self.session.query(
            case(
                [(period > 1440, func.from_days(func.floor(func.to_days(
                    StockPrice.time_stamp) / (period / 1440)) * (period / 1440)))],
                else_=func.date(StockPrice.time_stamp)
            ).label('trade_date'),
            cast(
                case(
                    [(period > 60, func.floor(
                        func.hour(StockPrice.time_stamp) / (period / 60)) * (period / 60))],
                    else_=func.hour(StockPrice.time_stamp)
                ), Integer
            ).label('trade_hours'),
            case(
                [(period > 60, 0)],
                else_=(func.floor(func.minute(
                    StockPrice.time_stamp) / period) * period)
            ).label('trade_minute'),
            func.max(case([(StockPrice.time_stamp == subquery.c.max_ts,
                            StockPrice.close_price)])).label('close_price'),
            func.min(case([(StockPrice.time_stamp == subquery.c.min_ts,
                            StockPrice.open_price)])).label('open_price'),
            func.max(StockPrice.high_price).label('high_price'),
            func.min(StockPrice.low_price).label('low_price'),
            func.sum(StockPrice.volume).label('volume')
        ).join(subquery, and_(
            case(
                [(period > 1440, func.from_days(func.floor(func.to_days(
                    StockPrice.time_stamp) / (period / 1440)) * (period / 1440)))],
                else_=func.date(StockPrice.time_stamp)
            ) == subquery.c.inner_date,
            cast(
                case(
                    [(period > 60, func.floor(
                        func.hour(StockPrice.time_stamp) / (period / 60)) * (period / 60))],
                    else_=func.hour(StockPrice.time_stamp)
                ), Integer
            ) == subquery.c.inner_hour,
            case(
                [(period > 60, 0)],
                else_=(func.floor(func.minute(
                    StockPrice.time_stamp) / period) * period)
            ) == subquery.c.inner_minute
        )).group_by(
            case(
                [(period > 1440, func.from_days(func.floor(func.to_days(
                    StockPrice.time_stamp) / (period / 1440)) * (period / 1440)))],
                else_=func.date(StockPrice.time_stamp)
            ),
            cast(
                case(
                    [(period > 60, func.floor(
                        func.hour(StockPrice.time_stamp) / (period / 60)) * (period / 60))],
                    else_=func.hour(StockPrice.time_stamp)
                ), Integer
            ),
            case(
                [(period > 60, 0)],
                else_=(func.floor(func.minute(
                    StockPrice.time_stamp) / period) * period)
            ))

        query = query.order_by(desc(func.max(StockPrice.time_stamp)))
        results = query.all()
        return results


# b = [ts.time_stamp for ts in all]
# limited_time_stamps_list = a.get_stock_data_by_period(60, b)
# # # latest_record = a.get_stock_data(60, limited_time_stamps_list.limited_time_stamps)


# def format_data(records):
#     stock_data = []
#     for record in records:
#         minutes = int(float(record[2]))
#         datetime_string = f"{record[0].strftime('%Y-%m-%d')} {str(record[1]).zfill(2)}:{str(minutes).zfill(2)}"
#         stock_dict = {
#             "time_stamp": datetime_string,
#             "open_price": record[3],
#             "close_price": record[4],
#             "high_price": record[5],
#             "low_price": record[6],
#             "volume": int(record[7])
#         }
#         stock_data.append(stock_dict)
#     return stock_data


# format = format_data(limited_time_stamps_list)
# for i in format:
#     print(i)


# # print(count_query)
# format = format_data(count_query)

# # for i in format:
# #     print(i)
# print(format)
