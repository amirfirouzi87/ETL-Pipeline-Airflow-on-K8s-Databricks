from airflow.sdk import DAG, task
from datetime import datetime

with DAG(
    dag_id="testdag",
    start_date=datetime(2023, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    @task
    def hello_task():
        print("Hello, Airflow!")

    hello_task()