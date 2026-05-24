/*
====================================================================
View: vw_track_analytics
====================================================================
Purpose:
    A denormalized view that combines fact and dimension tables
    for easy querying and Power BI reporting.
    Avoids repeated JOINs in analytical queries.
====================================================================
*/

USE SpotifyAnalytics;
GO

IF OBJECT_ID ('vw_track_analytics', 'V') IS NOT NULL
    DROP VIEW vw_track_analytics;
GO

CREATE VIEW vw_track_analytics AS
SELECT
    f.track_id,
    f.track_name,
    f.duration_ms,
    f.duration_ms / 60000.0 AS duration_minutes,
    f.explicit,
    f.release_year,
    f.added_at,
    a.artist_id,
    a.artist_name,
    al.album_id,
    al.album_name,
    al.release_date
FROM fact_track_metrics f
INNER JOIN dim_artist a ON f.artist_id = a.artist_id
INNER JOIN dim_album al ON f.album_id = al.album_id;
GO

-- Quick test
SELECT TOP 10 * FROM vw_track_analytics;
GO