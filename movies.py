import data_fetcher
import movie_storage


# List movies
def list_movies(movies):
    movie_list = movies.items()
    movie_count = len(movie_list)
    print(f"{movie_count} movies in total")

    for movie in movies.items():

        try:
            movie_rating = movie[1]['rating']
        except KeyError:
            movie_rating = ""

        try:
            movie_year = movie[1]['year']
        except KeyError:
            movie_year = ""

        print(f"{movie[0]}: {movie_rating} Year: {movie_year}")


def add_movie(movies):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    new_movie_name = input("Enter new movie name: ")
    if new_movie_name in movies:
        print(f"Movie {new_movie_name} already exist!")
        return

    movie_data = data_fetcher.fetch_data(new_movie_name)
    try:
        if movie_data['Response'] == 'False':
            print(f"{new_movie_name} not an existing movie.")
            return
    except KeyError:
        print("Something went wrong in getting the movie details.")
        return

    new_movie_name = movie_data['Title']
    try:
        new_movie_year = movie_data['Year']
    except KeyError:
        new_movie_year = ""
    try:
        new_movie_rating = movie_data['imdbRating']
    except KeyError:
        new_movie_rating = ""
    try:
        new_movie_poster_url = movie_data['Poster']
    except KeyError:
        new_movie_poster_url = ""

    movies[new_movie_name] = {}
    movies[new_movie_name]['rating'] = new_movie_rating
    movies[new_movie_name]['year'] = new_movie_year
    movies[new_movie_name]['poster'] = new_movie_poster_url
    movie_storage.write_movies(movies)
    print(f"{new_movie_name} successfully added")


# Delete a movie
def delete_movie(movies):
    movie_to_delete = input("Enter movie name to delete: ")
    movie_to_be_deleted = ""
    for movie in movies:
        if movie_to_delete.casefold() == movie.casefold():
            movie_to_be_deleted = movie
            print(f"Movie {movie_to_delete} successfully deleted")
    try:
        movies.pop(movie_to_be_deleted)
        movie_storage.write_movies(movies)
    except KeyError:
        print(f"Movie {movie_to_delete} doesn't exist!")


# Update a movie
def update_movie(movies):
    movie_to_update = input("Enter movie name: ")
    if movie_to_update not in movies:
        print(f"Movie {movie_to_update} doesn't exist!")
    else:
        new_movie_rating = float(input("Enter new movie rating (0-10): "))
        movies[movie_to_update]['rating'] = new_movie_rating
        movie_storage.write_movies(movies)

        print(f"Movie {movie_to_update} successfully updated")


# List movies stats
def movies_stats(movies):
    """

    :param movies:
    :return:
    """

    movie_ratings_list = [float(movie['rating']) for movie in movies.values()]

    # Average rating
    print(f"Average rating: {sum(movie_ratings_list) / float(len(movie_ratings_list))}")

    # Median rating
    print(f"Median rating: {statistics.median(movie_ratings_list)}")

    # Best movie
    movies_by_descending_rating = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
    best_rating = movies_by_descending_rating[0][1]['rating']
    # print movies with the best rating
    for movie in movies_by_descending_rating:
        if movie[1]['rating'] == best_rating:
            print(f"Best movie: {movie[0]}, {best_rating}")

    # Worst movie
    movies_by_ascending_rating = sorted(movies.items(), key=lambda x: x[1]['rating'])
    worst_rating = movies_by_ascending_rating[0][1]['rating']
    # print movies with the worst rating
    for movie in movies_by_ascending_rating:
        if movie[1]['rating'] == worst_rating:
            print(f"Worst movie: {movie[0]}, {worst_rating}")


# Choose a random movie
def random_movie(movies):
    random_choice_movie = random.choice(list(movies.items()))
    print(f"Your movie for tonight: {random_choice_movie[0]}, it's rated {random_choice_movie[1]['rating']}")


# Search for a movie
def search_movies(movies):
    movie_search_string = input("Enter part of movie name: ")
    movies_search_result = [key for key, val in movies.items() if movie_search_string.casefold() in key.casefold()]

    for movie in movies_search_result:
        print(f"{movie}, {movies[movie]['rating']}")


# List movies sorted by rating
def movies_by_rating(movies):
    # sort movies in descending rating
    movies_by_descending_rating = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)

    for movie in movies_by_descending_rating:
        print(f"{movie[0]} {movie[1]['rating']}")


def serialize_movie(movie_object):
    """
    returns a html formatted string from an movie object
    :param movie_object:
    """
    movie_string = "<li><div class=\"movie\">"
    movie_string += f"<img class=\"movie-poster\" src=\"{movie_object[1]['poster']}\"/>"
    movie_string += f"<div class=\"movie-title\">{movie_object[0]}</div>"
    movie_string += f"<div class=\"movie-year\">{movie_object[1]['year']}</div>"
    movie_string += "</li>"

    return movie_string


# Generate Website
def generate_web_page(movies):
    from pathlib import Path
    __HTML_TITLE_PLACEHOLDER__ = '__TEMPLATE_TITLE__'
    __HTML_MOVIE_GRID_PLACEHOLDER__ = '__TEMPLATE_MOVIE_GRID__'
    __MOVIE_APP_TITLE__ = 'My favourite movies'
    __STATIC_FOLDER__ = Path("_static/")
    __TEMPLATE_FILE__ = __STATIC_FOLDER__ / "index_template.html"
    __WEB_PAGE__ = __STATIC_FOLDER__ / "index.html"

    movie_data_string = ""

    for movie in movies.items():
        movie_data_string += serialize_movie(movie)

    if not movie_data_string:
        movie_data_string = f"<h2>No movie in file.</h2>"

    with open(__TEMPLATE_FILE__, "r") as template_file:
        template_data = template_file.read()

    new_html_data1 = template_data.replace(__HTML_TITLE_PLACEHOLDER__, __MOVIE_APP_TITLE__)
    new_html_data = new_html_data1.replace(__HTML_MOVIE_GRID_PLACEHOLDER__, movie_data_string)

    with open(__WEB_PAGE__, "w") as html_file:
        html_file.write(new_html_data)

    print("Website was successfully generated.")


# display menu choices and get user choice
def get_menu_choice():
    menu_items = ["0: Exit", "1: List movies", "2: Add movie", "3: Delete movie", "4: Update movie", "5: Stats", "6: Random movie",
                  "7: Search movie", "8: Movies sorted by rating", "9: Generate Website"]

    print("Menu:")
    for choice in menu_items:
        print(choice)

    user_choice = int(input("Enter choice (0-9): "))

    return user_choice


def execute_menu_choice(user_choice, movies):
    menu_functions = {
        1: list_movies,
        2: add_movie,
        3: delete_movie,
        4: update_movie,
        5: movies_stats,
        6: random_movie,
        7: search_movies,
        8: movies_by_rating,
        9: generate_web_page
    }

    if user_choice in menu_functions:
        print("")
        menu_functions[user_choice](movies)


def main():
    movies = movie_storage.list_movies()

    print("********** My Movies Database **********\n")

    while True:
        user_choice = get_menu_choice()

        if user_choice == 0:
            print("Bye!")
            break

        execute_menu_choice(user_choice, movies)

        input("\nPress enter to continue\n")


if __name__ == "__main__":
    import random
    import statistics

    main()
