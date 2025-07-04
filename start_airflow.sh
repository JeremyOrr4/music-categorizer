#!/bin/bash

# echo "[INFO] Uninstalling Airflow Helm release..."
# helm uninstall airflow
# helm repo remove apache-airflow

# echo "[INFO] Deleting Airflow services, pods, PVCs, configmaps, and secrets..."
# kubectl delete all --all -n airflow
# kubectl delete pvc --all -n airflow
# kubectl delete configmap --all -n airflow
# kubectl delete secret --all -n airflow

# # Info
# kubectl get all | grep airflow || echo "[INFO] All Airflow resources removed."

# start
kubectl create namespace airflow
helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm install airflow apache-airflow/airflow --namespace airflow --debug --timeout 10m01s
helm ls -n airflow 

kubectl apply -f init_deploy/secret.yaml --namespace airflow
helm upgrade --install airflow apache-airflow/airflow -n airflow -f init_deploy/values.yaml --debug --timeout 10m02s
# kubectl port-forward svc/airflow-api-server 8080:8080