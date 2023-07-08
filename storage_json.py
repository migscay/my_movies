from istorage import IStorage
import json
import data_fetcher


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def read_movies(self):
        with open(self.file_path, "r") as movies_json:
            return json.load(movies_json)

    def write_movies(self, movies):
        with open(self.file_path, "w") as movies_json:
            json.dump(movies, movies_json)
