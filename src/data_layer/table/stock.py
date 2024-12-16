
from sqlalchemy import func
from typing import List
from src.data_layer.mysql_connect import MySqlConnect
from sqlalchemy import func, desc, text
from src.model.stock import StockPrice

class StockPriceDL(MySqlConnect):

    def add(self, time_stamp, open_price, close_price, high_price, low_price, volume):
        stock_price = StockPrice(
                    time_stamp=time_stamp,
                    open_price=open_price,
                    close_price=close_price,
                    high_price=high_price,
                    low_price=low_price,
                    volume=volume
                )
        self.session.add(stock_price)
        self.session.commit()


    def commit(self) -> None:
        self.session.commit()

    def get(self):
        return self.session.query(StockPrice).all()

    def get_one_latest_record(self):
        return self.session.query(StockPrice.time_stamp).order_by(
            desc(StockPrice.time_stamp)).first()

    def calculate_count(self, period):  # đẩy lên service
        count_query = self.session.query(func.count(StockPrice.id)).scalar()
        total_count = count_query // period
        return total_count

    def get_limited_time_stamps_by_period(self, period, limit, page):
        limited_time_stamps = self.session.query(StockPrice.time_stamp).order_by(
            StockPrice.time_stamp.desc()).limit(period*limit).offset((period*limit)*(page-1))
        return [ts[0] for ts in limited_time_stamps]

    def get_by_period_and_limit(self, period, limit, page): 

        """
        - Noted : 1 period corresponds to 1 minute
        The function first calculates whether the period the user wants to query is hours or days 
        If greater than or equal to 1440, it means the user wants to access the date and less than 1440 will access the time.The function will then calculate time 

            - For example, the user uses period 2880 (ie 2 days) and limit is 70 records:
                time = (2880 // 1440) * 70 = 140 days
                and will calculate from the current date to 140 days ago as well as returns 70 records for 2 days each.

        Retrieves aggregated stock price data based on a specified time period and limit,
        ordered by trade date in descending order.

        Args:
            period (int): The time period in minutes for aggregation.
            limit (int): The maximum number of records to retrieve.
            page (int): The page number for pagination (not implemented in current function).

        Returns:
            list: A list of tuples containing aggregated stock price data, including trade date,
                open price, close price, high price, low price, and volume.
        """
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


