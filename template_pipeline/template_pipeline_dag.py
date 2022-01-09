## Import Libraries
import os
import sys
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from utils.python.read_configs import Configuration

## Add library for customs utils
sys.path.append(os.environ['GCS_BUCKET'] + '/dags/utils/python')

## Load Markdown
doc = Configuration.get_markdown(md_file='template_pipeline.md')

## Load Default Args
default_args = Configuration().get_default_args()
default_args.update({'query': 'query.sql'})  # Add any additional default_args here for DAG specific needs

## Load Params
params = Configuration().get_params()
params.update({'table': 'table',
               'view': 'vw_view'})  # Add any additional params here for DAG specific needs

## Setup DAG using context manager
with DAG(dag_id='template',
         start_date=datetime(2021, 12, 8),
         default_args=default_args,
         catchup=default_args['catchup'],
         max_active_runs=default_args['max_active_runs'],
         schedule_interval=default_args['schedule_interval'],
         tags=default_args['tags'],
         template_searchpath=default_args['template_searchpath'],
         params=params) as dag:
    dag.doc_md = doc

    start = DummyOperator(task_id='start')

    middle = DummyOperator(task_id='middle')

    end = DummyOperator(task_id='end')

    start >> middle >> end
