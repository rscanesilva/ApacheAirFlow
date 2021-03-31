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

# Example of source DAG starting the execution of the target DAG.
# After starting the execution of the target DAG, we have two flows:
# Flow A: Following the execution of the JOBS without waiting for the successful response from the target DAG
# Flow B: Waits for the target DAG to post the status of success or error in the pub / sub to make the decision whether execution follows or not.

GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "still-dynamics-307913")
TOPIC_FOR_SENSOR_DAG = os.environ.get("GCP_PUBSUB_SENSOR_TOPIC", "pubsub-trigger-composer-poc")

# [START howto_operator_gcp_pubsub_pull_messages_result_cmd]
echo_cmd = """
{% for m in task_instance.xcom_pull('pull_messages') %}
    echo "AckID: {{ m.get('ackId') }}, Base64-Encoded: {{ m.get('message') }}"
{% endfor %}
"""
# [END howto_operator_gcp_pubsub_pull_messages_result_cmd]


default_dag_args = {
    'start_date': datetime.datetime(2021, 3, 18),
    'owner': 'Interdependence Case Two'
}

with models.DAG(
        'interdependence_case_two_dag_source',
        schedule_interval=None,
        default_args=default_dag_args
) as dag:

    start = DummyOperator(
        task_id='start'
    )

    independent_flow = DummyOperator(
        task_id='independent_flow'
    )

    trigger = TriggerDagRunOperator(
        task_id='trigger_target_dag',
        trigger_dag_id="interdependence_case_two_dag_target",
        dag=dag,
        provide_context=True,
    )
    
     # [START howto_operator_gcp_pubsub_create_subscription]
    subscribe_task = PubSubCreateSubscriptionOperator(
        task_id="subscribe_task", project_id=GCP_PROJECT_ID, topic=TOPIC_FOR_SENSOR_DAG
    )
    # [END howto_operator_gcp_pubsub_create_subscription]
    # [START howto_operator_gcp_pubsub_pull_message_with_sensor]
    subscription = "{{ task_instance.xcom_pull('subscribe_task') }}"

    #PubSubSensor
    pull_messages = PubSubPullSensor(
        task_id="pull_messages",
        ack_messages=True,
        project_id=GCP_PROJECT_ID,
        subscription=subscription,
    )
    # [END howto_operator_gcp_pubsub_pull_message_with_sensor]

    # [START howto_operator_gcp_pubsub_pull_messages_result]
    pull_messages_result = BashOperator(
        task_id="pull_messages_result", 
        bash_command=echo_cmd
    )
    # [END howto_operator_gcp_pubsub_pull_messages_result]

    # [START howto_operator_gcp_pubsub_unsubscribe]
    unsubscribe_task = PubSubDeleteSubscriptionOperator(
        task_id="unsubscribe_task",
        project_id=GCP_PROJECT_ID,
        subscription="{{ task_instance.xcom_pull('subscribe_task') }}",
    )

    finish = DummyOperator(
        task_id='finish'
    )

    (
        start 
        >> trigger 
        >> [independent_flow, subscribe_task]
        >> finish
    )
    (
        pull_messages 
        >> pull_messages_result 
        >> unsubscribe_task() 
        >> finish
    )
    
