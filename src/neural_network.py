import os
import sys
import numpy as np
from keras.models import Sequential
from keras import optimizers
from keras.layers.core import Activation, Dense, Flatten
from keras.layers import Conv1D, MaxPooling1D
from keras.models import model_from_json

import data_generator
import preprocess_data

# Hush hush, TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
np.set_printoptions(suppress=True)

processor = preprocess_data.DataPreprocessor()
training_input_data = processor.get_input_data()
training_target_data = processor.get_output_data()

print(training_input_data)

validation_input_data = processor.get_validation_input_data()
validation_target_data = processor.get_validation_output_data()


class Network:
    def __init__(self):
        self.model = Sequential()

    def create_model(self):
        self.model.add(Dense(32, input_dim=len(training_input_data[0]), activation='relu'))
        self.model.add(Dense(128, input_dim=32, activation='sigmoid'))
        self.model.add(Dense(64, input_dim=128, activation='relu'))
        self.model.add(Dense(64, input_dim=64, activation='sigmoid'))
        self.model.add(Dense(11, input_dim=64, activation='sigmoid'))

    def compile_model(self):
        adam = optimizers.Adam(lr=1e-3, decay=1e-6)
        self.model.compile(loss='mean_squared_error', optimizer=adam, metrics=['accuracy'])

    def train_model(self):
        self.model.fit(training_input_data, training_target_data, epochs=1000, verbose=1)

    def predict(self):
        self.prediction = self.model.predict(validation_input_data)
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

    def load_model(self):
        with open("models/model.json", "r") as json_file:
            loaded_model_json = json_file.read()
            self.model = model_from_json(loaded_model_json)
            self.model.load_weights("models/model.h5")


def main():
    network = Network()
    
    if sys.argv[1] == "-p" and os.path.exists("models/model.json") and os.path.exists("models/model.h5"):
        print("Using saved model")
        network.load_model()
        network.predict()
    else:
        if sys.argv[1] == "-p":
            print("Unable to find .json or .h5 file.", end=" ")
        print("Training new model")
        network.create_model()
        network.compile_model()
        network.train_model()
        network.save_model()

    print(network.model.summary())
    print("\nSEEN DATA")
    print("\nInput:")
    print(training_input_data[len(validation_input_data)-1])
    print("\nActual:")
    actual = training_target_data[len(validation_target_data)-1]
    print(actual)
    print("\nPrediction:")
    prediction = network.predict()[len(validation_target_data)-1]
    print(prediction)
    print("\nDiff")
    print(actual - prediction)

    print("\n\nUNSEEN DATA")
    print("\nInput:")
    print(validation_input_data[len(validation_input_data)-1])
    print("\nActual:")
    actual = validation_target_data[len(validation_target_data)-1]
    print(actual)
    print("\nPrediction:")
    prediction = network.predict()[len(validation_target_data)-1]
    print(prediction)
    print("\nDiff")
    print(actual - prediction)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\033[91mUsage:\033[0m python3 neural_network.py <model_options>\n\033[93mUse python3 neural_network.py help for more information\033[0m")
        exit()
    elif sys.argv[1] == "help":
        print("\033[93mHelp:\033[0m Use -n to train a new model, use -p to use a pre-trained model (requires .h5 file)")
        exit()
    main()
