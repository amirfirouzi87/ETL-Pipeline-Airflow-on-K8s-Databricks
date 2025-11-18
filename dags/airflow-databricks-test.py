from airflow import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from datetime import datetime

default_args = {
  'owner': 'airflow'
}

with DAG(
    dag_id='databricks_dag',
    default_args=default_args,
    schedule="@weekly",
    start_date=datetime(2021, 3, 14),
    end_date=None,
    catchup=False,
) as dag:

    ingestion = DatabricksRunNowOperator(
        task_id='run_databricks_job',
        databricks_conn_id='databricks_default',
        job_id=817047180012395,  # Replace with your actual Databricks job ID
        notebook_params={"p_data_source": "Param-in-Airflow", "p_file_date": "{{ ds }}"}  # Example of passing parameters to the notebook
    )

    transform = DatabricksRunNowOperator(
        task_id='run_transformation_job',
        databricks_conn_id='databricks_default',
        job_id=11203669573114,  # Replace with your actual Databricks transformation job ID
        notebook_params={"p_file_date": "{{ ds }}"}
    )

    ingestion >> transform