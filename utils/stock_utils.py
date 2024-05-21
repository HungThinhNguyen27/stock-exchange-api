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

    def format_data(self, records):
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

    def data_frame(self, stock_list):
        data = []
        for row in stock_list:
            row_data = [row.time_stamp,
                        row.open_price,
                        row.close_price,
                        row.high_price,
                        row.low_price,
                        row.volume
                        ]
            data.append(row_data)
        return pd.DataFrame(data, columns=['time_stamp',
                                           'open_price',
                                           'close_price',
                                           'high_price',
                                           'low_price',
                                           'volume'])

    def time_calculate(self, data, interval_minutes):

        # df['time_stamp'] = pd.to_datetime(df['time_stamp'])

        if interval_minutes == 240:
            resample_rule = '4H'
            origin = pd.Timestamp(
                data['time_stamp'].dt.date.min()) + pd.Timedelta(hours=3)
            group_column = 'time_stamp'
        else:
            resample_rule = f'{interval_minutes}T'
            group_column = 'time_stamp'
            origin = 'start_day'

        grouped = data.resample(resample_rule, on=group_column, origin=origin)
        aggregated_df = grouped.agg(
            open_price=('open_price', 'first'),
            close_price=('close_price', 'last'),
            high_price=('high_price', 'max'),
            low_price=('low_price', 'min'),
            volume=('volume', 'sum')
        )

        aggregated_df = aggregated_df.reset_index()
        aggregated_df = aggregated_df.iloc[::-1]

        return aggregated_df

    def paginated(self, limit, offset, data):
        total_pages = (len(data) + limit - 1) // limit
        end = offset + limit
        paginated_df = data.iloc[offset:end]
        paginated_df = paginated_df.reset_index(drop=True)
        paginated_df['time_stamp'] = paginated_df['time_stamp'].apply(
            lambda x: f"{x.strftime('%Y-%m-%d')} {str(x.hour).zfill(2)}:{str(x.minute).zfill(2)}"
        )

        return paginated_df, total_pages
