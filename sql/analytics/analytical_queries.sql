/*
====================================================================
Analytical Queries for Spotify Analytics
====================================================================
Script Purpose:
    These queries answer business questions about playlist tracks,
    artists, albums, and listening trends.
====================================================================
*/

USE SpotifyAnalytics;
GO

-- 1. Top 10 artists by number of tracks in the playlist
SELECT TOP 10
    a.artist_name,
    COUNT(f.track_id) AS track_count
FROM fact_track_metrics f
INNER JOIN dim_artist a ON f.artist_id = a.artist_id
GROUP BY a.artist_name
ORDER BY track_count DESC;
GO

-- 2. Track distribution by release year (last 10 years)
SELECT
    f.release_year,
    COUNT(f.track_id) AS number_of_tracks
FROM fact_track_metrics f
WHERE f.release_year >= YEAR(GETDATE()) - 10
GROUP BY f.release_year
ORDER BY f.release_year DESC;
GO

-- 3. Proportion of explicit vs. non-explicit tracks
SELECT
    CASE WHEN f.explicit = 1 THEN 'Explicit' ELSE 'Clean' END AS content_type,
    COUNT(*) AS track_count,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS DECIMAL(5,2)) AS percentage
FROM fact_track_metrics f
GROUP BY f.explicit;
GO

-- 4. Average track duration (minutes) per artist (top 10 by duration)
SELECT TOP 10
    a.artist_name,
    AVG(f.duration_ms) / 60000.0 AS avg_duration_min
FROM fact_track_metrics f
INNER JOIN dim_artist a ON f.artist_id = a.artist_id
GROUP BY a.artist_name
ORDER BY avg_duration_min DESC;
GO

-- 5. Most recent tracks added to the playlist
SELECT TOP 20
    f.track_name,
    a.artist_name,
    f.added_at,
    f.release_year
FROM fact_track_metrics f
INNER JOIN dim_artist a ON f.artist_id = a.artist_id
ORDER BY f.added_at DESC;
GO

-- 6. Album with the most tracks in the playlist
SELECT TOP 1
    al.album_name,
    COUNT(f.track_id) AS track_count
FROM fact_track_metrics f
INNER JOIN dim_album al ON f.album_id = al.album_id
GROUP BY al.album_name
ORDER BY track_count DESC;
GO
