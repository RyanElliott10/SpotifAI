import sys
import numpy as np
import pandas as pd
import random
from keras.utils import to_categorical

from pull_library import GENRE_PRECEDNECES

DATA_THRESHOLD = 0
CSV_FILENAME = "data/training_data.csv"


class DataPreprocessor:
    def __init__(self, csv_name):
        self.all_input_data = []
        self.all_output_data = []
        self.raw_csv_data = pd.read_csv(CSV_FILENAME).sample(frac=1)

    def reduce_data(self, raw_data):
        # Removed index, song title, and various features not used as input
        raw_data.drop(raw_data.columns[0], axis=1, inplace=True)
        return raw_data.drop(columns=["name", "mode", "key", "type", "id", "uri", "track_href", "analysis_url", "duration_ms"])

    def _get_input_data(self, data):
        # Only change is making time_siganture one-hot
        data.drop(data.columns[0], axis=1, inplace=True)
        data = data.to_numpy()

        ts = np.array(data.T[len(data.T)-1], dtype=np.int)

        # Convert to one-hot
        num_values = np.max(ts)+1
        one_hot = np.eye(num_values)[ts]
        
        # Remove previous time_signature, append one-hot form to each element
        data = np.delete(data, len(data[0])-1, axis=1)
        self.all_input_data = np.append(data, one_hot, axis=1)

    def get_input_data(self):
        reduced = self.reduce_data(self.raw_csv_data.copy())
        self._get_input_data(reduced)
        return self.all_input_data[:DATA_THRESHOLD]

    def get_output_data(self):
        raw_csv_data = self.raw_csv_data.to_numpy()
        raw_labels = raw_csv_data.T[2]
        numerical_labels = []
        for label in raw_labels:
            numerical_labels.append(GENRE_PRECEDNECES.index(label))

        one_hot = to_categorical(numerical_labels)
        self.all_output_data = one_hot
        return self.all_output_data[:DATA_THRESHOLD]

    def get_validation_input_data(self):
        self.get_input_data()
        return self.all_input_data[DATA_THRESHOLD:]

    def get_validation_output_data(self):
        self.get_output_data()
        return self.all_output_data[DATA_THRESHOLD:]


def get_genre_counts():
    raw_csv_data = pd.read_csv(CSV_FILENAME)
    genre_counts = {
        "country" : 0,
        "metal" : 0,
        "alternative" : 0,
        "rap" : 0,
        "edm" : 0,
        "jazz" : 0,
        "pop" : 0,
        "rock" : 0,
        "classical" : 0
    }
    for el in raw_csv_data["genre"]:
        genre_counts[el] += 1
    return genre_counts

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        CSV_FILENAME = sys.argv[1]
    print(get_genre_counts())
    # processor = DataPreprocessor()
    # print("input_data/features:\n", processor.get_input_data())
    # print("\noutput_data/labels:\n", processor.get_output_data())
    # print("validation input_data/features:\n", processor.get_validation_input_data())
    # print("\nvalidation output_data/labels:\n", processor.get_validation_output_data())
