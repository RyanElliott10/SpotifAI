import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

CSV_FILENAME = ""
INDICES = {
    "genre" : 2,
    "danceability" : 3,
    "energy" : 4,
    "acousticness" : 9,
    "duration_ms" : 19
}

def chart(data):
    genre_counts = {
        "country" : [0, 0],
        "metal" : [0, 0],
        "alternative" : [0, 0],
        "rap" : [0, 0],
        "edm" : [0, 0],
        "jazz" : [0, 0],
        "pop" : [0, 0],
        "rock" : [0, 0],
        "classical" : [0, 0]
    }

    genres = []
    scores = []
    for (i, el) in enumerate(data):
        genre_counts[el[INDICES["genre"]]][0] += el[INDICES["duration_ms"]]
        genre_counts[el[INDICES["genre"]]][1] += 1
    for (k, v) in genre_counts.items():
        genres.append(k)
        scores.append(v[0] / v[1])

    y_pos = np.arange(len(genres))
    plt.bar(y_pos, scores, align="center")
    plt.xticks(y_pos, genres)
    plt.ylabel("duration_ms")
    plt.title("Average Duration for Each Genre")
    plt.show()

def main():
    csv_data = pd.read_csv(CSV_FILENAME).to_numpy()
    chart(csv_data)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\033[91mUsage:\033[0m python3 data_visualization.py < csv_filename >")
        exit()
    CSV_FILENAME = sys.argv[1]
    main()