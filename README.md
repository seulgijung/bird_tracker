# NY Rare Bird Tracker

Auto-updating dashboard for New York rare bird sightings from eBird.

## Features

- Scrapes eBird rare bird alerts every 4 hours
- Interactive map showing sighting locations
- Filter by species or search
- Auto-deployed to GitHub Pages

## Live Dashboard

Visit: `https://YOUR_USERNAME.github.io/bird_tracker/`

## Data Source

[eBird - New York Rare Bird Alert](https://ebird.org/alert/summary?sid=SN35466)

## How It Works

1. GitHub Actions runs `scraper.py` every 4 hours
2. Scraper fetches latest sightings from eBird
3. Data saved to `data.json`
4. GitHub Pages serves `index.html` which displays the data
