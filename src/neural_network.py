import os
import sys
import numpy as np
from keras.models import Sequential
from keras.layers.core import Activation, Dense
from keras.models import model_from_json

# Hush hush, TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

training_data = np.array([[0,0,0,1], [0,0,1,0], [0,1,0,0], [1,0,0,0], [1,0,0,1], [0,0,1,1], [0,1,1,0]], "float32")
target_data = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1], [1,0,0,1], [1,1,0,0], [0,1,1,0]], "float32")

test_data = np.array([[1,0,0,1], [0,0,1,1], [0,1,1,0]])
target_test_data = np.array([[1,0,0,1], [1,1,0,0], [0,1,1,0]])

class Network:

    def __init__(self):
        self.model = Sequential()

    def create_model(self):
        self.model.add(Dense(32, input_dim=4, activation='tanh'))
        self.model.add(Dense(16, input_dim=32, activation='relu'))
        self.model.add(Dense(4, activation='sigmoid'))

    def compile_model(self):
        self.model.compile(loss='mean_squared_error', optimizer='adam', metrics=['binary_accuracy'])

    def train_model(self):
        self.model.fit(training_data, target_data, epochs=300, verbose=3)

    def predict(self):
        self.prediction = self.model.predict(test_data)
        return self.prediction

    def save_model(self):
        model_json = self.model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)

        self.model.save_weights("model.h5")
        print("\nSuccessfully saved model")

    def load_model(self):
        with open("model.json", "r") as json_file:
            loaded_model_json = json_file.read()
            self.model = model_from_json(loaded_model_json)
            self.model.load_weights("model.h5")

def main():
    network = Network()
    
    if sys.argv[1] == "-p" and os.path.exists("model.json") and os.path.exists("model.h5"):
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

    print("\nPrediction:")
    print(network.predict())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\033[91mUsage:\033[0m python3 neural_network.py <model_options>\n\033[93mUse python3 neural_network.py help for more information\033[0m")
        exit()
    elif sys.argv[1] == "help":
        print("\033[93mHelp:\033[0m Use -n to train a new model, use -p to use a pre-trained model (requires .h5 file)")
        exit()
    main()