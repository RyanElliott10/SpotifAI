import sys
import spotipy
import spotipy.util as util

from objects.song_audio_features import *
from objects.song import *

AUDIO_FEATURES_BATCH_SIZE = 100
OFFSET_SIZE = 50
SCOPE = 'user-library-read'


def get_raw_features(song_ids, sp):
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

def get_tracks(token, sp):
    tracks = []
    i = 0
    print("Fetching data from Spotify")
    results = {'items' : []}
    while len(results['items']) >= OFFSET_SIZE or i == 0:
        results = sp.current_user_saved_tracks(limit=OFFSET_SIZE, offset=i)
        for item in results['items']:
            tracks.append(item['track'])
        i += OFFSET_SIZE
    
    return tracks

def get_song_ids(tracks):
    song_ids = []
    for track in tracks:
        song_id = track["id"]
        song_ids.append(song_id)

    return song_ids

def parse_into_songs(raw_features, tracks):
    songs = []
    for i, f in enumerate(raw_features):
        song_features = SongAudioFeatures(f)
        song = Song(song_features)
        song.name = tracks[i]["name"]
        songs.append(song)
    
    return songs

def main():
    user_count = len(sys.argv) - 1
    user_list = []
    for i in range(0, user_count):
        user_list.append(sys.argv[i+1])

    for username in user_list:
        token = util.prompt_for_user_token(username, SCOPE, redirect_uri='http://localhost/')
        if token is None:
            print("Bad token")
            sys.exit(1)

        sp = spotipy.Spotify(auth=token)
        
        tracks = get_tracks(token, sp)
        song_ids = get_song_ids(tracks)
        raw_features = get_raw_features(song_ids, sp)
        
        assert len(raw_features) == len(tracks)

        songs = parse_into_songs(raw_features, tracks)

        for song in songs:
            print(song.features.acousticness, song.name, song.features.uri)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: python3 pull_library.py username ...")
        sys.exit(0)
    main()
