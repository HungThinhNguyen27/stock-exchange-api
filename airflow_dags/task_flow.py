

from datetime import datetime, timedelta
from utils.crawl_stock_data import CrawlData
from airflow import DAG
from airflow.operators.python import PythonOperator
from data_layer.table.stock import StockPriceDL


def crawl_stock_price(ti):
    data_list = CrawlData().crawl_stock_price()
    ti.xcom_push(key='stock_data', value=data_list)


def add_stock_price_data(ti):
    data_list = ti.xcom_pull(key='stock_data', task_ids='crawl_data')
    StockPriceDL().add(data_list)


dag = DAG(
    dag_id='crawl_stock_data',
    schedule=timedelta(days=1),
    start_date=datetime.today() - timedelta(days=1),
    tags=['hungthinh'])

crawl_data = PythonOperator(
    task_id='crawl_data',
    python_callable=crawl_stock_price,
    dag=dag,
)
save_data = PythonOperator(
    task_id='save_data_to_mysql',
    python_callable=add_stock_price_data,
    dag=dag,
)
crawl_data >> save_data


# docker run -it --name crawl_stock_price -v /Users/macos/Downloads/test/dags:/opt/airflow/dags -p 8080:8080  -d apache/airflow:2.3.0-python3.8 bash
# bash -c '(airflow db init && airflow users create --username thinh123 --password thinh123 --firstname thinh lastname hung --role Admin --email thung4199@gmail.com); airflow webserver & airflow scheduler'
# docker exec -it 710 bash
# /Users/macos/Downloads/test
