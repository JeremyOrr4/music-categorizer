from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import V1Volume, V1PersistentVolumeClaimVolumeSource, V1VolumeMount

# DAG default args
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 0,
}

with DAG(
    dag_id="mount_data",
    default_args=default_args,
    description="Run music processing pods in sequence",
    schedule_interval=None,  # Run on demand
    start_date=days_ago(1),
    catchup=False,
) as dag:

    volume = V1Volume(
        name="music-categorizer-pvc",
        persistent_volume_claim=V1PersistentVolumeClaimVolumeSource(
            claim_name="music-categorizer-pvc"
        ),
    )

    volume_mount = V1VolumeMount(
        name="music-categorizer-pvc",
        mount_path="/music-categorizer-data",
    )

    get_audio = KubernetesPodOperator(
        task_id="get_audio",
        name="get-audio",
        namespace="airflow",
        service_account_name="airflow-worker",
        image="get-audio:latest",
        image_pull_policy="IfNotPresent",
        volumes=[volume],
        volume_mounts=[volume_mount],
        is_delete_operator_pod=True,
        get_logs=True,
    )

    pcm_encoder = KubernetesPodOperator(
        task_id="pcm_encoder",
        name="pcm-encoder",
        namespace="airflow",
        service_account_name="airflow-worker",
        image="pcm-encoder:latest",
        image_pull_policy="IfNotPresent",
        volumes=[volume],
        volume_mounts=[volume_mount],
        is_delete_operator_pod=True,
        get_logs=True,
    )

    pr_generator = KubernetesPodOperator(
        task_id="pr_generator",
        name="pr-generator",
        namespace="airflow",
        service_account_name="airflow-worker",
        image="pr-generator:latest",
        image_pull_policy="IfNotPresent",
        volumes=[volume],
        volume_mounts=[volume_mount],
        is_delete_operator_pod=True,
        get_logs=True,
    )

    lr_generator = KubernetesPodOperator(
        task_id="lr_generator",
        name="lr-generator",
        namespace="airflow",
        service_account_name="airflow-worker",
        image="lr-generator:latest",
        image_pull_policy="IfNotPresent",
        volumes=[volume],
        volume_mounts=[volume_mount],
        is_delete_operator_pod=True,
        get_logs=True,
    )

    clean_pvc = KubernetesPodOperator(
        task_id="clean_pvc",
        name="clean-pvc",
        namespace="airflow",
        service_account_name="airflow-worker",
        image="clean-pvc:latest",
        image_pull_policy="IfNotPresent",
        volumes=[volume],
        volume_mounts=[volume_mount],
        is_delete_operator_pod=True,
        get_logs=True,
    )

    get_audio >> pcm_encoder >> pr_generator >> lr_generator >> clean_pvc
