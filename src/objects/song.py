import pandas as pd

class Song:
    def __init__(self, features):
        self.features = features
        self.name = ""
        self.genre = ""

    def to_data_frame(self):
        new_dict = {
            "name" : self.name,
            "genre" : self.genre
        }
        new_dict.update(self.features.raw_data)
        columns = list(self.features.raw_data.keys())
        columns.insert(0, "name")
        columns.insert(1, "genre")
        return pd.DataFrame.from_dict(new_dict, orient='index')
    
    def get_dict(self):
        new_dict = {
            "name" : self.name,
            "genre" : self.genre
        }
        new_dict.update(self.features.raw_data)
        return new_dict