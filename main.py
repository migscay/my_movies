from storage_json import StorageJson
from storage_csv import StorageCsv
from movie_app import MovieApp
import os.path


def main():
    """
    different users can have different files to store their movies
    ask for the movies file name, as for now csv and json format
    files are catered for
    :return:
    """
    movies_file = input("Enter the name of your movies file: ")
    miguel_movies = ""
    if os.path.isfile(movies_file):
        file, extension = os.path.splitext(movies_file)
        if extension == ".json":
            print("Using JSON file")
            miguel_movies = StorageJson(movies_file)
        elif extension == ".csv":
            print("Using CSV file")
            miguel_movies = StorageCsv(movies_file)
        else:
            print("File format not supported")

        if miguel_movies:
            movie_app = MovieApp(miguel_movies)
            movie_app.run()
        else:
            print("Please type an existing CSV or JSON file")
    else:
        print("File not existing.")


if __name__ == "__main__":
    main()
