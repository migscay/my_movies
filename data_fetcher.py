import requests
from requests.exceptions import ConnectionError


def fetch_data(movie_title):
    """
    Fetches the animals data via API
    returns a list of dictionaries, each dictionary
    refers to an animal
    """
    __API_MOVIE_URL__ = 'https://www.omdbapi.com/?apikey=8252a1ec&t='

    url_get_request = __API_MOVIE_URL__ + movie_title
    movie_details = {}
    try:
        res = requests.get(url_get_request)
        movie_details = res.json()
    except ConnectionError as e:
        print(f"Check internet connection.")

    return movie_details
