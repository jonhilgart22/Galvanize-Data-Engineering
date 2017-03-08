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

dag = DAG('normalize_and_predict_bart_weather', default_args=default_args,
          schedule_interval='0 10 * * *') # run at 2 am
# run every 5 mins
t1 = BashOperator(
    task_id='normalize_data',
    bash_command='spark-submit ~/./normalization_bart_weather.py',
    retries=3,
    dag=dag)

t2 = BashOperator(
    task_id='generate_predictions',
    bash_command='spark-submit ~/./predict_ridership_ml_spark.py',
    retries=3,
    dag=dag)

t2.set_upstream(t1)
