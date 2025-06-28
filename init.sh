#!/bin/bash

RUN_INIT=false
RUN_PCM=false
RUN_PR=false

for arg in "$@"; do
  case $arg in
    --init) RUN_INIT=true ;;
    --pcm)  RUN_PCM=true ;;
    --pr)   RUN_PR=true ;;
    --all)  RUN_INIT=true; RUN_PCM=true; RUN_PR=true ;;
    *) echo "Unknown flag: $arg"; exit 1 ;;
  esac
done

if $RUN_INIT; then
  cd init_deploy
  kubectl apply -f PV.yaml
  kubectl apply -f PVC.yaml
  cd ..
fi

# ./start_airflow.sh

if $RUN_PCM; then
  cd PCM-Encoder
  docker build -f Dockerfile -t pcm-encoder:latest .
  kubectl apply -f k8s/deployment.yaml
  cd ..
fi

if $RUN_PR; then
  cd pr-generator
  kubectl delete job pr-generator
  docker build -f Dockerfile -t pr-generator:latest .
  kubectl apply -f k8s/deployment.yaml
  cd ..
fi


