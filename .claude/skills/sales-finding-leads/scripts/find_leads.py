#!/usr/bin/env python3
"""
Find business leads using Google Places API (New).
Uses grid-based search to maximize results beyond the 60-result API limit.
Outputs to ./leads/YYYY-MM-DD/normalized-query/
"""

import argparse
import json
import os
import re
import sys
import time
import unicodedata
from datetime import datetime
from pathlib import Path

# Load .env automatically (searches upward from cwd and script location)
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(usecwd=True))

import requests

API_ENDPOINT = "https://places.googleapis.com/v1/places:searchText"

# Buenos Aires default bounds
DEFAULT_BOUNDS = {
    "sw_lat": -34.71,
    "sw_lng": -58.53,
    "ne_lat": -34.52,
    "ne_lng": -58.33,
}

FIELD_MASK = ",".join([
    # Essentials
    "places.id",
    "places.displayName",
    "places.name",
    # Pro
    "places.formattedAddress",
    "places.shortFormattedAddress",
    "places.addressComponents",
    "places.postalAddress",
    "places.location",
    "places.viewport",
    "places.websiteUri",
    "places.googleMapsUri",
    "places.types",
    "places.primaryType",
    "places.primaryTypeDisplayName",
    "places.photos",
    "places.timeZone",
    "places.adrFormatAddress",
    "places.containingPlaces",
    # Enterprise
    "places.internationalPhoneNumber",
    "places.nationalPhoneNumber",
    "places.rating",
    "places.userRatingCount",
    "places.priceLevel",
    "places.priceRange",
    "places.businessStatus",
    "places.currentOpeningHours",
    "places.regularOpeningHours",
    "places.currentSecondaryOpeningHours",
    "places.regularSecondaryOpeningHours",
    # Enterprise + Atmosphere
    "places.reviews",
    "places.editorialSummary",
    "places.generativeSummary",
    "places.allowsDogs",
    "places.goodForChildren",
    "places.goodForGroups",
    "places.goodForWatchingSports",
    "places.liveMusic",
    "places.outdoorSeating",
    "places.restroom",
    "places.delivery",
    "places.dineIn",
    "places.curbsidePickup",
    "places.takeout",
    "places.reservable",
    "places.servesBreakfast",
    "places.servesLunch",
    "places.servesDinner",
    "places.servesBeer",
    "places.servesWine",
    "places.servesBrunch",
    "places.servesVegetarianFood",
    "places.parkingOptions",
    "places.paymentOptions",
    "places.accessibilityOptions",
    # Pagination
    "nextPageToken",
])


def normalize_slug(text):
    """Convert text to a filesystem-safe slug: lowercase, hyphens, no accents."""
    # Remove accents
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    # Lowercase and replace non-alphanumeric with hyphens
    text = re.sub(r"[^a-z0-9]+", "-", text.lower())
    # Strip leading/trailing hyphens
    return text.strip("-")


def build_output_dir(query):
    """Create and return output directory: ./leads/YYYY-MM-DD/query-slug/"""
    today = datetime.now().strftime("%Y-%m-%d")
    slug = normalize_slug(query)
    output_dir = Path("leads") / today / slug
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def search_text(api_key, query, location_restriction=None, page_token=None):
    """Execute a single text search request against the Places API."""
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": FIELD_MASK,
    }

    body = {
        "textQuery": query,
        "pageSize": 20,
        "languageCode": "es",
    }

    # Always include locationRestriction if provided (required for pagination too)
    if location_restriction:
        body["locationRestriction"] = location_restriction

    # Add page token for subsequent pages
    if page_token:
        body["pageToken"] = page_token

    response = requests.post(API_ENDPOINT, json=body, headers=headers)

    if response.status_code == 429:
        print("    Rate limited, waiting 5s...", flush=True)
        time.sleep(5)
        response = requests.post(API_ENDPOINT, json=body, headers=headers)

    if response.status_code != 200:
        print(f"    API error {response.status_code}: {response.text}", file=sys.stderr)
        return {"places": []}

    return response.json()


def create_grid(bounds, grid_size):
    """Divide geographic bounds into a grid of rectangles."""
    lat_step = (bounds["ne_lat"] - bounds["sw_lat"]) / grid_size
    lng_step = (bounds["ne_lng"] - bounds["sw_lng"]) / grid_size

    cells = []
    for i in range(grid_size):
        for j in range(grid_size):
            cells.append({
                "rectangle": {
                    "low": {
                        "latitude": bounds["sw_lat"] + i * lat_step,
                        "longitude": bounds["sw_lng"] + j * lng_step,
                    },
                    "high": {
                        "latitude": bounds["sw_lat"] + (i + 1) * lat_step,
                        "longitude": bounds["sw_lng"] + (j + 1) * lng_step,
                    },
                }
            })
    return cells


def search_all_pages(api_key, query, location_restriction=None):
    """Paginate through all result pages for a single area."""
    all_places = []
    page_token = None

    while True:
        result = search_text(api_key, query, location_restriction, page_token)
        places = result.get("places", [])
        all_places.extend(places)

        page_token = result.get("nextPageToken")
        if not page_token:
            break

        # Pause between pagination requests
        time.sleep(0.4)

    return all_places


def deep_search(api_key, query, bounds, grid_size):
    """Search across a grid of cells to maximize total results."""
    grid = create_grid(bounds, grid_size)
    all_places = {}
    total_cells = len(grid)

    print(f"Starting grid search ({total_cells} cells)...\n", flush=True)

    for i, cell in enumerate(grid, 1):
        sw = cell["rectangle"]["low"]
        ne = cell["rectangle"]["high"]
        print(
            f"  [{i}/{total_cells}] Searching area "
            f"({sw['latitude']:.4f},{sw['longitude']:.4f}) -> "
            f"({ne['latitude']:.4f},{ne['longitude']:.4f})...",
            flush=True,
        )

        places = search_all_pages(api_key, query, cell)
        new_count = 0
        for place in places:
            place_id = place.get("id")
            if place_id and place_id not in all_places:
                all_places[place_id] = place
                new_count += 1

        print(
            f"           Found {len(places)} results, "
            f"{new_count} new (total unique: {len(all_places)})",
            flush=True,
        )
        time.sleep(0.3)

    return list(all_places.values())


def build_photo_url(photo, api_key):
    """Build a photo URL from Places API photo resource name."""
    name = photo.get("name", "")
    if not name:
        return ""
    # Places API (New) photo URL format
    return f"https://places.googleapis.com/v1/{name}/media?maxWidthPx=400&key={api_key}"


def format_hours(hours_obj):
    """Format opening hours into readable HTML."""
    if not hours_obj:
        return ""
    periods = hours_obj.get("weekdayDescriptions", [])
    if not periods:
        return ""
    return "<br>".join(periods)


def format_reviews(reviews):
    """Format reviews into HTML."""
    if not reviews:
        return ""
    html = ""
    for r in reviews[:5]:  # Max 5 reviews
        author = r.get("authorAttribution", {}).get("displayName", "Anonymous")
        text = r.get("text", {}).get("text", "")
        stars = r.get("rating", 0)
        relative_time = r.get("relativePublishTimeDescription", "")
        star_display = "\u2605" * int(stars) + "\u2606" * (5 - int(stars))
        if text:
            text_short = text[:200] + ("..." if len(text) > 200 else "")
            html += (
                f'<div class="review">'
                f'<div class="review-header">'
                f'<span class="review-stars">{star_display}</span>'
                f'<span class="review-author">{author}</span>'
                f'<span class="review-time">{relative_time}</span>'
                f'</div>'
                f'<p>{text_short}</p>'
                f'</div>'
            )
    return html


def prepare_leads_json(places, api_key=""):
    """Prepare a simplified JSON array for embedding in the HTML report."""
    leads = []
    for place in places:
        photos = place.get("photos", [])
        photo_urls = []
        if photos and api_key:
            for p in photos[:5]:
                url = build_photo_url(p, api_key)
                if url:
                    photo_urls.append(url)

        reviews = []
        for r in place.get("reviews", [])[:5]:
            reviews.append({
                "author": r.get("authorAttribution", {}).get("displayName", ""),
                "rating": r.get("rating", 0),
                "time": r.get("relativePublishTimeDescription", ""),
                "text": r.get("text", {}).get("text", ""),
            })

        hours = place.get("regularOpeningHours", {}).get("weekdayDescriptions", [])

        leads.append({
            "name": place.get("displayName", {}).get("text", "N/A"),
            "address": place.get("formattedAddress", "N/A"),
            "shortAddress": place.get("shortFormattedAddress", ""),
            "phone": place.get("internationalPhoneNumber") or place.get("nationalPhoneNumber") or "",
            "website": place.get("websiteUri", ""),
            "rating": place.get("rating", 0),
            "ratingCount": place.get("userRatingCount", 0),
            "mapsUrl": place.get("googleMapsUri", ""),
            "status": place.get("businessStatus", "OPERATIONAL"),
            "type": place.get("primaryTypeDisplayName", {}).get("text", ""),
            "editorial": place.get("editorialSummary", {}).get("text", ""),
            "photos": photo_urls,
            "reviews": reviews,
            "hours": hours,
        })
    return leads


def generate_report(places, query, filter_label, output_path, template_path, api_key=""):
    """Generate an HTML report from the template and lead data."""
    template = Path(template_path).read_text(encoding="utf-8")

    leads = prepare_leads_json(places, api_key)

    # Build simple table rows
    rows = ""
    for i, lead in enumerate(leads):
        web_badge = '<span class="badge badge-success">Si</span>' if lead["website"] else '<span class="badge badge-destructive">No</span>'

        rows += f"""
        <tr data-idx="{i}" onclick="showDetail({i})">
          <td>{i + 1}</td>
          <td class="cell-name">{lead["name"]}</td>
          <td class="cell-truncate">{lead["address"]}</td>
          <td class="cell-phone">{lead["phone"]}</td>
          <td>{web_badge}</td>
          <td class="cell-rating">{lead["rating"] or "\u2014"}</td>
        </tr>"""

    total = len(leads)
    with_website = sum(1 for l in leads if l["website"])
    without_website = total - with_website
    with_reviews = sum(1 for l in leads if l["reviews"])
    with_photos = sum(1 for l in leads if l["photos"])
    rated = [l["rating"] for l in leads if l["rating"]]
    avg_rating = sum(rated) / len(rated) if rated else 0

    # Escape for JS embedding
    leads_json = json.dumps(leads, ensure_ascii=False)

    html = template
    html = html.replace("{{QUERY}}", query)
    html = html.replace("{{DATE}}", datetime.now().strftime("%Y-%m-%d %H:%M"))
    html = html.replace("{{FILTER_MODE}}", filter_label)
    html = html.replace("{{TOTAL}}", str(total))
    html = html.replace("{{WITH_WEBSITE}}", str(with_website))
    html = html.replace("{{WITHOUT_WEBSITE}}", str(without_website))
    html = html.replace("{{WITH_REVIEWS}}", str(with_reviews))
    html = html.replace("{{WITH_PHOTOS}}", str(with_photos))
    html = html.replace("{{AVG_RATING}}", f"{avg_rating:.1f}")
    html = html.replace("{{TABLE_ROWS}}", rows)
    html = html.replace("{{LEADS_JSON}}", leads_json)

    Path(output_path).write_text(html, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Find business leads using Google Places API (New)"
    )
    parser.add_argument("query", help='Search query (e.g., "Abogados en Buenos Aires")')
    parser.add_argument(
        "--filter",
        choices=["all", "no-website"],
        default="all",
        help="Filter: 'all' or 'no-website' only",
    )
    parser.add_argument(
        "--grid-size",
        type=int,
        default=5,
        help="Grid subdivisions per axis (default: 5 -> 5x5=25 cells)",
    )
    parser.add_argument("--sw-lat", type=float, default=DEFAULT_BOUNDS["sw_lat"])
    parser.add_argument("--sw-lng", type=float, default=DEFAULT_BOUNDS["sw_lng"])
    parser.add_argument("--ne-lat", type=float, default=DEFAULT_BOUNDS["ne_lat"])
    parser.add_argument("--ne-lng", type=float, default=DEFAULT_BOUNDS["ne_lng"])

    args = parser.parse_args()

    api_key = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not api_key:
        print("Error: GOOGLE_PLACES_API_KEY environment variable not set.", file=sys.stderr)
        print("See SETUP.md for configuration instructions.", file=sys.stderr)
        sys.exit(1)

    bounds = {
        "sw_lat": args.sw_lat,
        "sw_lng": args.sw_lng,
        "ne_lat": args.ne_lat,
        "ne_lng": args.ne_lng,
    }

    # Build output directory: ./leads/YYYY-MM-DD/query-slug/
    output_dir = build_output_dir(args.query)
    output_html = output_dir / "leads_report.html"
    output_json = output_dir / "leads_data.json"

    print(f"Query:   {args.query}")
    print(f"Grid:    {args.grid_size}x{args.grid_size} = {args.grid_size ** 2} cells")
    print(f"Filter:  {args.filter}")
    print(f"Bounds:  ({bounds['sw_lat']}, {bounds['sw_lng']}) -> ({bounds['ne_lat']}, {bounds['ne_lng']})")
    print(f"Output:  {output_dir}/")
    print()

    places = deep_search(api_key, args.query, bounds, args.grid_size)
    print(f"\nTotal unique results found: {len(places)}")

    filter_label = "Todos"
    if args.filter == "no-website":
        before = len(places)
        places = [p for p in places if not p.get("websiteUri")]
        filter_label = "Solo sin sitio web"
        print(f"After filter (no website): {len(places)} (removed {before - len(places)})")

    # Sort by rating descending, then by review count
    places.sort(key=lambda p: (p.get("rating", 0), p.get("userRatingCount", 0)), reverse=True)

    # Save raw JSON
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(places, f, ensure_ascii=False, indent=2)
    print(f"\nJSON data:   {output_json}")

    # Generate HTML report
    template_path = Path(__file__).parent.parent / "templates" / "report_template.html"
    generate_report(places, args.query, filter_label, output_html, template_path, api_key)
    print(f"HTML report: {output_html}")
    print("\nDone.")


if __name__ == "__main__":
    main()
