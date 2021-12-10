## Import Libraries
import os
import sys
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
# from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator, BigQueryExecuteQueryOperator
from utils.python.read_conf import read_conf

## Add library for customs utils
sys.path.append(os.environ['GCS_BUCKET'] + '/dags/utils/python')

## Load Default Args
default_args = read_conf().get_default_args()
default_args['use_legacy_sql'] = False
r_cfg = {'taxi_query': 'sql/taxi_query.sql',
         'destination_dataset_table': 'cloud-composer-poc-334522.taxi_trips.all_taxi_trips_test',
         'destination_dataset_table_v2': 'cloud-composer-poc-334522.taxi_trips.all_taxi_trips_test_v2',}
default_args.update(r_cfg)

def print_default_args():
    """
    This can be any python code you want and is called from the python operator. The code is not executed until
    the task is run by the airflow scheduler.
    """
    print(f'########## default_args: {default_args} ##########')


def print_env():
    print(f"##### Env Vars: {os.environ} #####")


# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG(dag_id='taxi-data-pipeline',
         start_date=datetime(2021, 12, 8),
         max_active_runs=1,
         schedule_interval=None,
         default_args=default_args,
         catchup=False,
         template_searchpath=[
             '/home/airflow/gcs/dags'
         ],
         tags=['test', 'taxi']) as dag:
    start = DummyOperator(task_id='start')

    end = DummyOperator(task_id='end')

    pc = PythonOperator(task_id='print_default_args',
                        python_callable=print_default_args)

    pe = PythonOperator(task_id='print_environment',
                        python_callable=print_env)

    bq_load = BigQueryExecuteQueryOperator(
        task_id='load_bq_table',
        sql=default_args['taxi_query'],
        destination_dataset_table=default_args['destination_dataset_table'],
        write_disposition='WRITE_TRUNCATE',
        params=default_args
    )

    bq_load_v2 = BigQueryInsertJobOperator(
        task_id='load_bq_table_v2',
        configuration={
            'query': {
                'query': default_args['taxi_query'],
                'destinationTable': default_args['destination_dataset_table_v2']
            },
            'writeDisposition': 'WRITE_TRUNCATE'
        },
        params=default_args
    )

    start >> pc >> pe >> [bq_load, bq_load_v2] >> end
