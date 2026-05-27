/*
====================================================================
DDL Scripts: Create Star Schema Tables for Spotify Analytics
====================================================================
Script Purpose:
    This script creates dimension and fact tables for the Spotify
    analytics pipeline, dropping existing tables if they already exist.
    Tables:
        - dim_artist
        - dim_album
        - fact_track_metrics
    Run this script after creating the SpotifyAnalytics database.
====================================================================
*/

-- Use the SpotifyAnalytics database (ensure it exists)
USE SpotifyAnalytics;
GO

-- ==========================
-- Drop tables if they exist 
-- ==========================
IF OBJECT_ID ('fact_track_metrics', 'U') IS NOT NULL
    DROP TABLE fact_track_metrics;
GO

IF OBJECT_ID ('dim_album', 'U') IS NOT NULL
    DROP TABLE dim_album;
GO

IF OBJECT_ID ('dim_artist', 'U') IS NOT NULL
    DROP TABLE dim_artist;
GO

-- =================================================================
-- Create dimension tables
-- =================================================================

-- dim_artist: stores unique artists
CREATE TABLE dim_artist (
    artist_id   NVARCHAR(50) PRIMARY KEY,
    artist_name NVARCHAR(200) NOT NULL
);
GO

-- dim_album: stores unique albums
CREATE TABLE dim_album (
    album_id     NVARCHAR(50) PRIMARY KEY,
    album_name   NVARCHAR(200),
    release_date DATE          -- can be NULL if not available
);
GO

-- =================================================================
-- Create fact table (references dimensions)
-- =================================================================
CREATE TABLE fact_track_metrics (
    track_id      NVARCHAR(50) PRIMARY KEY,
    track_name    NVARCHAR(200),
    duration_ms   INT,
    explicit      BIT,               
    release_year  INT,                
    added_at      DATETIME,
    artist_id     NVARCHAR(50) FOREIGN KEY REFERENCES dim_artist(artist_id),
    album_id      NVARCHAR(50) FOREIGN KEY REFERENCES dim_album(album_id)
);
GO

-- =================================================================
-- Create indexes for better query performance
-- =================================================================
CREATE INDEX idx_fact_artist ON fact_track_metrics(artist_id);
CREATE INDEX idx_fact_album  ON fact_track_metrics(album_id);
CREATE INDEX idx_fact_year   ON fact_track_metrics(release_year);
GO
