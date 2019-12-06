import time
import sys
import os
import spotipy
import spotipy.util as util
import numpy as np
import pandas as pd

import neural_network
import pull_library
import preprocess_data


def init_data(user):
    path = 'data/' + user + '.csv'
    if os.path.exists(path) == False:
        pull_library.main(mode=1, profile=user)

    processor = preprocess_data.DataPreprocessor(path)
    user_data = processor.get_validation_output_data()

    return np.asarray(user_data)


def init_model(network):    
    network.load_model("models/prod.json", "models/prod.h5")

def main():
    genre_list = []
    for i in range(1, len(sys.argv)):
        genre_list.append(sys.argv[i])

    print(genre_list)

    network = neural_network.Network()
    init_model(network)
    user_library = init_data("cschnelz")
    prediction = network.predict(user_library)
    print(prediction)



if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: python3 application.py genre ...")
        sys.exit(0)
    main()
