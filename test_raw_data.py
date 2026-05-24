import pandas as pd
df = pd.read_csv("data/raw/tracks_raw.csv")
print(df.shape)
print(df[["track_name", "artist_name"]].head())