import requests_with_caching
import json
def get_movies_from_tastedive(title):
    baseurl = 'https://tastedive.com/api/similar'
    params_dict = {}
    params_dict['q'] = title
    params_dict['type'] = 'movies'
    params_dict['limit'] = 5
    resp = requests_with_caching.get(baseurl, params=params_dict, permanent_cache_file="permanent_cache.txt")
    #print(type(resp.json()))
    return resp.json()
# get_movies_from_tastedive("Bridesmaids")
# get_movies_from_tastedive("Black Panther")

def extract_movie_titles(d):
    movie_list = d['Similar']['Results']
    movies = []
    for movie in movie_list:
        if movie['Type'] == "movie":
            movies.append(movie['Name'])
    return movies
# extract_movie_titles(get_movies_from_tastedive("Tony Bennett"))
# extract_movie_titles(get_movies_from_tastedive("Black Panther"))

def get_related_titles(l):
    result_list = []
    for item in l:
        related_movie = get_movies_from_tastedive(item)
        titles = extract_movie_titles(related_movie)
        for title in titles:
            if title not in result_list:
                result_list.append(title)
    return result_list
# get_related_titles(["Black Panther", "Captain Marvel"])
# get_related_titles([])

def get_movie_data(Title):
    baseurl = "http://www.omdbapi.com/"
    param_dict = {}
    param_dict['t'] = Title
    param_dict['r'] = "json"
    resp = requests_with_caching.get(baseurl, params = param_dict, permanent_cache_file="permanent_cache.txt")
    return resp.json()
# get_movie_data("Venom")
# get_movie_data("Baby Mama")

def get_movie_rating(d):
    ratings = d['Ratings']
    for rating in ratings:
        if rating['Source'] == "Rotten Tomatoes":
            return int(rating['Value'].rstrip('%'))
    return 0
# get_movie_rating(get_movie_data("Deadpool 2"))

def get_sorted_recommendations(movie_list):
    sorted_list = []
    movie_rating = {}
    related_movies = get_related_titles(movie_list)
    #print(related_movies)
    for movie in related_movies:
        rating = get_movie_rating(get_movie_data(movie))
        movie_rating[movie] = rating
    #print(movie_rating)
    return(sorted(movie_rating.keys(), key=lambda k:(movie_rating[k],k), reverse=True))
        
# get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])

