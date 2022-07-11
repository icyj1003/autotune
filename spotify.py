import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from globals import spotify_client_id, spotify_client_secret


def download_playlist(playlist_url, save_dir):
    client_credentials_manager = SpotifyClientCredentials(
        client_id=spotify_client_id, client_secret=spotify_client_secret)

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    playlist_URI = playlist_url.split("/")[-1].split("?")[0]

    for track in sp.playlist_tracks(playlist_URI)["items"]:
        track_id = track["track"]['id']
        track_preview_url = track["track"]["preview_url"]
        track_name = track["track"]["name"]
        if track_preview_url:
            data = requests.get(track_preview_url).content
            with open(save_dir + f'{track_id}.mp3', 'wb') as f:
                f.write(data)


download_playlist(
    playlist_url="https://open.spotify.com/playlist/37i9dQZF1DX4g8Gs5nUhpp?si=1dc519814d884733",
    save_dir='./audio_db/spotify/')
