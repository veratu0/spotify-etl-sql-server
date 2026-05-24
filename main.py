# main.py
import pandas as pd
from scripts.extract.extract_playlist import extract_playlist_data
from scripts.extract.auth_code_flow import get_user_token


def run_etl_pipeline(playlist_id: str):
    print("--- Starting Spotify ETL Pipeline ---")

    # Obtain token (once, though extract_playlist_data can also get it)
    print("Authenticating with Spotify...")
    token = get_user_token()
    print("Authentication successful.")

    # Extraction
    print(f"Extracting data for playlist: {playlist_id}")
    tracks_df = extract_playlist_data(playlist_id, token=token, save_raw=True)

    if tracks_df.empty:
        print("No tracks found. Exiting.")
        return

    print(f"Extraction complete. {len(tracks_df)} tracks found.")

    # Transformation (without popularity)
    print("Transforming data...")

    # Convert added_at to datetime
    if 'added_at' in tracks_df.columns:
        tracks_df['added_at'] = pd.to_datetime(tracks_df['added_at'])

    # Remove duplicates
    tracks_df_clean = tracks_df.drop_duplicates(subset=['track_id'])

    # Add release_year from release_date
    tracks_df_clean['release_year'] = pd.to_datetime(tracks_df_clean['release_date'], errors='coerce').dt.year

    # Fill missing release_year with 0 (or drop)
    tracks_df_clean['release_year'] = tracks_df_clean['release_year'].fillna(0).astype(int)

    # Save cleaned data
    tracks_df_clean.to_csv("data/processed/spotify_cleaned.csv", index=False)
    print(f"Transformation complete. Cleaned data saved to data/processed/spotify_cleaned.csv")
    print("--- ETL Pipeline Finished Successfully ---")


if __name__ == "__main__":
    YOUR_PLAYLIST_ID = "3jUrtBMNbXCFeHGBnVPND5"
    run_etl_pipeline(YOUR_PLAYLIST_ID)