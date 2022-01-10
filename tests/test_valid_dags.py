## Import Libraries
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.models import DagBag

def test_python_operator():
    test = PythonOperator(task_id="test_python", python_callable=lambda: "testme")
    result = test.execute(context={})
    assert result == "testme"

def test_bash_operator():
    test = BashOperator(task_id="test_bash", bash_command="echo testme")
    result = test.execute(context={})
    assert result == "testme"

# def test_dags_load_with_no_errors():
#     dag_bag = DagBag(include_examples=False)
#     dag_bag.process_file('taxi_data_pipeline/taxi_data_pipeline.py')
#     assert not dag_bag.import_errors
