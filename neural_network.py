import numpy as np
from keras.models import Sequential
from keras.layers.core import Activation, Dense

training_data = np.array([[0,0],[0,1],[1,0],[1,1]], "float32")
target_data = np.array([[0],[1],[1],[0]], "float32")

class Network:

    def __init__(self):
        self.model = Sequential()

    def create_model(self):
        self.model.add(Dense(32, input_dim=2, activation='relu'))
        self.model.add(Dense(16, input_dim=32, activation='relu'))
        self.model.add(Dense(1, activation='sigmoid'))

    def compile_model(self):
        self.model.compile(loss='mean_squared_error', optimizer='adam', metrics=['binary_accuracy'])

    def train_model(self):
        self.model.fit(training_data, target_data, epochs=1000, verbose=1)

    def predict(self):
        self.prediction = self.model.predict(training_data)
        return self.prediction

if __name__ == "__main__":
    network = Network()
    network.create_model()
    network.compile_model()
    network.train_model()
    print(network.predict())