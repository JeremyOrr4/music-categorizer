kubectl apply -f init_k8s/PV.yaml
kubectl apply -f init_k8s/PVC.yaml

docker build -f PCM-Encoding/Dockerfile -t pcm-encoding .
kubectl apply -f PCM-Encoding/k8s/deployment.yaml





