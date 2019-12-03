import time
import sys
import spotipy
import spotipy.util as util

from objects.song_audio_features import *
from objects.song import *

AUDIO_FEATURES_BATCH_SIZE = 100
OFFSET_SIZE = 50
SCOPE = 'user-library-read'
GENRE_PRECEDNECES = ["country", "metal", "alternative", "rap", "edm", "indie",
                     "jazz", "pop", "lo-fi", "rock", "classical"]


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

def parse_into_songs(raw_features, tracks, sp):
    print("Parsing into song objects and grabbing genres")
    songs = []
    for i, f in enumerate(raw_features):
        if i % 100 == 0:
            print(i, "/", len(raw_features))
        song_features = SongAudioFeatures(f)
        song = Song(song_features)
        song.name = tracks[i]["name"]
        songs.append(song)
        song.genre = sp.artist(tracks[i]["artists"][0]["uri"])["genres"]
    
    return songs

def scrub_genres(songs):
    found = False
    for song in songs:
        song_genres = song.genre
        for prec in GENRE_PRECEDNECES:
            for genre in song_genres:
                if prec in genre:
                    print(song.name, song.genre, "->", prec)
                    song.genre = prec
                    found = True
                    break
            if found:
                found = False
                break
    
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

    songs = parse_into_songs(raw_features, tracks, sp)
    scrub_genres(songs)
    print("\nSuccessfully scrubbed all the songs.")
    print("Converting to dataframes and writing to CSV...")

    songs = [s for s in songs if not isinstance(s.genre, list)]
    big_dict = {
        "name" : songs[0].name,
        "genre" : songs[0].genre
    }
    big_dict.update(songs[0].features.raw_data)
    for (k, v) in big_dict.items():
        big_dict[k] = [v]

    for song in songs[1:]:
        for (k, v) in song.get_dict().items():
            big_dict[k].append(v)

    df = pd.DataFrame.from_dict(big_dict, orient='index').T
    export_csv = df.to_csv('features.csv', header=True)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: python3 pull_library.py username ...")
        sys.exit(0)
    main()
