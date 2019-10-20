import json

def get_spotify_credentials():
    with open (".env") as json_file:
        data = json.load(json_file)
        return (data["CLIENT_ID"], data["CLIENT_SECRET"])
