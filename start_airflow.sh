helm uninstall airflow
kubectl delete svc airflow-api-server --ignore-not-found
kubectl delete svc airflow-webserver --ignore-not-found
kubectl delete pod -l app.kubernetes.io/instance=airflow --ignore-not-found
helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm install airflow apache-airflow/airflow -f init_k8s/minimal-airflow-values.yaml
kubectl port-forward svc/airflow-api-server 8080:8080