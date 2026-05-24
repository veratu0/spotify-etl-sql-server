import pyodbc
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


def get_sql_connection():
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_NAME')};"
        f"Trusted_Connection={os.getenv('DB_TRUSTED_CONNECTION')};"
    )
    return pyodbc.connect(conn_str)


def load_data(cleaned_csv="data/processed/spotify_cleaned.csv"):
    df = pd.read_csv(cleaned_csv)

    # Convert 'added_at' to SQL Server compatible datetime string
    # The CSV contains ISO format like "2026-05-23T09:15:26Z"
    df['added_at'] = pd.to_datetime(df['added_at']).dt.strftime('%Y-%m-%d %H:%M:%S')

    # Convert 'explicit' boolean to bit (0/1)
    df['explicit'] = df['explicit'].astype(int)

    # Convert 'release_date' for dim_album to date string (YYYY-MM-DD)
    # Handle possible NaT or empty values
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce').dt.strftime('%Y-%m-%d')

    conn = get_sql_connection()
    cursor = conn.cursor()

    # Clear tables
    cursor.execute("DELETE FROM fact_track_metrics")
    cursor.execute("DELETE FROM dim_artist")
    cursor.execute("DELETE FROM dim_album")
    conn.commit()

    # Load dim_artist (unique)
    artists = df[['artist_id', 'artist_name']].drop_duplicates()
    for _, row in artists.iterrows():
        cursor.execute("INSERT INTO dim_artist (artist_id, artist_name) VALUES (?, ?)",
                       (row['artist_id'], row['artist_name']))

    # Load dim_album (unique)
    albums = df[['album_id', 'album_name', 'release_date']].drop_duplicates()
    for _, row in albums.iterrows():
        # Skip if release_date is NaT (converted to None)
        release_date_val = row['release_date'] if pd.notna(row['release_date']) else None
        cursor.execute("INSERT INTO dim_album (album_id, album_name, release_date) VALUES (?, ?, ?)",
                       (row['album_id'], row['album_name'], release_date_val))

    # Load fact table
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO fact_track_metrics 
            (track_id, track_name, duration_ms, explicit, release_year, added_at, artist_id, album_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row['track_id'], row['track_name'], row['duration_ms'],
            row['explicit'], row['release_year'], row['added_at'],
            row['artist_id'], row['album_id']
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print("Data loaded successfully into SQL Server.")


if __name__ == "__main__":
    load_data()