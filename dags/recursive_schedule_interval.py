from __future__ import absolute_import, unicode_literals
import os
from airflow.operators import BashOperator
from airflow.models import DAG
from datetime import datetime, timedelta

args = {
    'owner': 'recursive_schedule_interval',
    'depends_on_past': False,
    'start_date': datetime(2021, 1, 1),
}

dag = DAG(
    dag_id='recursive_schedule_interval',
    default_args=args,
    schedule_interval="*/5 * * * 1,2,3,4,5",
    catchup=False
)

# cmd file name
CMD = 'echo Job executado em: $(date +"%d/%m/%Y %k:%M:%S")'

run_this = BashOperator(
    task_id='bash_operator', bash_command=CMD, dag=dag
)