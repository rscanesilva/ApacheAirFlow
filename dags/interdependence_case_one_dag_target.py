from __future__ import print_function

import datetime
from airflow import models
from datetime import date
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators import python_operator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
import logging

default_dag_args = {
    'start_date': datetime.datetime(2021, 3, 18),
    'owner': 'Interdependence Case One'
}

with models.DAG(
        'interdependence_case_one_dag_target',
        schedule_interval=None,
        default_args=default_dag_args) as dag:
    
    hello = BashOperator(
        task_id='say_hello',
        bash_command="echo Hello I am started from source DAG"
    )
