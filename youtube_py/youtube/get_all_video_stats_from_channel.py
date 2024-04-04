import requests
import math
import threading

def all_videos_from_channel(channel_id):
    print("Fetching all videos from channel...")
    get_channel_info = f"https://yt.lemnoslife.com/noKey/channels?id={channel_id}&part=contentDetails" 
    response = requests.get(get_channel_info)
    uploads_id = response.json()['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    get_videos_url = f"https://yt.lemnoslife.com/noKey/playlistItems?playlistId={uploads_id}&part=snippet&maxResults=800"
    response = requests.get(get_videos_url)
    next_page_token = response.json().get('nextPageToken')
    total_results = response.json()['pageInfo']['totalResults']

    total_pages = math.ceil(total_results / 50)

    all_videos = response.json()['items']

    for page in range(1, total_pages):
        next_page_url = f"{get_videos_url}&pageToken={next_page_token}"
        response = requests.get(next_page_url)
        next_page_token = response.json().get('nextPageToken')
        all_videos += response.json()['items']

    print(f"Total of {len(all_videos)} videos fetched.")
    return all_videos

def chunk_list(lst, chunk_size):
    """
    Split a list into chunks of specified size.
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def get_video_stats_for_chunk(chunk, url_with_ids_appended, all_videos_data):
    """
    Fetch video statistics for a chunk of video IDs.
    """
    response = requests.get(url_with_ids_appended)
    response_json = response.json()
    videos = response_json['items']
    all_videos_data += videos

def get_all_video_stats(all_videos):
    print("Extracting all video ids...")

    get_videos_info_url="https://yt.lemnoslife.com/noKey/videos?part=snippet,statistics"
    all_videos_ids = [video['snippet']['resourceId']['videoId'] for video in all_videos]
    chunked_video_ids = chunk_list(all_videos_ids, 25)

    print(f"Total of {len(all_videos_ids)} video ids extracted...")

    all_videos_data = []
    threads = []

    print("Starting to fetch video statistics...")
    for i, chunk in enumerate(chunked_video_ids):
        url_with_ids_appended = f"{get_videos_info_url}&id={','.join(chunk)}"
        thread = threading.Thread(target=get_video_stats_for_chunk, args=(chunk, url_with_ids_appended, all_videos_data))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print(f"Total of {len(all_videos_data)} videos fetched.")
    return all_videos_data 

def get_all_video_stats_from_channel(channel_id: str):
    try:
        all_videos = all_videos_from_channel(channel_id)
        all_videos_with_stats = get_all_video_stats(all_videos)
        return {
            "all_video_stats": all_videos_with_stats,
            "status": "success",
            "message": "All video stats fetched successfully."
        }
    except Exception as e:
        print("An error occurred.")
        with open("erorr.txt", "w") as f:
            f.write(str(e))

        return {
            "status": "error",
            "message": "An error occurred. Please check errorr.txt for more details.",
            "error": str(e),
        }
