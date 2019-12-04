import numpy as np
import pandas as pd
from keras.utils import to_categorical

from pull_library import GENRE_PRECEDNECES

DATA_THRESHOLD = 1000

class DataPreprocessor:
    def __init__(self):
        self.all_input_data = []
        self.all_output_data = []

    def reduce_data(self, raw_data):
        # Removed index, song title, and various features not used as input
        raw_data.drop(raw_data.columns[0], axis=1, inplace=True)
        return raw_data.drop(columns=["name", "mode", "type", "id", "uri", "track_href", "analysis_url", "duration_ms"])

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
        raw_csv_data = pd.read_csv("features.csv")
        reduced = self.reduce_data(raw_csv_data)
        self._get_input_data(reduced)
        return self.all_input_data[:DATA_THRESHOLD]

    # These need to be one encoded
    def get_output_data(self):
        raw_csv_data = pd.read_csv("features.csv").to_numpy()
        raw_labels = raw_csv_data.T[2]
        numerical_labels = []
        for label in raw_labels:
            numerical_labels.append(GENRE_PRECEDNECES.index(label))

        one_hot = to_categorical(numerical_labels)
        self.all_output_data = one_hot
        return self.all_output_data[:DATA_THRESHOLD]

    def get_validation_input_data(self):
        return self.all_input_data[DATA_THRESHOLD:]

    def get_validation_output_data(self):
        return self.all_output_data[DATA_THRESHOLD:]


if __name__ == "__main__":
    processor = DataPreprocessor()
    print("input_data/features:\n", processor.get_input_data())
    print("\noutput_data/labels:\n", processor.get_output_data())
    print("validation input_data/features:\n", processor.get_validation_input_data())
    print("\nvalidation output_data/labels:\n", processor.get_validation_output_data())

# Order of features:
# genre, danceability, energy, key, loudness, mode, speechiness, acousticness, liveness, valence, tempo, duration_ms, time_signature