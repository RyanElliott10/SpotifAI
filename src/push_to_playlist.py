import pprint
import sys

import spotipy
import spotipy.util as util

def add_to_playlist(username, playlist_id, track_ids):
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username, scope, redirect_uri='http://localhost/')

    if not token:
        print("Can't get token for", username)
        exit()
    
    sp = spotipy.Spotify(auth=token)
    sp.trace = False

    n = 100
    chunks = [track_ids[i * n:(i + 1) * n] for i in range((len(track_ids) + n - 1) // n )]
    for chunk in chunks:
        results = sp.user_playlist_add_tracks(username, playlist_id, chunk)
