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
                'query': """SELECT
                            *
                            FROM
                            `{{ params.project_id }}.{{ params.dataset }}.all_taxi_trips`
                            WHERE
                            id IN ('e4424ddc-cc53-446d-bed3-ccae930d4998','a2478b16-9c42-4ba1-bff6-ad0a10ea70ab',
                                   'ac87056b-0266-422f-81d2-1a6b592bbfdb','6c09c0e4-ce4e-47a5-b5fe-9ce947c2c507',
                                   '0338ede9-494f-4caa-88dc-91eff3648a3e','e20a954e-baf9-40a2-af84-006c8fe26e0d',
                                   '7db6a04b-e394-4c0b-9439-efe94ae5ecb9','922e90bf-deca-4ec1-9453-9edc73efc8af',
                                   '03fd0b86-d3a2-417e-9275-884a0bcaf03c','97499029-8eed-4610-b79b-1c674a20504b')""",
                'destinationTable': default_args['destination_dataset_table_v2']
            },
            'createDisposition': 'CREATE_IF_NEEDED',
            'writeDisposition': 'WRITE_TRUNCATE'
        },
        params=default_args
    )

    start >> pc >> pe >> [bq_load, bq_load_v2] >> end
