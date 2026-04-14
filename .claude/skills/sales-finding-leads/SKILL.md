---
name: sales-finding-leads
description: Finds business leads using Google Places API with deep grid-based search. Use when the user wants to find potential clients, leads, prospects, or businesses in a geographic area.
allowed-tools: Bash(python *) Bash(pip *) Bash(source *) Bash(bash *) Read Write Edit
---

# Finding Leads via Google Places API

Searches for businesses using Google Places API (New) with grid-based area subdivision to maximize results beyond the 60-result API limit.

## Prerequisites

Before first use, run the project setup script:

```bash
bash setup.sh
```

This checks for Python 3, creates a virtual environment, installs dependencies, and sets up `.env` from `.env.example`. The user must then add their `GOOGLE_PLACES_API_KEY` to `.env`.

If setup was already run, just activate the venv:

```bash
source venv/bin/activate
```

The script loads `.env` automatically via `python-dotenv`.

## Workflow

```
Lead Search Progress:
- [ ] Step 0: Verify setup (venv active, .env has API key)
- [ ] Step 1: Confirm search parameters with user
- [ ] Step 2: Run the search script
- [ ] Step 3: Present results and open report
```

### Step 0: Verify setup

1. Check if `venv/` exists. If not, run `bash setup.sh`.
2. Activate: `source venv/bin/activate`
3. Check `.env` exists and has a real key (not the placeholder).

### Step 1: Confirm search parameters

Ask the user:

1. **What to search**: business type and city (e.g., "Abogados en Buenos Aires")
2. **Filter mode**: Ask explicitly:
   - `all` -- return every result
   - `no-website` -- return ONLY businesses without a website (high-value leads for web design/marketing agencies)
3. **Search depth**: Default grid is 5x5 (25 cells, up to ~1500 unique results). Offer:
   - `3` (3x3=9 cells) -- quick scan
   - `5` (5x5=25 cells) -- standard depth (default)
   - `7` (7x7=49 cells) -- deep scan, slower but more thorough

If the city is NOT Buenos Aires, ask for approximate geographic bounds (SW and NE coordinates) or look them up.

### Step 2: Run the search script

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/find_leads.py "QUERY" \
  --filter FILTER_MODE \
  --grid-size GRID_SIZE
```

Default bounds are Buenos Aires. For other cities, add:
```
--sw-lat LAT --sw-lng LNG --ne-lat LAT --ne-lng LNG
```

The script automatically creates the output directory:
```
./leads/YYYY-MM-DD/query-slug/
├── leads_report.html
└── leads_data.json
```

Multiple searches on the same day go under the same date folder. The query is normalized to a slug (lowercase, no accents, hyphens).

The script:
1. Divides the search area into a grid of rectangles
2. Runs a Places API text search in each cell
3. Paginates through all pages per cell (up to 60 results each)
4. Deduplicates results by place ID
5. Optionally filters to only businesses without a website
6. Saves raw data to JSON and generates an HTML report

### Step 3: Present results

After the script finishes:
1. Report the total leads found, how many have/don't have a website, how many have reviews and photos
2. Tell the user where the output folder is (e.g., `./leads/2026-04-14/abogados-en-caballito/`)
3. Open the HTML report from that folder

The HTML report shows a compact table (name, address, phone, web, rating). Clicking any row opens a full detail view with contact info, photos, opening hours, and reviews. The JSON contains the full API response including location coordinates, address components, payment options, and all atmosphere data.

## City bounds reference

| City | SW Lat | SW Lng | NE Lat | NE Lng |
|---|---|---|---|---|
| Buenos Aires | -34.71 | -58.53 | -34.52 | -58.33 |
| CABA only | -34.69 | -58.53 | -34.54 | -58.34 |
| Montevideo | -34.93 | -56.27 | -34.82 | -56.07 |
| Santiago | -33.52 | -70.75 | -33.35 | -70.55 |
