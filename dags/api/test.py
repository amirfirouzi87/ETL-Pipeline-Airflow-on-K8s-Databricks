import requests
import json
from datetime import datetime


CHANNEL_HANDLE = "irantalks"
API_KEY = "AIzaSyDti7f8Cvo4T-XByekEHFKkFH0aGsdS0sI"

max_results = 50


# def get_playlist_id():
#     CHANNEL_HANDLE = "irantalks"
#     API_KEY = "AIzaSyDti7f8Cvo4T-XByekEHFKkFH0aGsdS0sI"
#     try:

#         url  = f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"

#         response = requests.get(url)

#         playlist_id = response.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']
#         return playlist_id
    
#     except requests.exceptions.RequestException as e:
#         raise e
    
# if __name__ == "__main__":
#     print(get_playlist_id())


# def get_video_metadata(playlist_id):
#     max_results = 50
#     playlist_id = "UUS2Zt54GTkLbKDiJGQR-JUw"
#     main_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlist_id}&key={API_KEY}"

#     video_ids = []
#     page_token = None

#     try:
#         while True:
            
#             if page_token:
#                 url = f"{main_url}&pageToken={page_token}"
#             else:
#                 url = main_url
            
#             response = requests.get(url)

#             video_ids.extend(item['contentDetails']['videoId'] for item in response.json().get('items', []))

#             page_token = response.json().get('nextPageToken')

#             if not page_token:
#                 break

#         return video_ids

#     except requests.exceptions.RequestException as e:
#         raise e

# if __name__ == "__main__":
#     print(get_video_metadata("UUS2Zt54GTkLbKDiJGQR-JUw"))

def extract_video_data():
    extracted_data = []
    video_ids = ['plEbM0umX3k', 'WZzbGPH0O5E', '9YTgL-4DPxg', '239arhS6Ws0', '1NOghc3h6RI', 'C1vjK-azVIo', 'KZnWGU3SWSA', '-2JuTQkg2vI', 'P51nTiFpMtg', 'GaLXaJ7dj6I', 'FI74SZg9Ciw', 'GCcFDve1tqg', 'crmpEwgt7oo', '7pZnmkpQVnY', 'TOHYr5yqKeg', 'vu83TMixmlw', 'NdEtUmjhkE8', 'RSQFhN_RF0c', 'aPneWXGq84U', 'a7nDQYj61bE', 'vk9KEkReSrU', '6RkauJQjGG4', 'RXKJwIciKwo', 'WNGMreWRctc', '8fsR6wkE0p4', 'gA-_5YdHIP4', 'ATtfoyXAyak', 'GZVBphzIR7A', '-7UmsBAZv5E', 'xIXiOry1h6E', 'JlSnGiMexbA', '8P-k4ZP-nlE', 'dH_rCizHHCg', 'LVWNiXtzedA', 'SEvXaWDWK_s', 'crB_UOj6MVY', 'G8NsTvTb3l4', 'ue3x6zi7I-I', 'slasF2_sYwo', '_rxHMS7rb9Q', '29V0XXeNgv0', 'mauToijH04A', '_6vI4b5m07s', 'rbu0qpZaMtE', '1YHzRnQ7cOc', 'Dv4j4FWADos', 'hVn0JypXS28', 'x-okRU2wtjo', 'OZHsOYyM8uE', 'BAh8PmTgF5w', 'RzjDPRYzUh0', 'ODtq09ox2pM', 't5-YeSrv2T0', 'oZ5XwlwJrp8', 'FfW3mSNB2SU', 'kcZ1AoHKhcI', 'LDpK7qtYk9E', 'WeCJQ7wtHTE', 'ERgHXda6VMA', 'PvnVC4nYoI0', 'SIo4Jy58Oj4', 'vALYKHClNU4', 'hXLIpUljWGo', 'HCA0TIVesb8', 'rzrssJtcxM4', 'vODBm1luy3w', 'rvl6qIiy7k0', 'sxXDchFGou4', 'wvkNOTQDP6o', 'bL1_GhfAAAA', 'XlSdsXKjZ_U', '-OMbcZ36b2k', 'om9RqFnDcSE', 'aVVA4MtJZuo', 'TU9dnYxcY6k', 'fANGyqCvZLE', 'Q19c6vU69FQ', 'eRH_K6AXxuY', 'V6HPAyse-2U', 'Ki4SvvoyMzc', '8xTrXtpYKls', 'uy9spwDXbrM', '5XJm_blhwFU', 'ZaOKNvXfXyI', 'T_ADaw4_ii0', 'Mej3aQEDy64', 'Saqeif6dBs0', '2yIgfClogZ8', 'h86f_b8Q55o', 'aHO4x-V9hXw', 'eNziqP36RQY', '6NgR-L9lwUY']
    def batch_list(video_id_lst, batch_size):
        for i in range(0, len(video_id_lst), batch_size):
            yield video_id_lst[i:i + batch_size]


    try:
        for batch in batch_list(video_ids,max_results):
            video_ids_str = ",".join(batch)
            # print(video_ids_str)
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

if __name__ == "__main__":
    print(extract_video_data())
# def save_to_json_upload_s3(extracted_data):

#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
#     file_name = f"YT_data_{timestamp}.json"
#     file_path = f"/tmp/{file_name}"    

#     with open(file_path, 'w', encoding='utf-8') as json_outfile:
#         json.dump(extracted_data, json_outfile, ensure_ascii=False, indent=4)

#     s3 = S3Hook(aws_conn_id='s3_conn')
#     s3.load_file(
#         filename=file_path,
#         key=file_name,
#         bucket_name="youtubeetl852147",
#         replace=True
#     )
#     return file_name