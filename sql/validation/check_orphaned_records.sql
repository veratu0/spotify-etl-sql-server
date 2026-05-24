/*
====================================================================
Data Integrity: Orphaned Records Check
====================================================================
Purpose:
    Ensure that every fact row has valid artist and album references.
    Run after every data load.
====================================================================
*/

USE SpotifyAnalytics;
GO

-- Check for fact rows missing an artist
SELECT COUNT(*) AS orphaned_tracks_missing_artist
FROM fact_track_metrics f
LEFT JOIN dim_artist a ON f.artist_id = a.artist_id
WHERE a.artist_id IS NULL;
GO

-- Check for fact rows missing an album
SELECT COUNT(*) AS orphaned_tracks_missing_album
FROM fact_track_metrics f
LEFT JOIN dim_album al ON f.album_id = al.album_id
WHERE al.album_id IS NULL;
GO

-- Check for duplicate artist names (potential data issue)
SELECT artist_name, COUNT(*) AS dup_count
FROM dim_artist
GROUP BY artist_name
HAVING COUNT(*) > 1;
GO