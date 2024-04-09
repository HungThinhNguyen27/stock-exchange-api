
from model.stock import StockPrice
from typing import List
from data_layer.mysql_connect import MySqlConnect
from sqlalchemy import func, desc, asc
from sqlalchemy.sql import case
import json
import csv
import pandas as pd


class StockPriceDL(MySqlConnect):

    def add(self, record) -> None:
        self.session.add(record)
        self.session.commit()

    def commit(self) -> None:
        self.session.commit()

    def calculate_count(self, interval):
        count_query = (
            self.session.query(
                func.count().label('total_count')
            ).select_from(
                self.session.query(
                    func.date(StockPrice.time_stamp).label('trade_date'),
                    func.hour(StockPrice.time_stamp).label('trade_hour'),
                    (func.floor(func.minute(StockPrice.time_stamp) / interval)
                     * interval).label('interval')
                )
                .group_by(
                    "trade_date",
                    "trade_hour",
                    "interval"
                )
                .subquery()
            )
        )
        count_result = count_query.one()
        return count_result.total_count

    def get_stock_data(self, interval, limit, offset):

        min_max_ts = self.session.query(
            func.date(StockPrice.time_stamp).label('inner_date'),
            func.hour(StockPrice.time_stamp).label('inner_hour'),
            (func.floor(func.minute(StockPrice.time_stamp) / interval)
             * interval).label('inner_interval'),
            func.min(StockPrice.time_stamp).label('min_ts'),
            func.max(StockPrice.time_stamp).label('max_ts')
        ).group_by('inner_date', 'inner_hour', 'inner_interval').subquery()

        query = self.session.query(
            func.date(StockPrice.time_stamp).label('trade_date'),
            func.hour(StockPrice.time_stamp).label('trade_hour'),
            (func.floor(func.minute(StockPrice.time_stamp) / interval)
             * interval).label('five_min_interval'),
            func.max(case([(StockPrice.time_stamp == min_max_ts.c.min_ts,
                            StockPrice.open_price)], else_=None)),
            func.max(case([(StockPrice.time_stamp == min_max_ts.c.max_ts,
                            StockPrice.close_price)], else_=None)),
            func.max(StockPrice.high_price),
            func.min(StockPrice.low_price),
            func.sum(StockPrice.volume)
        ).filter(
            func.date(StockPrice.time_stamp) == min_max_ts.c.inner_date,
            func.hour(StockPrice.time_stamp) == min_max_ts.c.inner_hour,
            (func.floor(func.minute(StockPrice.time_stamp) / interval)
             * interval) == min_max_ts.c.inner_interval
        ).group_by(
            'trade_date', 'trade_hour', 'five_min_interval'
        ).order_by(
            func.date(StockPrice.time_stamp).desc(),
            func.hour(StockPrice.time_stamp).desc(),
            (func.floor(func.minute(StockPrice.time_stamp) / interval) * interval).desc()
        ).correlate(StockPrice)

        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)

        return query


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


# a = StockPriceDL()
# result = a.get_stock_data(30, None, None)
# formatted_output = format_data(result)
# dowload = a.download_stock_info("json", formatted_output)


# formatted_output = format_data(result)
# # print("Total count:", result)
# for row in formatted_output:
#     rowaaa = {"stock_candles": row}
#     print(rowaaa)
# for row in result:
#     print(row)
