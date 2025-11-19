from airflow.sdk import DAG
from api.yt_vids_data import get_playlist_id, get_video_metadata, extract_video_data, save_to_json

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
}


with DAG(
    dag_id='get_youtube_videos_metadata_dag',
    default_args=default_args,
    catchup=False,
) as dag:

    playlist_id = get_playlist_id()
    video_metadata = get_video_metadata(playlist_id)
    extracted_data = extract_video_data(video_metadata)
    save_in_json = save_to_json(extracted_data)
    playlist_id >> video_metadata >> extracted_data >> save_in_json