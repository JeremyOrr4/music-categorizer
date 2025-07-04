from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2023, 1, 1),
}

dag = DAG(
    dag_id='hello_world_dag',
    default_args=default_args,
    schedule=None,
    catchup=False,
)

hello_task = BashOperator(
    task_id='print_hello',
    bash_command='echo "Hello, World!"',
    dag=dag,
)

