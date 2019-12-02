import spotipy
import sys
from utils import get_spotify_credentials
from spotipy.oauth2 import SpotifyClientCredentials


credentials = get_spotify_credentials()

client_credentials_manager = SpotifyClientCredentials(client_id=credentials[0],
                                                      client_secret=credentials[1])
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


if len(sys.argv) > 1:
    name = ' '.join(sys.argv[1:])
else:
    name = 'Radiohead'

#results = spotify.search(q='artist:' + name, type='artist')
results = spotify.search(q='')
items = results['artists']['items']
if len(items) > 0:
    artist = items[0]
    print(artist['name'], artist['images'][0]['url'])
