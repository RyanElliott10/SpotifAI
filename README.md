# SpotifAI
Handy dandy neural network that generates playlists from a given input library.

# Requirements
```
Keras==2.3.1
Keras-Applications==1.0.8
Keras-Preprocessing==1.1.0
numpy==1.17.0
spotipy==2.4.4
h5py==2.10.0
```

Run `pip3 install -r requirements.txt` to install all used libraries.

# Instructions
Create a new file, `src/.env`, that will contain two keys (in JSON format):
```
{
  "CLIENT_ID": "<your_spotify_api_id_here>",
  "CLIENT_SECRET": "<your_spotify_api_secret_here>"
}
```

# Usage
There are two modes you can run `neural_network.py` in:
* Using a pre-trained model
* Training a new model

To use a pre-trained model, run `python3 neural_network.py -p`. This option requires the existence of two files: `model.json` and `model.h5`.

To train a new model (and generate the above required files), run `python3 neural_network -n`. This will train the model and create `model.json` and `model.h5` which can later be used as pre-trained models.

# add me on linkedIn @Sean-Nesbit
