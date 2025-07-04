from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime

default_args = {
    "start_date": datetime(2023, 1, 1),
    "catchup": False,
}

with DAG(
    "k8s_pod_order_example",
    default_args=default_args,
    schedule_interval=None,
    description="Run pods in sequence A -> B -> C",
) as dag:

    task_a = KubernetesPodOperator(
        namespace="airflow",
        image="alpine",
        cmds=["sh", "-c", "echo 'Task A running' && sleep 5"],
        name="task-a",
        task_id="run_task_a",
        is_delete_operator_pod=True,
    )

    task_b = KubernetesPodOperator(
        namespace="airflow",
        image="alpine",
        cmds=["sh", "-c", "echo 'Task B running' && sleep 5"],
        name="task-b",
        task_id="run_task_b",
        is_delete_operator_pod=True,
    )

    task_c = KubernetesPodOperator(
        namespace="airflow",
        image="alpine",
        cmds=["sh", "-c", "echo 'Task C running' && sleep 5"],
        name="task-c",
        task_id="run_task_c",
        is_delete_operator_pod=True,
    )

    task_a >> task_b >> task_c
