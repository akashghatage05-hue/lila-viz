# LILA BLACK — Player Journey Visualization Tool

A browser-based tool for LILA Games' Level Design team to explore player behavior across maps.

## Live Tool
👉 https://gleeful-banoffee-64d886.netlify.app/

## What it does
- Visualizes 89,000+ player events across 3 maps (AmbroseValley, GrandRift, Lockdown)
- Distinguishes human players (blue) from bots (grey)
- Shows kills, deaths, storm deaths, and loot events as distinct markers
- Heatmap overlays for kill zones, death zones, and high-traffic areas
- Filter by map, date, and specific match
- Timeline playback to watch a match unfold over time

## Setup

### Requirements
- Python 3.x
- Node.js (optional, for local serving)

### Install dependencies
```
pip install pyarrow pandas
```

### Run data pipeline
Place the `player_data/` folder in the root directory, then:
```
python convert_data.py
```
This generates `public/data.json` and `public/matches.json`

### Serve locally
```
python -m http.server 3000 --directory public
```
Then open http://localhost:3000

## Tech Stack
- Python + PyArrow for data pipeline
- Vanilla HTML/CSS/JavaScript + Canvas API for frontend
- Netlify for hosting

## Deliverables
- `convert_data.py` — data pipeline script
- `public/index.html` — visualization tool
- `ARCHITECTURE.md` — technical decisions and tradeoffs
- `INSIGHTS.md` — three data insights from the tool
```

Save it, then push everything:
```
git add README.md ARCHITECTURE.md
git commit -m "Add README and architecture doc"
git push
