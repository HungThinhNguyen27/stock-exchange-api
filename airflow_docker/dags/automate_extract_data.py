from airflow.operators.python import PythonOperator
from airflow.decorators import task
from airflow.models.dag import DAG
from datetime import datetime, timezone, timedelta
import requests
from airflow.hooks.base_hook import BaseHook
from sqlalchemy import create_engine
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
import pandas as pd
import pytz
from airflow.utils.task_group import TaskGroup


def api_constant(self):

    # period = 10080
    period = "1"
    start_date = datetime(2023, 5, 1, tzinfo=timezone.utc)
    start_timestamp = int(start_date.timestamp())
    url = "https://api.tiki.vn/rally/markets/asaxu/klines"
    current_date = datetime.utcnow()
    current_timestamp = int(current_date.timestamp())

    # current_date = datetime(2021, 4, 1, tzinfo=timezone.utc)
    # current_timestamp = int(current_date.timestamp())
    # start_date = current_date - timedelta(days=1)
    # start_timestamp = int(start_date.timestamp())

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7',
        'Cache-Control': 'no-cache',
        'Origin': 'https://exchange.tiki.vn',
        'Pragma': 'no-cache',
        'Referer': 'https://exchange.tiki.vn/',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    params_list = {
        'period': period,
        'time_from': start_timestamp,
        'time_to': current_timestamp
    }
    return url, params_list, headers


@task
def crawl_data():
    base_url, params_list, headers = api_constant()
    response = requests.get(base_url, params=params_list,
                            headers=headers)
    data_list = []
    if response.status_code == 200:
        data = response.json()
        data_list.extend(data)
    return data_list


@task
def transform_data(data_list):
    formatted_data = [
        {
            'time_stamp': record[0],
            'open_price': record[1],
            'close_price': record[4],
            'high_price': record[2],
            'low_price': record[3],
            'volume': record[5],
        }
        for record in data_list
    ]
    vietnam_timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    for record in formatted_data:
        print(record)
        normal_time = datetime.utcfromtimestamp(record['time_stamp'])
        vietnam_time = normal_time.replace(
            tzinfo=pytz.utc).astimezone(vietnam_timezone)
        record['time_stamp'] = vietnam_time.strftime('%Y-%m-%d %H:%M')
    return formatted_data


@task
def load_to_mysql(formatted_data):
    # Connect to MySQL
    mysql_hook = BaseHook.get_connection("mysql_default")
    connection_string = f"mysql+pymysql://{mysql_hook.login}:{mysql_hook.password}@{mysql_hook.host}/{mysql_hook.schema}"
    engine = create_engine(connection_string)
    # Load data into MySQL
    df = pd.DataFrame(formatted_data)
    df.to_sql(name='stock_price', con=engine, if_exists='replace', index=False)
    print("Data loaded to MySQL successfully")


with DAG(dag_id="automate_crawl_data", schedule_interval=timedelta(minutes=1), start_date=datetime(2024, 5, 14), catchup=False,  tags=["product_model"]) as dag:

    with TaskGroup("extract_data_from_tiki_exchange", tooltip="Extract and transform data") as extract_load_src:
        data_crawl = crawl_data()
        formatted_data = transform_data(data_crawl)
        load_data_to_mysql = load_to_mysql(formatted_data)

        # define order
        data_crawl >> formatted_data >> load_data_to_mysql
