import sys
import spotipy
import spotipy.util as util

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
    token = util.prompt_for_user_token(username, scope)# client_id='http://localhost/', client_secret='http://localhost/', redirect_uri='http://localhost/')


    if token is None:
        print("Bad token")
        sys.exit(1)

    ## I have 141 songs in my lib

    tracks = []

    sp = spotipy.Spotify(auth=token)

    i = 0;
    while(1):
        results = sp.current_user_saved_tracks(limit=50, offset=i)
        for item in results['items']:
            tracks.append(item['track'])
        if len(results['items']) < 50:
            break
        i+=50

    #for track in tracks:
    #    print(track['name'])

    print(tracks[0]['name'])
    id = tracks[0]['id']
    analysis = sp.audio_analysis(id)
    print(analysis['sections'][0]['key'])