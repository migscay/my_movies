from istorage import IStorage
import csv


class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def read_movies(self):
        movies = {}
        movie_title = ''
        movie_detail = {}
        with open(self.file_path, 'r') as movies_csv:
            for line in csv.DictReader(movies_csv):
                if movie_title:
                    movies[movie_title] = movie_detail

                for key, value in line.items():
                    if key == 'title':
                        movie_title = value
                        movie_detail = {}
                    else:
                        movie_detail[key] = value

            if movie_title:
                movies[movie_title] = movie_detail

        return movies

    def write_movies(self, movies):
        fields = ["title", "rating", "year", "poster"]

        with open(self.file_path, "w+", newline="\n", encoding='UTF8') as movies_csv:
            writer = csv.writer(movies_csv)

            writer.writerow(fields)

            # Write the data
            movies_data = []
            data = []

            if len(movies) > 0:
                for movie_title, movie_details_dict in movies.items():

                    data = [movie_title]

                    for movie_details in movie_details_dict.values():
                        data.append(movie_details)

                    movies_data.append(data)

            writer.writerows(movies_data)
