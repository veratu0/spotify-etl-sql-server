import requests
import time
import pandas as pd
from .auth_code_flow import get_user_token as get_spotify_token


def get_tracks_details(track_ids, token):
    url = "https://api.spotify.com/v1/tracks"
    headers = {"Authorization": f"Bearer {token}"}
    all_tracks = []
    for i in range(0, len(track_ids), 50):
        batch = track_ids[i:i + 50]
        params = {"ids": ",".join(batch)}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        all_tracks.extend(data["tracks"])
        time.sleep(0.1)
    return all_tracks


def enrich_with_popularity(tracks_df, token=None, save_processed=True):
    if token is None:
        token = get_spotify_token()
    track_ids = tracks_df["track_id"].tolist()
    tracks_details = get_tracks_details(track_ids, token)

    popularity_dict = {}
    for track in tracks_details:
        if track and track.get("id"):
            popularity_dict[track["id"]] = track.get("popularity")

    tracks_df["track_popularity"] = tracks_df["track_id"].map(popularity_dict)

    if save_processed:
        tracks_df.to_csv("data/processed/tracks_enriched.csv", index=False)
    return tracks_df