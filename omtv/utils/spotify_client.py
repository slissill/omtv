import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# ⚠️ Remplace par tes propres identifiants Spotify
SPOTIFY_CLIENT_ID = "248302368bd24af4be033b01648ef37a"
SPOTIFY_CLIENT_SECRET = "143ff30095aa4b5899b613c49a823e29"

os.environ["SPOTIPY_CLIENT_ID"] = SPOTIFY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = SPOTIFY_CLIENT_SECRET

# Initialisation du client Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

def get_albums_by_artist(artist_name):
    """Récupère la liste des albums d'un artiste donné"""
    results = sp.search(q=f"artist:{artist_name}", type="artist")
    if not results['artists']['items']:
        return []

    artist_id = results['artists']['items'][0]['id']
    albums = sp.artist_albums(artist_id, album_type='album')
    
    return [
        {"name": album["name"], "image": album["images"][0]["url"] if album["images"] else None}
        for album in albums["items"]
    ]
