from collections import defaultdict
from flask import request, send_file
import json
import csv
import pandas as pd
from io import BytesIO


class StockUtils:

    def pagination(self, page_param):
        per_page = 10
        offset = (page_param - 1) * per_page
        return per_page, offset

    def group_and_sum_book_orders_buy(self, book_order_list):
        price_asa_map = defaultdict(float)
        for book_order in book_order_list:
            price = book_order.price
            total = book_order.total
            taker_type = book_order.taker_type

            if taker_type == 'buy':
                price_asa_map[price] += total
        return price_asa_map

    def group_and_sum_book_orders_sell(self, book_order_list):
        price_asa_map = defaultdict(float)
        for book_order in book_order_list:
            price = book_order.price
            total = book_order.total
            taker_type = book_order.taker_type

            if taker_type == 'sell':
                price_asa_map[price] += total
        return price_asa_map

    def page_param(self, count_result, page, limit):

        total_pages = (count_result + limit - 1) // limit
        next_page_url = None
        if page < total_pages:
            next_page_url = (
                f"{request.base_url}?page={page + 1}&limit={limit}"
            )
        return next_page_url, total_pages

    def format_data1(self, records):
        stock_data = []
        for record in records:
            minutes = int(float(record[2]))
            datetime_string = f"{record[0].strftime('%Y-%m-%d')} {str(record[1]).zfill(2)}:{str(minutes).zfill(2)}"
            stock_dict = {
                "time_stamp": datetime_string,
                "open_price": record[3],
                "close_price": record[4],
                "high_price": record[5],
                "low_price": record[6],
                "volume": int(record[7])
            }
            stock_data.append(stock_dict)
        return stock_data

    def format_data(self, records):
        stock_data = []
        for record in records:
            stock_dict = {
                "time_stamp": record.first_time_stamp.strftime("%Y-%m-%d %H:%M:%S"),
                "open_price": record.first_open_price,
                "close_price": record.last_close_price,
                "high_price": record.high_price,
                "low_price": record.low_price,
                "volume": int(record.volume)
            }
            stock_data.append(stock_dict)
        return stock_data

    def download_file(self, type_file, file_data, interval):

        filename = f'stock_info_{interval}min.{type_file}'

        if type_file == 'json':
            file_content = json.dumps(file_data, indent=4)
            mimetype = 'application/json'
            file_bytes = file_content.encode('utf-8')
            file_obj = BytesIO(file_bytes)

        elif type_file == 'csv':
            with open(filename, mode='w', newline='') as csv_file:
                fieldnames = file_data[0].keys()
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                for row in file_data:
                    writer.writerow(row)
            mimetype = 'text/csv'
            file_obj = filename

        return send_file(file_obj, as_attachment=True, download_name=filename, mimetype=mimetype)

    def paginated(self, limit, offset, data):
        total_pages = (len(data) + limit - 1) // limit
        end = offset + limit
        paginated_df = data.iloc[offset:end]
        paginated_df = paginated_df.reset_index(drop=True)
        paginated_df['time_stamp'] = paginated_df['time_stamp'].apply(
            lambda x: f"{x.strftime('%Y-%m-%d')} {str(x.hour).zfill(2)}:{str(x.minute).zfill(2)}"
        )

        return paginated_df, total_pages

    def calculate_total_pages(self, total_count: int, limit: int) -> int:
        """
        Tính tổng số trang dựa trên tổng số mục và số lượng mục trên mỗi trang.

        Args:
            total_count (int): Tổng số mục.
            limit (int): Số lượng mục trên mỗi trang.

        Returns:
            int: Tổng số trang.
        """
        return (total_count + limit - 1) // limit