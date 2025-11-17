helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm show values apache-airflow/airflow > airflow-values.yaml


docker build --pull --tag my-airflow-image:0.1 -f CICD/Dockerfile .

kubectl create namespace airflow

helm install airflow apache-airflow/airflow \
    --namespace airflow -f chart/airflow-override-values.yaml