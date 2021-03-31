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

# Example of source DAG stating execution target DAG 
default_dag_args = {
    'start_date': datetime.datetime(2021, 3, 18),
    'owner': 'Interdependence Case One'
}

def run_target_dag(**kwargs):
    run = kwargs['dag_run'].conf.get('run_target_dag')
    if run == "true":
        return 'abort'
    else:
        return 'trigger_target_dag'

with models.DAG(
        'interdependence_case_one_dag_source',
        schedule_interval=None,
        default_args=default_dag_args) as dag:
    
    branching = BranchPythonOperator(
        task_id='trigger_next_dag_or_exit',
        python_callable=run_target_dag,
        provide_context=True)


    trigger = TriggerDagRunOperator(
        task_id='trigger_target_dag',
        trigger_dag_id="interdependence_case_one_dag_target",
        dag=dag,
        provide_context=True,
    )
    
    abort = DummyOperator(
        task_id='abort'
    )

    branching >> [trigger, abort]
