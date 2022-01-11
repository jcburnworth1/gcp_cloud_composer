## Repo Structure
* Directory - Repeated for all unique DAGs
  * <file_dag.py> - Must have _dag.py for proper deployment to Composer
  * sql
    * <sql_file.sql> - All files with .sql will be deployed to Composer
* utils - Python Package for configurations & helpers
  * bash - Shell scripts to set up new folders
    * setup_new_dag_folder.sh - Run this script with a single argument of folder name to create proper folder structure
  * default_args - Folder containing default arguments for DAG, Can be overwritten
    * default-args-environ.json - Proper default arguments are dynamically loaded on DAG run
  * params
    * params-environ.json - Proper params are dynamically loaded on DAG run
  * python
    * read_args_params.py - Class / functions for loading default arguments and params
    * helpers.py - Class / functions for printing environ / arguments / etc.

## Local Development
* `pip install apache-airflow`
* `pip install google-cloud-storage`
* `pip install apache-airflow-providers-google`
* Setup environment variable 
  * GCS_BUCKET - Bucket name of the Composer Bucket

## Cloud Build Triggers
* This repo is setup for automatic deploys when pushes are made to master
  * Upon push, `cloudbuild.yaml` will execute in Cloud Build and place files into their proper places in GCS