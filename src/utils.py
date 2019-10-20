import json

def get_spotify_credentials():
    with open (".env") as json_file:
        data = json.load(json_file)
        return (data["SPOTID"], data["SPOTPASS"])

print(get_spotify_credentials())