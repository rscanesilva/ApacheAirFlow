from __future__ import print_function

from airflow import models
from datetime import datetime
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator

default_dag_args = {
    'start_date': datetime(2021, 3, 18),
    'owner': 'File transfer GCS to GCS'
}

with models.DAG(
        'file_transfer_gcs_to_gcs',
        schedule_interval=None,
        default_args=default_dag_args) as dag:

    copy_single_file = GCSToGCSOperator(
        task_id='copy_single_file',
        source_bucket='southamerica-east1-poc-airf-904b2db6-bucket',
        source_objects=['dags/airflow_monitoring.py'],
        destination_bucket='trigger-bucket-poc',
        destination_object='copied_file/airflow_monitoring.py',
        
    )