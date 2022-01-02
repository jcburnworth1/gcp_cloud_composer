## Import Libraries
import os
import sys
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from utils.python.read_args_params import ReadArgsParams

## Add library for customs utils
sys.path.append(os.environ['GCS_BUCKET'] + '/dags/utils/python')

## Load Default Args
default_args = ReadArgsParams().get_default_args()
default_args.update({'taxi_query': 'taxi_query.sql'})  # Add any additional default_args here for DAG specific needs

## Load Params
params = ReadArgsParams().get_params()
params.update({'table': 'all_taxi_trips_test'})

## Testing out default default_args and env variables
def print_default_args():
    """
    Print default arguments
    :return: None
    """
    print(f'########## default_args: {default_args} ##########')

def print_params():
    """
    Print default params
    :return: None
    """
    print(f'########## Params: {params} ##########')

def print_env():
    """
    Print environment variables
    :return: None
    """
    print(f"##### Env Vars: {os.environ} #####")

## Setup DAG using context manager
with DAG(dag_id='taxi-data-pipeline',
         start_date=datetime(2021, 12, 8),
         default_args=default_args,
         catchup=default_args['catchup'],
         max_active_runs=default_args['max_active_runs'],
         schedule_interval=default_args['schedule_interval'],
         tags=default_args['tags'],
         template_searchpath=default_args['template_searchpath'],
         params=params) as dag:

    start = DummyOperator(task_id='start')

    end = DummyOperator(task_id='end')

    pda = PythonOperator(task_id='print_default_args',
                                        python_callable=print_default_args)

    pp = PythonOperator(task_id='print_params',
                                  python_callable=print_params)

    pe = PythonOperator(task_id='print_environment',
                                        python_callable=print_env)

    bq_load_table = BigQueryExecuteQueryOperator(
        task_id='load_bq_table',
        sql=default_args['taxi_query'],
        destination_dataset_table=f"{params['project_id']}.{params['dataset']}.{params['table']}",
        write_disposition='WRITE_TRUNCATE',
        params=params
    )

    bq_load_view =  BigQueryExecuteQueryOperator(
        task_id='load_bq_view',
        sql='create_replace_view.sql'
    )

    email_test = EmailOperator(
        task_id='send_email',
        to='jcb.learning.gcp@gmail.com',
        subject='THIS IS A TEST',
        html_content='THIS IS A TEST'
    )

    start >> [pda, pp, pe] >> bq_load_table >> bq_load_table >> email_test >> end
