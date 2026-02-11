# Day 46 – Spotify Playlist Automation

## What I Learned
- OAuth authentication with Spotify
- Using Spotipy to interact with the Spotify API
- Web scraping with BeautifulSoup
- Combining scraped data with external APIs
- Automating playlist creation

## Project Overview
This project:
- Scrapes Billboard Hot 100 songs for a given date
- Searches each song on Spotify
- Creates a private Spotify playlist
- Adds all found songs automatically

## Tech Stack
- Python
- BeautifulSoup
- requests
- Spotipy (Spotify Web API)
- dotenv for environment variables

## How It Works
1. User enters a date (YYYY-MM-DD)
2. Songs are scraped from Billboard Hot 100
3. Spotify OAuth authenticates the user
4. A private playlist is created
5. Songs are added to the playlist

## Result
A fully automated Spotify playlist generator based on historical music charts.
