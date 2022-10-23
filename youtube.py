from youtubesearchpython import VideosSearch
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

def get_youtube_keywords(data): #Collective data
    #Parse data
    keywords = []
    for song in data:
        song_search = song[0]
        for i in song[1]:
            song_search += f" {i}" 
        keywords.append(song_search)
    return keywords

def open_url_first_result(keywords): #Individual song keywords
    
    videosearch = VideosSearch(keywords, limit=1)
    return videosearch.result()

def add_to_playlist(link, playlist_id, youtube): #individual items
    #Request body
    body = dict(
        snippet=dict(
            playlistId = playlist_id,
            resourceId = dict(
                kind='youtube#video',
                videoId=link.rsplit("=")[1])
        )
    )
    #Request execution
    playlists_insert_response = youtube.playlistItems().insert(part='snippet', body=body).execute()
    print(f"Playlist Resource: {playlists_insert_response}")
if __name__ == "__main__":
    import spotify

    data = spotify.find_tracks(input())
    print("Searching for songs now...")
    song_data = get_youtube_keywords(data)
    song_data = [open_url_first_result(song) for song in song_data]
    print(song_data)
    for index, i in enumerate(song_data):
        song_data[index] = i['result'][0]['link']
    print("Found all songs! Attempting to add to playlist...")

    SCOPES = ['https://www.googleapis.com/auth/youtube']
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'
    CLIENT_SECRETS_FILE = 'client_data.json'
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
    playlist_title = input("Enter a playlist title: ")
    body = dict (
        snippet=dict(
            title=playlist_title,
            description=""
        ),
        status=dict(
            privacyStatus='private'
        ) 
    ) 

    playlists_insert_response = youtube.playlists().insert(
        part='snippet,status',
        body=body
    ).execute()
    print(f"New playlist ID: {playlists_insert_response['id']}")
    playlist_id = playlists_insert_response['id']
    add_to_playlist(song_data[0], playlist_id, youtube)


