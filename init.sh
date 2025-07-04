#!/bin/bash

RUN_INIT=false
RUN_PCM=false
RUN_PR=false
RUN_LR=false
RUN_MR=false
RUN_AF=false
RUN_DOCKER=false

for arg in "$@"; do
  case $arg in
    --init) RUN_INIT=true ;;
    --pcm)  RUN_PCM=true ;;
    --pr)   RUN_PR=true ;;
    --lr)   RUN_LR=true ;;
    --mr)   RUN_MR=true ;;
    --af)   RUN_AF=true ;;
    --docker)   RUN_DOCKER=true ;;
    --all)  RUN_INIT=true; RUN_PCM=true; RUN_PR=true; RUN_LR=true; RUN_MR=true; RUN_AF=true; RUN_DOCKER=true;;
    *) echo "Unknown flag: $arg"; exit 1 ;;
  esac
done

if $RUN_INIT; then
  cd init_deploy
  kubectl apply -f PVC.yaml
  cd ..
fi

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

if $RUN_LR; then
  cd lr-generator
  kubectl delete job lr-generator  
  docker build -f Dockerfile -t lr-generator:latest .
  kubectl apply -f k8s/deployment.yaml
  cd ..
fi

if $RUN_MR; then
  cd music-recommender
  kubectl delete job music-recommender  
  docker build -f Dockerfile -t music-recommender:latest .
  kubectl apply -f k8s/deployment.yaml
  cd ..
fi

if $RUN_AF; then
  ./start_airflow.sh
fi


if $RUN_DOCKER; then
  cd PCM-Encoder
  docker build -f Dockerfile -t pcm-encoder:latest .
  cd ..

  cd pr-generator
  kubectl delete job pr-generator
  docker build -f Dockerfile -t pr-generator:latest .
  cd ..

  cd lr-generator
  kubectl delete job lr-generator  
  docker build -f Dockerfile -t lr-generator:latest .
  cd ..

  cd music-recommender
  kubectl delete job music-recommender  
  docker build -f Dockerfile -t music-recommender:latest .
  cd ..

fi
