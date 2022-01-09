## Setup new DAG directory with proper structure
## Must pass name of folder as only argument
## Naming Convention <dag_name>_pipeline
## Example: taxi_data_pipeline
folder=$1
echo "Setting up new directory: $folder"

mkdir $folder
cp -r template_pipeline/* $folder

mv $folder/template_pipeline_dag.py $folder/$folder"_pipeline_dag.py"
mv $folder/template_pipeline.md $folder/$folder"_pipeline.md"