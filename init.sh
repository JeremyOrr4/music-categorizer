
cd init_k8s
kubectl apply -f PV.yaml
kubectl apply -f PVC.yaml
cd ..

# ./start_airflow.sh

cd PCM-Encoder
docker build -f Dockerfile -t PCM-Encoder:latest .
kubectl apply -f k8s/deployment.yaml
cd ..



