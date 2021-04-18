import logging
from airflow import models
from datetime import datetime, date
from airflow.operators.dummy_operator import DummyOperator
from airflow.contrib.operators import kubernetes_pod_operator
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators.python_operator import BranchPythonOperator
from airflow.hooks.mysql_hook import MySqlHook

default_dag_args = {
    'start_date': datetime(2021, 3, 12),
    'owner': 'ARQT-REFE'
}

def validate_exec_date_function(connid, holidayTask, businessTask):
    mysql_hook: MySqlHook = MySqlHook(mysql_conn_id=connid)
    returned = mysql_hook.get_records(sql="SELECT count(date) FROM holiday where date=Date(now())")
    countReturned = int(re.sub("[^0-9]", "", str(returned[0])))
    
    print(countReturned)
    if countReturned > 0:
        return holidayTask
    else:
        return businessTask


with models.DAG(
    'poc_composer_source_dag',
    schedule_interval=None,
    default_args=default_dag_args) as dag:
    
    validate_exec_date = BranchPythonOperator(
        task_id='validate_exec_date',
        python_callable=validate_exec_date_function('mysql_calendar', 'holiday', 'task_one'),
        provide_context=True
    )

    task_one = DummyOperator(
        task_id='task_one'
    )

    grid = kubernetes_pod_operator.KubernetesPodOperator(
        task_id='pod-grid',
        name='pod-grid',
        namespace='default',
        image='rodriguesflavio/poc-pubsub-ok4',
        on_failure_callback='skip')
    
    sub_process = TriggerDagRunOperator(
       task_id='trigger_sub_process',
       trigger_dag_id="poc_composer_target_dag",
       dag=dag,
       provide_context=True,
    )
    
    skip = DummyOperator(
        task_id='skip',
        trigger_rule = 'all_done'
    )

    scheduleTask = DummyOperator(
        task_id='scheduleTask'
    )

    #exec when exec date is a holiday
    holiday = DummyOperator(
        task_id='holiday'
    )

    #defining the execution sequence
    (
        validate_exec_date 
        >> [task_one, holiday]
    )
    (
        task_one 
        >> [ grid, sub_process] 
        >> skip 
        >> scheduleTask
    )
    