from __future__ import print_function

from airflow import models
from datetime import datetime, date, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.sensors.date_time_sensor import  DateTimeSensor

default_dag_args = {
    'start_date': datetime(2021, 3, 18),
    'owner': 'Job with own scheduler'
}

with models.DAG(
        'date_time_sensor',
        schedule_interval=None,
        default_args=default_dag_args) as dag:
    
    hello = BashOperator(
        task_id='init',
        bash_command="echo Dag running"
    )
    
    awaitStart = DateTimeSensor(
        task_id='wait_for_five_minutes',
        target_time=datetime.now() + timedelta(minutes = 5),
    )

    hello >> awaitStart