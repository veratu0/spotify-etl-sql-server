import requests
import time
import pandas as pd
import json
from .auth_code_flow import get_user_token as get_spotify_token


def get_playlist_tracks(playlist_id, token):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/items"
    headers = {"Authorization": f"Bearer {token}"}
    tracks = []
    limit = 100
    offset = 0

    while True:
        params = {"limit": limit, "offset": offset}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        tracks.extend(data.get("items", []))

        next_url = data.get("next")
        if not next_url:
            break
        offset += limit
        time.sleep(0.1)
    return tracks


def extract_playlist_data(playlist_id, token=None, save_raw=True):
    # if token is None, obtain a new one
    if token is None:
        token = get_spotify_token()
    raw_tracks = get_playlist_tracks(playlist_id, token)

    if save_raw:
        with open(f"data/raw/playlist_{playlist_id}.json", "w") as f:
            json.dump(raw_tracks, f, indent=2)

    records = []
    for item in raw_tracks:
        track = item.get("item")  
        if not track or track.get("id") is None:
            continue
        artist = track["artists"][0] if track["artists"] else {"id": None, "name": None}
        record = {
            "track_id": track["id"],
            "track_name": track["name"],
            "duration_ms": track.get("duration_ms"),
            "explicit": track.get("explicit"),
            "album_id": track["album"]["id"],
            "album_name": track["album"]["name"],
            "release_date": track["album"]["release_date"],
            "artist_id": artist["id"],
            "artist_name": artist["name"],
            "added_at": item.get("added_at")
        }
        records.append(record)

    df = pd.DataFrame(records)
    df.to_csv("data/raw/tracks_raw.csv", index=False)
    return df
