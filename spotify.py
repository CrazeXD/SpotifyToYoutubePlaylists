from time import sleep
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint

CLIENT_SECRET = r"df2865e5b47d406cb95f2919ef7b9fae"
CLIENT_ID = r"e3ddf1ec45e94213b4f169c9e0e80f61"
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)


def find_tracks(pl_id):
    response = sp.playlist_items(pl_id,
                                    fields='items.track.id,total',
                                    additional_types=['track'])
    print("Initializing tracks...", end="")
    sleep(0.5)
    print(f"Found {len(response['items'])} tracks!")
    pprint(response['items'])
    solution = []
    for response in list(response['items']):
        track_id = response['track']['id']
        track_info = sp.track(track_id)
        track_name = track_info["name"]
        track_artists = [artist["name"] for artist in track_info["artists"]]
        solution.append((track_name, track_artists))
    return solution


if __name__=="__main__":
    find_tracks(pl_id=input())