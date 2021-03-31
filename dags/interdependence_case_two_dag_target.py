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
from airflow.providers.google.cloud.operators.pubsub import (
    PubSubCreateSubscriptionOperator,
    PubSubCreateTopicOperator,
    PubSubDeleteSubscriptionOperator,
    PubSubDeleteTopicOperator,
    PubSubPublishMessageOperator,
    PubSubPullOperator,
)
from airflow.providers.google.cloud.sensors.pubsub import PubSubPullSensor
from airflow.utils.dates import days_ago
import os
import random

GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "still-dynamics-307913")
TOPIC_FOR_SENSOR_DAG = os.environ.get("GCP_PUBSUB_SENSOR_TOPIC", "pubsub-trigger-composer-poc")
MESSAGE = {"data": b"success"};

default_dag_args = {
    'start_date': datetime.datetime(2021, 3, 18),
    'owner': 'Interdependence Case Two'
}

with models.DAG(
        'interdependence_case_two_dag_target',
        schedule_interval=None,
        default_args=default_dag_args) as dag:
    
    start = DummyOperator(
        task_id='start'
    )

    publish_task = PubSubPublishMessageOperator(
        task_id="publish_task",
        project_id=GCP_PROJECT_ID,
        topic=TOPIC_FOR_SENSOR_DAG,
        messages=[MESSAGE],
    )

    start >> publish_task