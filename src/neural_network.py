import os
import sys
import numpy as np
from keras.models import Sequential
from keras import optimizers
from keras.layers.core import Activation, Dense, Flatten
from keras.models import model_from_json

import data_generator
import preprocess_data
from pull_library import GENRE_PRECEDNECES

CONFIDENCE_THRESHOLD = 0.6
CULMINATE_GENRE = "pop"
CULMINATE_GENRE_NAMES = []
USE_MODEL = "model"

# Hush hush, TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
np.set_printoptions(suppress=True)
np.set_printoptions(threshold=sys.maxsize)

processor = preprocess_data.DataPreprocessor()
training_input_data = processor.get_input_data()
training_target_data = processor.get_output_data()

validation_input_data = processor.get_validation_input_data()
validation_target_data = processor.get_validation_output_data()


class Network:
    def __init__(self):
        self.model = Sequential()

    def create_model(self):
        self.model.add(Dense(16, input_dim=len(training_input_data[0]), activation='relu'))
        self.model.add(Dense(64, input_dim=16, activation='softmax'))
        self.model.add(Dense(128, input_dim=64, activation='relu'))
        self.model.add(Dense(256, input_dim=128, activation='relu'))
        self.model.add(Dense(128, input_dim=256, activation='relu'))
        self.model.add(Dense(64, input_dim=128, activation='relu'))
        self.model.add(Dense(32, input_dim=64, activation='relu'))
        self.model.add(Dense(16, input_dim=32, activation='relu'))
        self.model.add(Dense(len(GENRE_PRECEDNECES), input_dim=16, activation='relu'))

    def compile_model(self):
        adam = optimizers.Adam(lr=1e-3, decay=1e-6)
        self.model.compile(loss='logcosh', optimizer=adam, metrics=['accuracy'])

    def train_model(self):
        self.model.fit(training_input_data, training_target_data, epochs=1000, verbose=1)

    def predict(self, data):
        self.prediction = self.model.predict(data)
        return self.prediction

    def save_model(self):
        try:
            os.mkdir("models/")
        except OSError:
            print("Unable to create models/ dir")

        model_json = self.model.to_json()
        with open("models/model.json", "w") as json_file:
            json_file.write(model_json)

        self.model.save_weights("models/model.h5")
        print("\nSuccessfully saved model")

    def load_model(self, json_path, h5_path):
        with open(json_path, "r") as json_file:
            loaded_model_json = json_file.read()
            self.model = model_from_json(loaded_model_json)
            self.model.load_weights(h5_path)


def validate_predictions(network):
    prediction = network.predict(validation_input_data)
    expected = processor.get_validation_output_data()
    for (i, val) in enumerate(prediction):
        print("Diff:\n", prediction[i] - expected[i])
        print(prediction[i], "\n", expected[i], "\n")

def in_depth_validate_predictions(network, verbose=False):
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
    prediction = network.predict(validation_input_data)
    expected = processor.get_validation_output_data()
    misslabeled_count = 0
    num_low_confidence = 0

    print(prediction)

    for (i, val) in enumerate(prediction):
        expected_index = 0
        largest = 0
        for (j, v) in enumerate(expected[i]):
            if v > largest:
                largest = v
                expected_index = j
        largest = 0
        prediction_index = 0
        for (j, v) in enumerate(prediction[i]):
            if v > largest:
                largest = v
                prediction_index = j

        # If its confidence is too low, skip it
        if largest < CONFIDENCE_THRESHOLD:
            num_low_confidence += 1
            continue
        elif GENRE_PRECEDNECES[prediction_index] == CULMINATE_GENRE:
            CULMINATE_GENRE_NAMES.append(processor.raw_csv_data.to_numpy()[i][1])
        
        # Determine accuracy
        if prediction_index != expected_index:
            misslabeled_count += 1
            if verbose:
                print(f"Song name: {processor.raw_csv_data.to_numpy()[i][1]}")
                print(f"Guessed: {GENRE_PRECEDNECES[prediction_index]}, expected: {GENRE_PRECEDNECES[expected_index]}")
                print(expected[i])
                print(prediction[i], "\n")
            correct_genre = GENRE_PRECEDNECES[expected_index]
            genre_counts[correct_genre] += 1
    
    num_correct = len(prediction) - misslabeled_count - num_low_confidence
    print(f"\nFOR GENRE {CULMINATE_GENRE}")
    print("\tNUM TO BE ADDED TO PLAYLIST:", len(CULMINATE_GENRE_NAMES))

    print("\nNUM MISSLABELLED:", misslabeled_count)
    print("NUM CORRECT:", num_correct)
    print("TOTAL SONGS:", len(prediction))
    print(f"NUM IGNORED DUE TO LOW CONFIDENCE: {num_low_confidence}")
    print("VALIDATION ACCURACY (WITH HIGH CONFIDENCE):", 100 * num_correct / (len(prediction) - num_low_confidence))

    print("\nTOTAL GENRE COUNTS:", preprocess_data.get_genre_counts())
    print("MISSLABELLED GENRES:", genre_counts)

    print("\nPREDICTED SONGS")
    for s in CULMINATE_GENRE_NAMES:
        print(s)

def main():
    network = Network()

    if sys.argv[1] == "-p":
        print("Using saved prod model")
        network.load_model("models/87.json", "models/87.h5")
        in_depth_validate_predictions(network, True)
    elif sys.argv[1] == "-o":
        print("Using saved old model")
        network.load_model(f"models/{USE_MODEL}.json", f"models/{USE_MODEL}.h5")
        in_depth_validate_predictions(network, True)
    else:
        if sys.argv[1] == "-p":
            print("Unable to find .json or .h5 file.", end=" ")
        print("Training new model")
        network.create_model()
        network.compile_model()
        network.train_model()
        network.save_model()

        print("\n\nUNSEEN DATA")
        print("\nInput:")
        print(validation_input_data)
        print("\nActual:")
        actual = validation_target_data
        print(actual)
        print("\nPrediction:")
        prediction = network.predict(validation_input_data)
        print(prediction)
        print("\nDiff")
        print(actual - prediction)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\033[91mUsage:\033[0m python3 neural_network.py < model_options > < model_to_use > < genre_to_predict >\n\033[93mUse python3 neural_network.py help for more information\033[0m")
        exit()
    elif sys.argv[1] == "help":
        print("\033[93mHelp:\033[0m Use -n to train a new model, use -p to use a pre-trained model (requires .h5 file)")
        exit()

    if len(sys.argv) >= 3:
        USE_MODEL = sys.argv[2]
    if len(sys.argv) == 4:
        CULMINATE_GENRE = sys.argv[3]
    main()
