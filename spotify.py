import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(
    client_id='15c5c210e74d4a68857f725fcc29810d', client_secret='2201177c1efb47768ee8b74faffb0101')

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_link = "https://open.spotify.com/playlist/37i9dQZF1DX5UMwGFV95IS?si=206e8a2350094bd2"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]

for track in sp.playlist_tracks(playlist_URI)["items"]:

    track_id = track["track"]['id']
    track_preview_url = track["track"]["preview_url"]
    track_name = track["track"]["name"]

    if track_preview_url:
        print(track_id, track_preview_url, track_name)
