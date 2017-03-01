#! usr/bin/env python
from airflow import DAG
from airflow.operators import BashOperator, PythonOperator
from datetime import datetime, timedelta
__author__ = "Jonathan Hilgart"


default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2016, 1, 1),
        'email': ['jonathan.hilgart@gmail.com'],
        'email_on_failure': True,
        'email_on_retry': False,
        'retries': 3,
        'retry_delay': timedelta(minutes=5),
      }

dag = DAG('normalize_bart_weather_data', default_args=default_args,
          schedule_interval='0 2 * * *') # run at 2 am
# run every 5 mins
t1 = BashOperator(
    task_id='normalize_data',
    bash_command='python ~/./normalization_bart_weather.py',
    retries=3,
    dag=dag)

t2 = BashOperator(
    task_id='delete_logs',
    bash_command='rm -rf ~/airflow/logs/*',
    retries=3,
    dag=dag)
