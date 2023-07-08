import random
import statistics
import data_fetcher
import movie_storage
from storage_json import StorageJson


class MovieApp():
    def __init__(self, storage):
        self._storage = storage
        self.movies = {}

    def list_movies(self, movies):
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

    def add_movie(self, movies):
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
        self._storage.write_movies(movies)
        print(f"{new_movie_name} successfully added")

    def delete_movie(self, movies):
        movie_to_delete = input("Enter movie name to delete: ")
        movie_to_be_deleted = ""
        for movie in movies:
            if movie_to_delete.casefold() == movie.casefold():
                movie_to_be_deleted = movie
        try:
            movies.pop(movie_to_be_deleted)
            self._storage.write_movies(movies)
            print(f"Movie {movie_to_delete} successfully deleted")
        except KeyError:
            print(f"Movie {movie_to_delete} doesn't exist!")

    def update_movie(self, movies):
        pass

    def movies_stats(self, movies):
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

    def random_movie(self, movies):
        random_choice_movie = random.choice(list(movies.items()))
        print(f"Your movie for tonight: {random_choice_movie[0]}, it's rated {random_choice_movie[1]['rating']}")

    def search_movies(self, movies):
        movie_search_string = input("Enter part of movie name: ")
        movies_search_result = [key for key, val in movies.items() if movie_search_string.casefold() in key.casefold()]

        for movie in movies_search_result:
            print(f"{movie}, {movies[movie]['rating']}")

    def movies_by_rating(self, movies):
        # sort movies in descending rating
        movies_by_descending_rating = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)

        for movie in movies_by_descending_rating:
            print(f"{movie[0]} {movie[1]['rating']}")

    def _serialize_movie(self, movie_object):
        """
        returns a html formatted string from a movie object
        """
        movie_string = "<li><div class=\"movie\">"
        movie_string += f"<img class=\"movie-poster\" src=\"{movie_object[1]['poster']}\"/>"
        movie_string += f"<div class=\"movie-title\">{movie_object[0]}</div>"
        movie_string += f"<div class=\"movie-year\">{movie_object[1]['year']}</div>"
        movie_string += "</li>"

        return movie_string

    def generate_web_page(self, movies):
        from pathlib import Path
        __HTML_TITLE_PLACEHOLDER__ = '__TEMPLATE_TITLE__'
        __HTML_MOVIE_GRID_PLACEHOLDER__ = '__TEMPLATE_MOVIE_GRID__'
        __MOVIE_APP_TITLE__ = 'My favourite movies'
        __STATIC_FOLDER__ = Path("_static/")
        __TEMPLATE_FILE__ = __STATIC_FOLDER__ / "index_template.html"
        __WEB_PAGE__ = __STATIC_FOLDER__ / "index.html"

        movie_data_string = ""

        for movie in movies.items():
            movie_data_string += self._serialize_movie(movie)

        if not movie_data_string:
            movie_data_string = f"<h2>No movie in file.</h2>"

        with open(__TEMPLATE_FILE__, "r") as template_file:
            template_data = template_file.read()

        new_html_data1 = template_data.replace(__HTML_TITLE_PLACEHOLDER__, __MOVIE_APP_TITLE__)
        new_html_data = new_html_data1.replace(__HTML_MOVIE_GRID_PLACEHOLDER__, movie_data_string)

        with open(__WEB_PAGE__, "w") as html_file:
            html_file.write(new_html_data)

        print("Website was successfully generated.")

    def get_menu_choice(self):
        menu_items = ["0: Exit", "1: List movies", "2: Add movie", "3: Delete movie", "4: Update movie", "5: Stats",
                      "6: Random movie",
                      "7: Search movie", "8: Movies sorted by rating", "9: Generate Website"]

        print("Menu:")
        for choice in menu_items:
            print(choice)

        user_choice = int(input("Enter choice (0-9): "))

        return user_choice

    def execute_menu_choice(self, user_choice, movies):
        menu_functions = {
            1: self.list_movies,
            2: self.add_movie,
            3: self.delete_movie,
            4: self.update_movie,
            5: self.movies_stats,
            6: self.random_movie,
            7: self.search_movies,
            8: self.movies_by_rating,
            9: self.generate_web_page
        }

        if user_choice in menu_functions:
            print("")
            menu_functions[user_choice](movies)

    def run(self):
        movies = self._storage.read_movies()

        print("********** My Movies Database **********\n")

        while True:
            user_choice = self.get_menu_choice()

            if user_choice == 0:
                print("Bye!")
                break

            self.execute_menu_choice(user_choice, movies)

            input("\nPress enter to continue\n")


def main():
    miguel_movies = StorageJson('movies.json')
    movie_app = MovieApp(miguel_movies)
    movie_app.run()


if __name__ == "__main__":
    main()
