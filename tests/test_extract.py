from scripts.extract.extract_playlist import extract_playlist_data

playlist_id = "3jUrtBMNbXCFeHGBnVPND5"
df = extract_playlist_data(playlist_id, save_raw=True)
print(df.head())
