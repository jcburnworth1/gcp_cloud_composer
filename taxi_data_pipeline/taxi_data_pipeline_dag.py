## Import Libraries
import os
import sys
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from utils.python.read_configs import Configuration
from utils.python.helpers import Helpers

## Add library for customs utils
sys.path.append(os.environ['GCS_BUCKET'] + '/dags/utils/python')

## Load Markdown
doc = Configuration().get_markdown(md_file='taxi_data_pipeline.md')

## Load Default Args
default_args = Configuration().get_default_args()
default_args.update({'taxi_query': 'taxi_query.sql'})  # Add any additional default_args here for DAG specific needs

## Load Params
params = Configuration().get_params()
params.update({'table': 'all_taxi_trips_test',
               'view': 'vw_all_taxi_trips_test'})  # Add any additional params here for DAG specific needs

## Setup DAG using context manager
with DAG(dag_id='taxi-data-pipeline',
         start_date=datetime(2021, 12, 8),
         default_args=default_args,
         catchup=default_args['catchup'],
         max_active_runs=default_args['max_active_runs'],
         schedule_interval=default_args['schedule_interval'],
         tags=['taxi', 'datasource'],
         template_searchpath=default_args['template_searchpath'],
         params=params) as dag:
    dag.doc_md = doc

    start = DummyOperator(task_id='start')

    end = DummyOperator(task_id='end')

    pda = PythonOperator(task_id='print_default_args',
                         python_callable=Helpers.print_default_args,
                         op_kwargs={'default_args': default_args})

    pp = PythonOperator(task_id='print_params',
                        python_callable=Helpers.print_params,
                        op_kwargs={'params': params})

    pe = PythonOperator(task_id='print_environment',
                        python_callable=Helpers.print_env)

    bq_load_table = BigQueryExecuteQueryOperator(
        task_id='load_bq_table',
        use_legacy_sql=default_args['use_legacy_sql'],
        template_fields=['labels'],
        sql=default_args['taxi_query'],
        destination_dataset_table=f"{params['project_id']}.{params['dataset']}.{params['table']}",
        create_disposition=default_args['create_disposition'],
        write_disposition=default_args['write_disposition'],
        labels=default_args['labels'],
        params=params
    )

    bq_load_view = BigQueryExecuteQueryOperator(
        task_id='load_bq_view',
        sql='create_replace_view.sql',
        destination_dataset_table=None,
        time_partitioning=None,
        params=params
    )

    email_test = EmailOperator(
        task_id='send_email',
        to='jcb.learning.gcp@gmail.com',
        subject='THIS IS A TEST',
        html_content='THIS IS A TEST'
    )

    start >> [pda, pp, pe] >> bq_load_table >> bq_load_view >> email_test >> end
