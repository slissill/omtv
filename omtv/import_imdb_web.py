import requests
from datetime import datetime
def get_json_from_title(title, json_result):
    try:
        print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print (f"get_json_from_title (web) >>>> {datetime.now()} >>>>> {title}")
        print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

        id = get_imdb_movie_id(title)
        if id == -1 : return 2

        json = get_imdb_movie_header(id)
        if json == None: return None

        json_actors = get_imdb_movie_actors(id)
        if json_actors != None: json['actors'] = json_actors

        json_result.clear()
        json_result.update(json)

        return 1
    except Exception as e:        
        print(f"{title} : Une erreur a été déclenchée: {str(e)}")
        return 3

def my_imdib_api_key(): return 'a1412b072a662bfa071a119e96d5699d'


def get_imdb_movie_id(title):
    response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={my_imdib_api_key()}&query={title}')
    if response.status_code != 200: return -1
    datas = response.json()
    if not datas['results']: return -1
    return datas['results'][0]['id']


def get_imdb_movie_header(id): 
    response = requests.get(f'https://api.themoviedb.org/3/movie/{id}?api_key={my_imdib_api_key()}')
    if response.status_code != 200: return None
    json_brut = response.json()
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


def get_imdb_movie_actors(id): 
    response = requests.get(f'https://api.themoviedb.org/3/movie/{id}/credits?api_key={my_imdib_api_key()}')
    if response.status_code != 200: return None
    return [actor['name'] for actor in response.json().get('cast', [])][:5]