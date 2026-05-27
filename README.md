# Spotify ETL Pipeline & Analytics Dashboard

## Overview
End‑to‑end data pipeline that extracts playlist data from Spotify API, transforms it using Python/Pandas, loads into SQL Server, and visualises insights in Power BI.

**Technology Stack**
- Python (Requests, Pandas, pyodbc)
- SQL Server
- Power BI
- Git & GitHub

## How It Works
1. **Extract** – Authenticate via OAuth 2.0 (Authorization Code Flow), fetch playlist tracks using Spotify Web API.
2. **Transform** – Clean data, handle nulls, convert data types, engineer features (release year, duration minutes).
3. **Load** – Load into SQL Server star schema (dim_artist, dim_album, fact_track_metrics).
4. **Analyse** – Answer business questions using SQL and DAX.
5. **Visualise** – Interactive Power BI dashboard.

## Setup Instructions

### Prerequisites
- Python 3.9+
- SQL Server (Express or Developer)
- Power BI Desktop
- Spotify Developer account

### Clone the repository
```bash
git clone https://github.com/veratu0/spotify-etl-sql-server.git
cd spotify-etl-sql-server
