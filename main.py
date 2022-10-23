from spotify import *
from youtube import *

data = find_tracks(input("Enter a Spotify Playlist link: "))
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
print("---------------------------------------------------------------------------------------")
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
for song in song_data:
    add_to_playlist(song, playlist_id, youtube)
print("Completed!")