
from sqlalchemy import func, select, alias, column
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
# from sqlalchemy.sql.functions import row_number


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
            StockPrice.time_stamp.desc()).limit(period*limit).offset((period*limit)*(page-1))

        return [ts[0] for ts in limited_time_stamps]

    def get_by_period_and_limit(self, period, limit, page):
        
        partition = self.calculate_partition(period, limit, page)
        sql = f"""
        WITH limited_data AS (
            SELECT 
                time_stamp, 
                open_price, 
                close_price, 
                high_price, 
                low_price, 
                volume,
                FLOOR(UNIX_TIMESTAMP(time_stamp) / (:period * 60)) AS period
            FROM (SELECT *
                  FROM
                    StockData.stock_price_new PARTITION ({partition})
                  ORDER BY
                    time_stamp desc
                  LIMIT 100800 offset 0
            ) AS subquery
        )
        SELECT
            MIN(time_stamp) AS first_time_stamp,
            SUBSTRING_INDEX(GROUP_CONCAT(open_price ORDER BY time_stamp ASC), ',', 1) AS first_open_price,
            SUBSTRING_INDEX(GROUP_CONCAT(close_price ORDER BY time_stamp), ',', 1) AS last_close_price,
            MIN(low_price) AS low_price,
            MAX(high_price) AS high_price,
            SUM(volume) AS volume
        FROM limited_data
        GROUP BY period
        ORDER BY first_time_stamp DESC
        """
        query = text(sql)
        parameters = {
            'period': period,
            'limit': period * limit,
            'offset': (period * limit) * (page - 1),
        }
        result = self.session.execute(query, parameters).fetchall()

        return result
    
    def calculate_partition(self, period, limit, page): 
        query = text("SELECT count(id) FROM stock_price_new PARTITION (p2024)")
        count_query = self.session.execute(query).scalar()

        current_offset = (page - 1) * period * limit

        # Determine which partition(s) to use
        if current_offset + (period * limit) <= count_query: 
            return 'p2024'
        elif current_offset > count_query:
            return 'p2023'
        else:
            return 'p2023, p2024'
        


