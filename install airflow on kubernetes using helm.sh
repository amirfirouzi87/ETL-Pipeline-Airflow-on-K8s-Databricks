kind delete cluster --name kind
kind create cluster --image kindest/node:v1.27.0 --config k8s/clusters/kind-cluster.yaml

helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm show values apache-airflow/airflow > airflow-values.yaml


docker build --pull --tag my-airflow-image:0.1 -f CICD/Dockerfile .
kind load docker-image my-airflow-image:0.1

kubectl create namespace airflow

kubectl apply -f k8s/secrets/git-secrets.yaml
kubectl apply -f k8s/volumes/airflow-logs-pv.yaml
kubectl apply -f k8s/volumes/airflow-logs-pvc.yaml


helm install airflow apache-airflow/airflow \
    --namespace airflow -f chart/airflow-override-values.yaml \
    --set-string images.airflow.tag="0.1" \
    --debug


kubectl port-forward svc/airflow-api-server 8080:8080 --namespace airflow