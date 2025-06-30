from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="my_example_dag",
    schedule_interval=None,
    catchup=False,
) as dag:
    t1 = BashOperator(
        task_id="print_hello",
        bash_command="echo 'Hello from Airflow!'"
    )
