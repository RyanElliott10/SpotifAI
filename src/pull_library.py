import sys
import spotipy
import spotipy.util as util

from objects.song_audio_features import *
from objects.song import *

AUDIO_FEATURES_BATCH_SIZE = 100
OFFSET_SIZE = 50

def get_raw_features(song_ids):
    raw_features = []
    prev_index = 0
    next_index = AUDIO_FEATURES_BATCH_SIZE

    while next_index <= len(song_ids):
        raw_features.extend(sp.audio_features(song_ids[prev_index:next_index]))
        if next_index >= len(song_ids):
            break
            
        prev_index = next_index
        next_index += AUDIO_FEATURES_BATCH_SIZE
        if next_index > len(song_ids):
            next_index = len(song_ids)

    return raw_features

scope = 'user-library-read'

if len(sys.argv) > 1:
    user_count = len(sys.argv) - 1
    user_list = []
    for i in range(0, user_count):
        user_list.append(sys.argv[i+1])
else:
    print("Usage: python3 pull_library.py username ...")
    sys.exit(0)

for username in user_list:
    token = util.prompt_for_user_token(username, scope, redirect_uri='http://localhost/')
    if token is None:
        print("Bad token")
        sys.exit(1)

    tracks = []
    sp = spotipy.Spotify(auth=token)
    i = 0
    print("Fetching data from Spotify")
    results = {'items' : []}
    while len(results['items']) >= OFFSET_SIZE or i == 0:
        results = sp.current_user_saved_tracks(limit=OFFSET_SIZE, offset=i)
        for item in results['items']:
            tracks.append(item['track'])
        i += OFFSET_SIZE

    song_ids = []
    songs = []
    for track in tracks:
        song_id = track["id"]
        song_ids.append(song_id)

    raw_features = get_raw_features(song_ids)
    print(len(tracks))
    assert len(raw_features) == len(tracks)
    features = []

    for i, f in enumerate(raw_features):
        song_features = SongAudioFeatures(f)
        features.append(song_features)
        song = Song(song_features)
        song.name = tracks[i]["name"]
        songs.append(song)

    # YEET I got all the songs and features
    for song in songs:
        print(song.features.acousticness, song.name, song.features.uri)
