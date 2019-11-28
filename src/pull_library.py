import sys
import spotipy
import spotipy.util as util

scope = 'user-library-read'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    username = "cschnelz"

token = util.prompt_for_user_token(username, scope, 
    client_id='e9f25d79743c49f584b852ae182e2b80', client_secret='54b53145a5d24c48a8b20d56f367b605', redirect_uri='http://localhost/')


if token is None:
    print("Bad token")
    sys.exit(0)

## I have 141 songs in my lib

tracks = []

sp = spotipy.Spotify(auth=token)

i = 0;
while(1):
    results = sp.current_user_saved_tracks(limit=50, offset=i)
    for item in results['items']:
        tracks.append(item['track'])
    #if len(results['items']) > 0:
    #    item = results['items'][0]
    #    tracks.append(item['track'])
    if len(results['items']) < 50:
        break
    i+=50

#for track in tracks:
#    print(track['name'])

print(tracks[0])
id = tracks[0]['id']
analysis = sp.audio_analysis(id)
print(analysis['sections'][0]['key'])