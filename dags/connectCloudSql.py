from datetime import timedelta, datetime, timezone

from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

from dependencies import pymysql

default_args = {
   'owner': 'Airflow',
   'start_date': datetime(2019, 1, 1),
   # 'end_date': datetime(2020, 12, 31),
   'depends_on_past': True,
   'retries': 1,
   'retry_delay': timedelta(minutes=1),
   'catchup_by_default': False
}

dag = DAG('cloudsql_via_proxy', schedule_interval='@once',
         default_args=default_args)


# Firstly run the dummy operator
dummy = DummyOperator(
   task_id='dummy',
   trigger_rule='all_success',
   dag=dag,
)


def fn_select():
   sql = "SELECT * FROM holidays"
   
   connection = pymysql.connect(
      host='34.95.154.184',
      port=3306,
      user='root',
      password='poccomposer',
      db='calendar',
      charset='utf8',
      cursorclass=pymysql.cursors.DictCursor)

   # try the SELECT query
   with connection.cursor() as cursor:
      cursor.execute(sql)
      dbdata = cursor.fetchall()
      for i in dbdata:
            print(i)
      connection.commit()


fn_select = PythonOperator(
   task_id='fn_select',
   python_callable=fn_select,
   dag=dag)

dummy >> fn_select