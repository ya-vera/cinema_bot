from datetime import datetime
from urllib.parse import quote
import random
def get_movie_url(movie_name):
    film_ = quote(movie_name)
    url_1 = f"https://www.kinopoisk.ru/index.php?kp_query={film_}"
    url_2 = f"https://premier.one/search?query={film_}"
    url_3 = f"https://okko.tv/search?q={film_}"
    url_4 = f"https://www.ivi.tv/search?q={film_}"
    url_5 = f"https://doramy.club/?s={film_}"

    array = [url_1, url_2, url_3, url_4, url_5]
    return array
def get_movie(url, id, key):
    api_key1 = '343dd4e7-5f76-4328-b0d8-3dd9febbf25f'
    headers = {'X-API-KEY': api_key1, 'accept': 'application/json'}
    response = requests.get(url, headers=headers)
    movies = response.json()[key]
    movie = movies[random.randint(0, len(movies) - 1)]
    id = movie[id]

    url = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}'

    resp = requests.get(url, headers=headers)
    movie = resp.json()
    return movie
def get_random_movie():
    base_url = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/collections?type=TOP_250_MOVIES&page=1'
    id = 'kinopoiskId'
    key = 'items'
    return get_movie(base_url, id, key)
def get_new_movie():
    now = datetime.now()
    current_year = now.year
    base_url = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-filters?yearFrom={current_year}&yearTo={current_year}'
    id = 'filmId'
    key = 'films'
    return get_movie(base_url, id, key)

def get_popular_movie():
    base_url = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/collections?type=TOP_POPULAR_ALL&page=1'
    id = 'kinopoiskId'
    key = 'items'
    return get_movie(base_url, id, key)

import random
import requests

def by_filter_get(rating_low, rating_high, year_from, year_to, genre, country):
    api_key = 'NK0KE17-X0Z4YKE-QWQ5PMA-CS9R2RA'
    headers = {'X-API-KEY': api_key, 'accept': 'application/json'}

    genre = genre.lower()

    if (year_from == ''):
        year = ''
        if (year != ''):
            year = "?year=" + str(year)
        if (rating_low == ''):
            rating_low = '0'
        if (rating_high == ''):
            rating_high = '10'
        if (genre != '' and genre != 'Все'):
            if (year != ''):
                genre = "&genres.name=" + genre
            else:
                genre = "?genres.name=" + genre
        if (country != '' and country != 'Все'):
            if (year == '' and genre == '' or year == '' and genre == 'Все'):
                country = "?countries.name=" + country
            else:
                country = "&countries.name=" + country
        base_url = "https://api.kinopoisk.dev/v1.4/movie" + year + genre + country

        response = requests.get(base_url, headers=headers)
        movies = response.json()

        movies = movies['docs']

        movie = movies[random.randint(0, len(movies) - 1)]
        return movie

    for year in range(year_from, year_to):
        if (year != ''):
            year = "?year=" + str(year)
        if (rating_low == ''):
            rating_low = '0'
        if (rating_high == ''):
            rating_high = '10'
        if (genre != '' and genre != 'Все'):
            if (year != ''):
                genre = "&genres.name=" + genre
            else:
                genre = "?genres.name=" + genre
        if (country != '' and country != 'Все'):
            if (year == '' and genre == '' or year == '' and genre == 'Все'):
                country = "?countries.name=" + country
            else:
                country = "&countries.name=" + country
        base_url = "https://api.kinopoisk.dev/v1.4/movie" + year + genre + country
        response = requests.get(base_url, headers=headers)
        movies = response.json()

        movies = movies['docs']
        if (len(movies) == 0):
            return "Не найдено"
        movie = movies[random.randint(0, len(movies) - 1)]
        return movie

api_key1 = '343dd4e7-5f76-4328-b0d8-3dd9febbf25f'
def get_movie_info(movie_name):
    headers = {'X-API-KEY': api_key1, 'accept': 'application/json'}
    base_url = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword={movie_name}&page=1'
    response = requests.get(base_url, headers=headers)
    movies = response.json()['films']
    movie = movies[0]
    id = movie['filmId']

    url = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{id}'
    resp = requests.get(url, headers=headers)
    movie = resp.json()
    return movie

def show_info_about_movie(movie):
    name = "Название : "
    name += movie['nameRu']
    year_ = f"Год : {movie['year']}"
    type_ = "Жанр : "
    i = 1
    for genre in movie['genres']:
        if i == 1:
            type_ += genre['genre'] + " "
        else:
            type_ += ", " + genre['genre'] + " "
        i += 1
    country_ = "Страна : "
    i = 1
    for country in movie['countries']:
        if i == 1:
            country_ += country['country'] + " "
        else:
            country_ += ", " + country['country'] + " "
        i += 1
    description_ = "Описание : "
    if ('description' in movie and movie['description'] != None):
        description_ += movie['description']
    else:
        description_ += 'Отсутствует'
    rating = "Рейтинг : "
    if (movie['ratingImdb'] != None):
        rating += str(movie['ratingImdb'])
    else:
        rating += 'Отсутствует'
    text__ = name + '\n' + '\n' + year_ + '\n' + '\n' + rating + '\n' + '\n' + type_ + '\n' + '\n' + country_ + '\n' + '\n' + description_ + '\n' + '\n'
    urls = get_movie_url(movie['nameRu'])
    return text__, urls

def show_info_about_movie2(movie):
    name = "Название : "
    name += movie['name']
    year_ = f"Год : {movie['year']}"

    type_ = "Жанр : "
    i = 1
    for genre in movie['genres']:
        if i == 1:
            type_ += genre['name'] + " "
        else:
            type_ += ", " + genre['name'] + " "
        i += 1

    country_ = "Страна : "
    i = 1
    for country in movie['countries']:
        if i == 1:
            country_ += country['name'] + " "
        else:
            country_ += ", " + country['name'] + " "
        i += 1

    description_ = "Описание : "
    if (movie['description'] and movie['description'] != ''):
        description_ += movie['description']
    else:
        description_ += 'Отсутствует'

    rating = "Рейтинг : "
    rating += str(movie['rating']['imdb'])

    text__ = name + '\n' + '\n' + year_ + '\n' + '\n' + rating + '\n' + '\n' + type_ + '\n' + '\n' + country_ + '\n' + '\n' + description_ + '\n' + '\n'
    urls = get_movie_url(movie['name'])
    return text__, urls

