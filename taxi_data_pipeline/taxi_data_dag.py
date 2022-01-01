## Import Libraries
import os
import sys
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from utils.python.read_conf import read_conf

## Add library for customs utils
sys.path.append(os.environ['GCS_BUCKET'] + '/dags/utils/python')

## Load Default Args
default_args = read_conf().get_default_args()
r_cfg = {'taxi_query': 'taxi_query.sql',
         'table': 'all_taxi_trips_test'}
default_args.update(r_cfg)

## Testing out default args and env variables
def print_default_args():
    """
    This can be any python code you want and is called from the python operator. The code is not executed until
    the task is run by the airflow scheduler.
    """
    print(f'########## default_args: {default_args} ##########')

def print_env():
    print(f"##### Env Vars: {os.environ} #####")

## Setup DAG using context manager
with DAG(dag_id='taxi-data-pipeline',
         start_date=datetime(2021, 12, 8),
         default_args=default_args) as dag:

    start = DummyOperator(task_id='start')

    end = DummyOperator(task_id='end')

    pc = PythonOperator(task_id='print_default_args',
                        python_callable=print_default_args)

    pe = PythonOperator(task_id='print_environment',
                        python_callable=print_env)

    bq_load = BigQueryExecuteQueryOperator(
        task_id='load_bq_table',
        sql=default_args['taxi_query'],
        destination_dataset_table=f"{default_args['project_id']}.{default_args['dataset']}.{default_args['table']}",
        write_disposition='WRITE_TRUNCATE',
        params=default_args
    )

    email_test = EmailOperator(
        task_id='send_email',
        to='jcb.learning.gcp@gmail.com',
        subject='THIS IS A TEST',
        html_content='THIS IS A TEST'
    )

    bash_fail = BashOperator(
        task_id='always_fail',
        bash_command='exit(1)'
    )

    start >> pc >> pe >> bq_load >> [email_test, bash_fail] >> end
