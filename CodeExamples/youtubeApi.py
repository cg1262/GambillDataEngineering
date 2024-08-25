import requests 
import requests_oauthlib
import pandas as pd 
import googleapiclient.discovery
import datetime 


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

    video_ids = [item for item in search_response['items']]

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
  return all_videos

def get_channel_stats(api_key, channel_id):
  """Fetches basic channel statistics using the YouTube Data API.

  Args:
    api_key: Your YouTube Data API key.
    channel_id: The ID of the channel to retrieve statistics for.

  Returns:
    A dictionary containing channel statistics.
  """

  youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

  request = youtube.channels().list(
      part="snippet,statistics",
      id=channel_id
  )
  response = request.execute() 


  channel = response['items'][0]
  statistics = channel['statistics']

  return {
      'title': channel['snippet']['title'],
      'subscriber_count': statistics['subscriberCount'],
      'video_count': statistics['videoCount'],
      'view_count': statistics['viewCount']
  }

def get_video_stats_by_date(api_key, video_id, start_date, end_date):
  youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

  request = youtube.reports().query(
      reportId='youtube.videoPerformanceReport',
      startDate=start_date.strftime('%Y-%m-%d'),
      endDate=end_date.strftime('%Y-%m-%d'),
      dimensions='day',
      metrics='views',
      filters=f'video=={video_id}'
  )
  response = request.execute()
  # Process the response data and store it in a suitable format for SQL insertion
  return response

def get_video_ids(api_key, channel_id):
  """Retrieves a list of video IDs for a given channel.

  Args:
    api_key: Your YouTube Data API key.
    channel_id: The ID of the channel to retrieve videos for.

  Returns:
    A list of video IDs.
  """

  youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

  request = youtube.search().list(
      part="snippet",
      channelId=channel_id,
      order="date",
      maxResults=100  # Adjust maxResults as needed
  )
  response = request.execute()
  df = pd.json_normalize(response['items'])
  video_ids = []
  for index,row in df:
    video_ids.append(index)#['id']['videoId']

  # Handle pagination if necessary (check for nextPageToken)

  return video_ids


# Replace with your API key and channel ID
api_key = ""
channel_id = ""

channel_stats = get_channel_stats(api_key, channel_id)
print(channel_stats)

videos = ''#get_all_video_details(api_key, channel_id)
print(videos)

data1 = {'col1': [1, 2], 'col2': [3, 4]}
df1 = pd.DataFrame(data1)

data2 = {'col1': [5, 6], 'col2': [7, 8]}
df2 = pd.DataFrame(data2)

# Concatenate DataFrames
union_df = pd.concat([df1, df2], ignore_index=True)

print(union_df)
