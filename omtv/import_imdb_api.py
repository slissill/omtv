from imdb import IMDb

def get_json_from_title(title, json_result, instance_imdb):

    try:
        print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print (f"get_json_from_title (api) >>>>>>>>>>>>>>>> {title}")
        print ("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        if instance_imdb == None: ia = IMDb()
        else: ia = instance_imdb

        movies = ia.search_movie(title)
        if not movies: 
            return 2
        
        id = movies[0].getID()
        movie = ia.get_movie(id)
        year = movie['year'] if 'year' in movie else ""
        cover = movie['cover url'] if 'cover url' in movie else ""         
        rating = movie['rating'] if 'rating' in movie else "" 
        director = movie['director'][0]['name'] if 'director' in movie else "" 
        cast = []
        if 'cast' in movie:
            max_actors = 5
            cast = [{'name':actor['name'],} for actor in movie['cast'][:max_actors]]
        json = {"id": id, "year": year, "cover": cover, "rating": rating, "director": director,  "cast": cast} 

        json_result.clear()
        json_result.update(json)
        return 1        
    except Exception as e:        
        print(f"{title} : Une erreur a été déclenchée: {str(e)}")
        return 3
        