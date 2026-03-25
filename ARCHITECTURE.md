# Architecture — LILA BLACK Player Journey Visualization Tool

## Tech Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Data pipeline | Python + PyArrow + Pandas | Fast parquet parsing, minimal setup |
| Frontend | Vanilla HTML/CSS/JavaScript | No framework overhead, single file, instant deploy |
| Rendering | HTML5 Canvas | Handles 60k+ events efficiently, full control over drawing |
| Hosting | Netlify Drop | Zero-config deploy, free, instant shareable URL |

## Data Flow
```
Raw parquet files (1,250 files, ~89k events)
        ↓
convert_data.py (Python)
  - Reads each .nakama-0 file with PyArrow
  - Decodes event bytes to UTF-8 strings
  - Detects bots (numeric user_id) vs humans (UUID)
  - Adds date field from folder name
  - Outputs two files:
        ↓
public/data.json     — all 89,104 events (25MB)
public/matches.json  — 796 match summaries
        ↓
Browser loads both JSON files on page start
        ↓
JavaScript filters events by map/date/match selection
        ↓
Canvas renders dots, markers, heatmap overlays
```

## Coordinate Mapping

The trickiest part. Game world uses 3D coordinates (x, y, z) but minimaps
are 2D 1024x1024 images. The y axis is elevation — ignored for 2D plotting.
Only x and z are used.

Each map has a scale and origin defined in the README:

| Map | Scale | Origin X | Origin Z |
|-----|-------|----------|----------|
| AmbroseValley | 900 | -370 | -473 |
| GrandRift | 581 | -290 | -290 |
| Lockdown | 1000 | -500 | -500 |

Conversion formula:
```
u = (x - originX) / scale
v = (z - originZ) / scale
pixelX = u * 1024
pixelY = (1 - v) * 1024   ← Y is flipped (image origin is top-left)
```

The Y flip was the key gotcha — without it all points appear mirrored vertically.

## Assumptions

- Timestamps represent match-relative time, not wall-clock time. Playback
  uses relative ordering within a match_id.
- February 14 is a partial day per the README — treated as valid data,
  just smaller sample size.
- Bot detection is purely filename/user_id based (numeric = bot, UUID = human)
  as documented in the README. No heuristic needed.
- All position events outside the 0-1 UV range are rendered but may appear
  outside the minimap bounds — treated as valid edge data.

## Tradeoffs

| Decision | What I chose | What I gave up |
|----------|-------------|----------------|
| No backend | Pure frontend JSON | Can't handle datasets >100MB |
| Single HTML file | Simple deploy, easy review | Harder to maintain long-term |
| Canvas over WebGL | Simpler code | Performance ceiling ~100k points |
| Pre-process to JSON | Fast browser load | Extra build step needed |
| Load all data upfront | Instant filter response | ~3s initial load time |

## With More Time

- Stream data progressively instead of loading all 25MB upfront
- Add player path trails — connect position dots into movement lines per player
- Add zoom and pan on the canvas
- Add a match comparison view — two matches side by side
- Move to WebGL (deck.gl) for handling larger datasets
- Build a proper backend with DuckDB for live querying
```

---

4. Press `Ctrl+S` to save

Then in PowerShell:
```
git add ARCHITECTURE.md
git commit -m "Fix architecture doc content"
git push