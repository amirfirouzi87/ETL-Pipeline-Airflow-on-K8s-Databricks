from airflow.sdk import DAG
from airflow.providers.databricks.operators.databricks import DatabricksRunNowOperator
from api.yt_vids_data import get_playlist_id, get_video_metadata, extract_video_data, save_to_json_upload_s3
from datetime import timedelta, datetime

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}


with DAG(
    dag_id='get_youtube_videos_metadata_dag',
    default_args=default_args,
    schedule='@hourly',
    start_date=datetime(2025, 11, 20),
    catchup=False,
) as dag:

    playlist_id = get_playlist_id()
    video_metadata = get_video_metadata(playlist_id)
    extracted_data = extract_video_data(video_metadata)
    save_in_json = save_to_json_upload_s3(extracted_data)

    run_databricks_job = DatabricksRunNowOperator(
        task_id='run_transformation_job',
        databricks_conn_id='databricks_default',
        job_id=253944526787423  # Replace with your actual Databricks job ID
    )

    playlist_id >> video_metadata >> extracted_data >> save_in_json >> run_databricks_job