import json


def list_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data.

    For example, the function may return:
    {
      "Grown Ups": {
        "rating": "5.9",
        "year": "2010",
        "poster": "https://m.media-amazon.com/images/M/MV5BMjA0ODYwNzU5Nl5BMl5BanBnXkFtZTcwNTI1MTgxMw@@._V1_SX300.jpg"},
      "..." {
        ...
      },
    }
    """
    with open("movies.json", "r") as movies_json:
        movies = json.load(movies_json)

    return movies


def write_movies(movies):
    """
    writes movies to movies.json file
    """
    with open("movies.json", "w") as movies_json:
        json.dump(movies, movies_json)
