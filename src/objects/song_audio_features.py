class SongAudioFeatures:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.danceability = raw_data["danceability"]
        self.energy = raw_data["energy"]
        self.key = raw_data["key"]
        self.loudness = raw_data["loudness"]
        self.mode = raw_data["mode"]
        self.speechiness = raw_data["speechiness"]
        self.acousticness = raw_data["acousticness"]
        self.instrumentalness = raw_data["instrumentalness"]
        self.liveness = raw_data["liveness"]
        self.valence = raw_data["valence"]
        self.tempo = raw_data["tempo"]
        self.type = raw_data["type"]
        self.id = raw_data["id"]
        self.uri = raw_data["uri"]
        self.track_href = raw_data["track_href"]
        self.analysis_url = raw_data["analysis_url"]
        self.duration_ms = raw_data["duration_ms"]
        self.time_signature = raw_data["time_signature"]

    def get_duration_seconds(self):
        return self.duration_ms / 1000
