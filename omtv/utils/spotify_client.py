import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os


#pip install spotipy

SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

os.environ["SPOTIPY_CLIENT_ID"] = SPOTIFY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = SPOTIFY_CLIENT_SECRET


# Initialisation du client Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())


def get_infos_artist(artist_name):
    """Récupère les infos de l'artiste et la liste de ses albums"""
    results = sp.search(q=f"artist:{artist_name}", type="artist")
    if not results['artists']['items']:
        return {"artist": None, "albums": []}

    artist = results['artists']['items'][0]
    artist_id = artist['id']
    artist_name = artist['name']
    artist_image = artist['images'][0]['url'] if artist['images'] else None

    albums = sp.artist_albums(artist_id, album_type='album')
    albums_info = [
        {
            "id": album["id"],  
            "name": album["name"], 
            "image": album["images"][0]["url"] if album["images"] else None, 
            "release_date": album["release_date"]
        }
        for album in albums["items"]
    ]
    
    return {
    "artist": {"id": artist_id, "name": artist_name, "image": artist_image },
    "albums": albums_info
    }

def get_tracks_by_album(album_id):
    """Récupère la liste des pistes d'un album donné"""
    results = sp.album_tracks(album_id)
    
    return [
        {
            "id": track["id"], 
            "name": track["name"], 
            "duration_ms": track["duration_ms"] //1000, 
            "preview_url": track["preview_url"], 
            }  
        for track in results["items"]
    ]