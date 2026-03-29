import requests
import json
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="./.env")
API_KEY=os.getenv("API_KEY")
CHANNEL_HANDLE="MrBeast"
maxResults=50

def get_playlist_id():
    try:
        url=f"https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful  
        data = response.json()
        #print(json.dumps(data, indent=4))
        channel_items=data['items'][0]
        channel_playlistId=channel_items['contentDetails']['relatedPlaylists']['uploads']
        #print(channel_playlistId)
        return channel_playlistId
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# base_url= f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&playlistId=UUX6OQ3DkcsbYNE6H8uQQuVA&key=AIzaSyCwrfliF_ELfKxD6bRTN4dRjU1LBKHikz0" 

def get_video_ids(playlist_id):

    video_ids=[]
    page_token=None
    base_url_1= f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlist_id}&key={API_KEY}" 

    try:
        while True:
            url=base_url_1
            if page_token:
                url += f"&pageToken={page_token}"
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful  
            data = response.json()
            #print(json.dumps(data, indent=4))
            items=data['items']
            for item in items:
                video_id=item['contentDetails']['videoId']
                video_ids.append(video_id)
            page_token=data.get('nextPageToken')
            if not page_token:
                break
        print(video_ids)
        return video_ids

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def batch_list(video_id_lst,batch_size):
    for video_id in range(0, len(video_id_lst), batch_size):
        yield video_id_lst[video_id:video_id + batch_size]

def get_extracted_data(video_ids):
    extracted_data=[]
    for batch in batch_list(video_ids, maxResults):
        video_ids_str=','.join(batch)
        url=f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_ids_str}&key={API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful  
            data = response.json()
            #print(json.dumps(data, indent=4))
            items=data['items']
            for item in items:
                video_id=item['id']
                title=item['snippet']['title']
                published_at=item['snippet']['publishedAt']
                view_count=item['statistics'].get('viewCount', 0)
                like_count=item['statistics'].get('likeCount', 0)
                comment_count=item['statistics'].get('commentCount', 0)
                extracted_data.append({
                    'video_id': video_id,
                    'title': title,
                    'published_at': published_at,
                    'view_count': view_count,
                    'like_count': like_count,
                    'comment_count': comment_count
                })
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
    print(extracted_data)
    return extracted_data

if __name__ == "__main__":
    playlist_id=get_playlist_id()
    print(playlist_id)
    get_video_ids(playlist_id)  # Add this line

