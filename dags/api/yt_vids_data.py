import requests
import json
from datetime import date

from airflow.sdk import task, Variable


CHANNEL_HANDLE = "TheDataGuyOfficial"
API_KEY = Variable.get("API_KEY")

max_results = 50

@task
def get_playlist_id():

    try:

        url  = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

        response = requests.get(url)

        playlist_id = response.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        return playlist_id
    
    except requests.exceptions.RequestException as e:
        raise e
    


@task
def get_video_metadata(playlist_id):

    main_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={API_KEY}"

    video_ids = []
    page_token = None

    try:
        while True:
            
            if page_token:
                url = f"{main_url}&pageToken={page_token}"
            else:
                url = main_url
            
            response = requests.get(url)

            video_ids.extend(item['contentDetails']['videoId'] for item in response.json().get('items', []))

            page_token = response.json().get('nextPageToken')

            if not page_token:
                break

        return video_ids

    except requests.exceptions.RequestException as e:
        raise e

@task
def extract_video_data(video_ids):
    extracted_data = []

    def batch_list(video_id_lst, batch_size):
        for i in range(0, len(video_id_lst), batch_size):
            yield video_id_lst[i:i + batch_size]


    try:
        for batch in batch_list(video_ids,max_results):
            video_ids_str = ",".join(batch)
            url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"
            response = requests.get(url)

            for item in response.json().get('items', []):
                
                video_data = {
                    'video_id': item['id'],
                    'title': item['snippet']['title'],
                    'published_at': item['snippet']['publishedAt'],
                    'duration': item['contentDetails']['duration'],
                    'view_count': item['statistics']['viewCount'],
                    'like_count': item['statistics']['likeCount'],
                    'comment_count': item['statistics']['commentCount']
                }
                extracted_data.append(video_data)

        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e


@task
def save_to_json(extracted_data):
    file_path = f"./data/YT_data_{date.today()}.json"

    with open(file_path, 'w', encoding='utf-8') as json_outfile:
        json.dump(extracted_data, json_outfile, ensure_ascii=False, indent=4)