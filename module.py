from googleapiclient.discovery import build

# api_key = "AIzaSyAgTu4Qkv8Ywvz9G1JpqWkP0qAsjkd4Xdg"
# api_key = "AIzaSyBfKYXY-Tw7bNv-3d1fIr0lkZKS7Fj8Rlc"
# api_key = "AIzaSyBnBB7bftIfpBkz8oZAjEFQje_Vkg3Bcko"
# api_key = "AIzaSyBynMSluOg1PXuKPsytlTPo1fqgkqEOIsY"
api_key = "AIzaSyDmsvIOn5_Y0xBxUhLn7nWHNJRnSBWcuIY"

youtube = build('youtube', 'v3', developerKey=api_key)

def channel_search(query):
    request = youtube.search().list(
        part='snippet',
        q=query,
        type='channel',
        maxResults=5
    )
    return request.execute()

def channel_videos(channel_id, next_page_token):
    request = youtube.search().list(
        q='歌ってみた',
        part='snippet',
        type='video',
        channelId=channel_id,
        pageToken=next_page_token,
        maxResults=50,
        fields="items(id/videoId,snippet(title)),nextPageToken"
    )
    return request.execute()

def video_detail(video_id):
    request = youtube.videos().list(
        part='snippet,statistics,contentDetails',
        id=video_id,
        fields="items(snippet(title,description,thumbnails,channelId,channelTitle,publishedAt),statistics(viewCount),contentDetails(duration))"
    )
    return request.execute()