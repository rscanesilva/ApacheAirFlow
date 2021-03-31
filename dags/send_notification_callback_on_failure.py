from airflow import models
from airflow.operators import email_operator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

from airflow.hooks.base_hook import BaseHook
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator

# This should match the connection ID created in the Medium article
SLACK_CONN_ID = "slack"

def error():
    raise ValueError('Force error for test!!')

#SALCK NOTIFICATION
def task_fail_slack_alert(context):
    slack_webhook_token = BaseHook.get_connection(SLACK_CONN_ID).password
    slack_msg = """
            :red_circle: Task Failed. 
            *Task*: {task}  
            *Dag*: {dag} 
            *Execution Time*: {exec_date}  
            *Log Url*: {log_url} 
            """.format(
        task=context.get("task_instance").task_id,
        dag=context.get("task_instance").dag_id,
        ti=context.get("task_instance"),
        exec_date=context.get("execution_date"),
        log_url=context.get("task_instance").log_url,
    )

    failed_alert = SlackWebhookOperator(
        task_id="slack_test",
        http_conn_id=SLACK_CONN_ID,
        webhook_token=slack_webhook_token,
        message=slack_msg,
        username="airflow",
    )

    return failed_alert.execute(context=context)

#EMAIL NOTIFICATION - TODO: CONFIG SENDGRID
def report_failure(context):
    send_email = email_operator.EmailOperator(
        task_id='email_summary',
        to='rscanesilva@gmail.com',
        subject='Test email notify on task failure',
        html_content="Atendimento emergêncial!!! \n Erro na task: "+ context.get("task_instance").task_id,
    )
    send_email.execute(context)



default_dag_args = {
    'start_date': datetime(2021, 3, 18),
    'owner': 'Custom notification on failure',
    "on_failure_callback": task_fail_slack_alert
}

with models.DAG(
    'send_notification_on_failure',
    schedule_interval=None,
    default_args=default_dag_args) as dag:


    forceError = PythonOperator(
        task_id='force_error',
        python_callable=error
    )

