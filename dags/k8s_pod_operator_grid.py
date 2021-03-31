import datetime

from airflow import models
from airflow.contrib.kubernetes import secret
from airflow.contrib.operators import kubernetes_pod_operator

YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

default_args = {
    'owner': 'Trigger',
    'depends_on_past': False,
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
}

# If a Pod fails to launch, or has an error occur in the container, Airflow
# will show the task as failed, as well as contain all of the task logs
# required to debug.
with models.DAG(
        dag_id='k8s_pod_operator_grid',
        default_args=default_args,
        #schedule_interval=datetime.timedelta(days=1),
        start_date=YESTERDAY,
        schedule_interval=None,
) as dag:
    kubernetes_min_pod = kubernetes_pod_operator.KubernetesPodOperator(
        task_id='pod-grid',
        name='pod-grid',
        namespace='default',
        image='rodriguesflavio/flavio-poc')
    
    
    
        