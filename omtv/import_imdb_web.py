import os
import requests
from datetime import datetime

# Charge la constante de la clé API IMDB
IMDB_API_KEY = os.environ.get('IMDB_API_KEY')


def get_json_from_title(title, json_result, light):
    try:
        print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print (f"get_json_from_title (web) >>>> {datetime.now()} >>>>> {title}")
        print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        id = get_imdb_movie_id(title)
        if id == -1 : return 2

        json = get_imdb_movie_header(id, light)
        if json == None: return None

        json_actors = get_imdb_movie_actors(id, light)
        if json_actors != None: json['actors'] = json_actors

        json_videos = get_imdb_movie_videos(id, light)
        if json_videos != None: json['videos'] = json_videos

        json_result.clear()
        json_result.update(json)

        return 1
    except Exception as e:        
        print(f"{title} : Une erreur a été déclenchée: {str(e)}")
        return 3


def get_imdb_movie_id(title):
    response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={IMDB_API_KEY}&query={title}')
    if response.status_code != 200: return -1
    datas = response.json()
    if not datas['results']: return -1
    return datas['results'][0]['id']


def get_imdb_movie_header(id, light): 
    response = requests.get(f'https://api.themoviedb.org/3/movie/{id}?api_key={IMDB_API_KEY}')
    if response.status_code != 200: return None
    json_brut = response.json()
    if light:
        json_light = {
                            'id': json_brut.get('id'),
                            'imdb_id': json_brut.get('imdb_id'),
                            'release_date': json_brut.get('release_date'),
                            'poster_path': json_brut.get('poster_path'), 
                            'homepage': json_brut.get('homepage'),
                            'origin_country': json_brut.get('origin_country'),
                            'genres': [genre['name'] for genre in json_brut.get('genres', [])],
                            'vote_average': json_brut.get('vote_average'),
                            'vote_count': json_brut.get('vote_count'),
                            'popularity': json_brut.get('popularity'),
                        }    
        return json_light
    else:
        return json_brut


def get_imdb_movie_actors(id, light): 
    response = requests.get(f'https://api.themoviedb.org/3/movie/{id}/credits?api_key={IMDB_API_KEY}')
    if response.status_code != 200: return None
    json_brut = response.json()
    if light:
        json_light = []
        for item in json_brut.get('cast', [])[:5]:
            json_light.append({
                'name': item['name'],
                'character': item['character'],
                'profile_path': item['profile_path']
            })
        return json_light
    else:
        return json_brut

def get_imdb_movie_videos(id, light): 
    response = requests.get(f'https://api.themoviedb.org/3/movie/{id}/videos?api_key={IMDB_API_KEY}')
    if response.status_code != 200: return None
    json_brut = response.json()
    if light:
        json_light = []
        for item in json_brut.get('results', []):
            if item['site'].lower() == 'youtube':
                json_light.append({
                    'name': item['name'],
                    'key': item['key'],
                    'type': item['type']
            })
        return json_light        
    else:
        return json_brut

