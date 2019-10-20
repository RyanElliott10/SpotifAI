import os
import numpy as np
from keras.models import Sequential
from keras.layers.core import Activation, Dense
from keras.models import model_from_json

training_data = np.array([[0,0,0,1], [0,0,1,0], [0,1,0,0], [1,0,0,0], [1,0,0,1], [0,0,1,1], [0,1,1,0]], "float32")
target_data = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1], [1,0,0,1], [1,1,0,0], [0,1,1,0]], "float32")

test_data = np.array([[1,0,0,1], [0,0,1,1], [0,1,1,0]])
target_test_data = np.array([[1,0,0,1], [1,1,0,0], [0,1,1,0]])

class Network:

    def __init__(self):
        self.model = Sequential()

    def create_model(self):
        self.model.add(Dense(32, input_dim=4, activation='relu'))
        self.model.add(Dense(16, input_dim=32, activation='relu'))
        self.model.add(Dense(4, activation='sigmoid'))

    def compile_model(self):
        self.model.compile(loss='mean_squared_error', optimizer='adam', metrics=['binary_accuracy'])

    def train_model(self):
        self.model.fit(training_data, target_data, epochs=300, verbose=1)

    def predict(self):
        self.prediction = self.model.predict(test_data)
        return self.prediction

    def save_model(self):
        model_json = self.model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.model.save_weights("model.h5")
        print("Saved model to disk")

    def load_model(self):
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        # load weights into new model
        self.model.load_weights("model.h5")
        print("Loaded model from disk")

def main():
    network = Network()
    
    if os.path.exists("model.json") and os.path.exists("model.h5"):
        print("Using saved model")
        network.load_model()
        network.predict()
    else:
        print("Training new model")
        network.create_model()
        network.compile_model()
        network.train_model()
        network.save_model()

    print("\nPrediction:")
    print(network.predict())

if __name__ == "__main__":
    main()