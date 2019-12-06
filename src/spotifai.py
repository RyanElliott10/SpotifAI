import sys
import json

import neural_network

prefs = {
    "model_name" : "",
    "confidence_threshold" : 0.0,
    "data_csv" : "",
    "username" : "",
    "playlist_uris" : [],
    "genres" : []
}

def main(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        for d in data:
            prefs[d] = data[d]

    neural_network.CONFIDENCE_THRESHOLD = prefs["confidence_threshold"]
    neural_network.CULMINATE_GENRES = prefs["genres"]
    neural_network.USE_MODEL = prefs["model_name"]
    neural_network.USE_CSV = prefs["data_csv"]
    neural_network.SPOTIFY_USERNAME = prefs["username"]
    neural_network.PLAYLIST_URIS = prefs["playlist_uris"]
    neural_network.in_depth_validate_predictions(neural_network.Network())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\033[91mUsage:\033[0m python3 spotifai.py < preferences_filename >")
        exit()
    main(sys.argv[1])