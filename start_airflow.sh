helm uninstall airflow
kubectl delete svc airflow-api-server --ignore-not-found
kubectl delete svc airflow-webserver --ignore-not-found
helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm install airflow apache-airflow/airflow -f init_deploy/minimal-airflow-values.yaml
kubectl port-forward svc/airflow-api-server 8080:8080