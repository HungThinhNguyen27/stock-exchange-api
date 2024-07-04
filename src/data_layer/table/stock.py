
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
from functools import lru_cache


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
        if period >= 1440: 
            str = "DAY"
            time = (period // 1440) * limit
        else: 
            str = "HOUR"
            time = 1 if period < 60 else (period // 60) * limit 
            
        sql = f"""
                WITH ranked_data AS (
                    SELECT 
                        *,
                        ROW_NUMBER() OVER (PARTITION BY trade_date ORDER BY time_stamp ASC) AS rn_asc,
                        ROW_NUMBER() OVER (PARTITION BY trade_date ORDER BY time_stamp DESC) AS rn_desc
                    FROM (
                        SELECT 
                            FROM_UNIXTIME(FLOOR(UNIX_TIMESTAMP(time_stamp) / ({period}* 60)) * ({period} * 60)) AS trade_date,
                            open_price,
                            close_price,
                            high_price,
                            low_price,
                            volume,
                            time_stamp
                        FROM StockData.stock_price_new
                        WHERE time_stamp >= (SELECT MAX(time_stamp) - INTERVAL {time} {str} FROM StockData.stock_price_new) 

                    ) AS subquery
                )
                SELECT
                    trade_date,
                    MAX(CASE WHEN rn_desc = 1 THEN close_price END) AS close_price,
                    MAX(CASE WHEN rn_asc = 1 THEN open_price END) AS open_price,
                    MAX(high_price) AS high_price,
                    MIN(low_price) AS low_price,
                    SUM(volume) AS volume
                FROM ranked_data
                GROUP BY trade_date
                ORDER BY trade_date DESC 
                limit {limit}
        """
        query = text(sql)
        return self.session.execute(query).fetchall()


