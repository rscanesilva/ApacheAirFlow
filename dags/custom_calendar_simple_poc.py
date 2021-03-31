from __future__ import print_function

import datetime
from airflow import models
from datetime import date
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators import python_operator
from airflow.operators.dummy_operator import DummyOperator
import logging

default_dag_args = {
    'start_date': datetime.datetime(2021, 3, 18),
    'owner': 'Custom Calendar'
}

def get_holiday_variable_value(**kwargs):
    holiday = datetime.datetime.strptime(
        kwargs['dag_run'].conf.get('holiday') , 
        '%d-%m-%Y'
    )

    if holiday.date() == date.today():
        return 'holiday'
    else:
        return 'bussiness_day'

with models.DAG(
        'custom_calendar_simple_poc',
        schedule_interval=None,
        default_args=default_dag_args) as dag:
    
    branching = BranchPythonOperator(
        task_id='branching',
        python_callable=get_holiday_variable_value,
        provide_context=True)

    bussiness_day = BashOperator(
        task_id='bussiness_day',
        bash_command="echo JOBS IS RUNNING TODAY IS BUSSINES DAY"
    )
    
    holiday = DummyOperator(
        task_id='holiday'
    )

    for i in range(0, 5):
        dummies = DummyOperator(task_id='task_{0}'.format(i))
        for j in range(0, 3):
            dummyOperator = DummyOperator(task_id='task_{0}_{1}'.format(i, j))
            dummies >> dummyOperator

        branching >> [bussiness_day, holiday]
        bussiness_day >> dummies