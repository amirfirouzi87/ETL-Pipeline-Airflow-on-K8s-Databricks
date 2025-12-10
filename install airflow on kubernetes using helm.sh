kind delete cluster --name kind
kind create cluster --image kindest/node:v1.27.0 --config kind/clusters/kind-cluster.yaml

helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm show values apache-airflow/airflow > airflow-values.yaml


docker build --pull --tag my-airflow-image:0.1 -f docker/Dockerfile .
kind load docker-image my-airflow-image:0.1

kubectl create namespace airflow

kubectl apply -f kubernetes/secrets/git-secrets.yaml
kubectl apply -f kubernetes/volumes/airflow-logs-pv.yaml
kubectl apply -f kubernetes/volumes/airflow-logs-pvc.yaml


helm upgrade --install airflow apache-airflow/airflow \
    --namespace airflow -f chart/airflow-override-values.yaml \
    --debug


kubectl port-forward svc/airflow-api-server 8080:8080 --namespace airflow