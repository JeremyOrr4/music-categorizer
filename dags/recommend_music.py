from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from kubernetes.client import V1Volume, V1PersistentVolumeClaimVolumeSource, V1VolumeMount

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 0,
}

with DAG(
    dag_id="recommend_music",
    default_args=default_args,
    description="Get recommend songs from database",
    schedule_interval=None,
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

    music_recommender = KubernetesPodOperator(
        task_id="music_recommender",
        name="music-recommender",
        namespace="airflow",
        service_account_name="airflow-worker",
        image="music-recommender:latest",
        image_pull_policy="IfNotPresent",
        cmds=["python", "main.py"],
        arguments=["--recommend", "New Person, Same Old Mistakes"],
        volumes=[volume],
        volume_mounts=[volume_mount],
        is_delete_operator_pod=True,
        get_logs=True,
    )

    music_recommender
