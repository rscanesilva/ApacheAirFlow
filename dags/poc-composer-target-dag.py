import logging
from airflow import models
from datetime import datetime
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators import kubernetes_pod_operator
from airflow.operators.dagrun_operator import TriggerDagRunOperator

default_dag_args = {
    'start_date': datetime(2021, 3, 18),
    'owner': 'ARQT-REFE'
}

with models.DAG(
    'poc_composer_target_dag',
    schedule_interval=None,
    default_args=default_dag_args) as dag:
    
    task_one = DummyOperator(
        task_id='task_fake'
    )

   
    