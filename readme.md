## Repo Structure
* Directory - Repeated for all unique DAGs
  * <file_dag.py> - Must have _dag.py for proper deployment to Composer
  * sql
    * <sql_file.sql> - All files with .sql will be deployed to Composer
* utils - Python Package for configurations & helpers
  * bash - Shell scripts to setup new folders
    * setup_new_dag_folder.sh - Run this script with a single argument of folder name to create proper folder structure
  * default_args - Folder containing default argurments for DAG, Can be overwritten
    * default-args-environ.json - Proper default arguments are dynamically loaded on DAG run
  * params
    * params-environ.json - Proper params are dynamically loaded on DAG run
  * python
    * read_args_params.py - Class for loading default arguments and params

## Local Development
* `pip install apache-airflow`
* 'pip install google-cloud-storage'
* 'pip install apache-airflow-providers-google'
* Setup environment variable 
  * GCS_BUCKET - Bucket name of the Composer Bucket