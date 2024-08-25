import googleapiclient.discovery
import pandas as pd
def get_all_video_details(api_key, channel_id):
  """Retrieves detailed information for all videos on a channel, handling pagination.

  Args:
    api_key: Your YouTube Data API key.
    channel_id: The ID of the channel to retrieve videos for.

  Returns:
    A list of dictionaries, each containing video details.
  """

  youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

  all_videos = []
  next_page_token = None

  while True:
    search_response = youtube.search().list(
        part="id",
        channelId=channel_id,
        order="date",
        maxResults=50,
        pageToken=next_page_token
    ).execute()
    try: 
        video_ids = pd.json_normalize(search_response["items"])
        try:
           new_pd = pd.concat([video_ids,vid_id2],ignore_index=True)
        except:
            vid_id2 = pd.json_normalize(search_response["items"])
    except Exception as e:
        print(e)
    if not video_ids:
      break

    videos_response = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=','.join(video_ids)
    ).execute()

    all_videos.extend(videos_response['items'])

    next_page_token = search_response.get('nextPageToken')
    if not next_page_token:
      break
  try:    
        return new_pd#all_videos
  except:
        return vid_id2
api_key = "your api key here"
channel_id = "your channel id here"
# Example usage:
all_videos_data = get_all_video_details(api_key, channel_id)