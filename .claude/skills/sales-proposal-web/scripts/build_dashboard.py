"""Generates a self-contained HTML dashboard for a lead.

Consolidates: lead data (Google Places), Stitch design screenshots,
sales proposal, budget, and roadmap into a single tabbed HTML file.

Usage:
    python build_dashboard.py <lead-slug>

Output:
    <repo_root>/proposals/<lead-slug>/dashboard.html
"""
from __future__ import annotations

import base64
import json
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = SKILL_ROOT.parent.parent.parent

LEADS_DIR = REPO_ROOT / "leads"
STITCH_DIR = REPO_ROOT / "stitch_designs"
ROADMAPS_DIR = REPO_ROOT / "roadmaps"
BUDGETS_DIR = REPO_ROOT / "budgets"
PROPOSALS_DIR = REPO_ROOT / "proposals"

# ── i18n ──────────────────────────────────────────────────────────────────────

TRANSLATIONS = {
    "es": {
        "lang": "es",
        "title_prefix": "Propuesta comercial",
        "tab_business": "Negocio",
        "tab_design": "Diseño",
        "tab_proposal": "Propuesta",
        "tab_budget": "Presupuesto",
        "tab_roadmap": "Roadmap",
        "business_type": "Tipo de negocio",
        "rating": "Calificación",
        "reviews_title": "Reseñas destacadas",
        "address": "Dirección",
        "phone": "Teléfono",
        "hours": "Horarios",
        "no_website": "Sin sitio web actualmente",
        "has_website": "Sitio web actual",
        "design_title": "Diseño propuesto",
        "design_system": "Sistema de diseño",
        "color_mode": "Modo de color",
        "colors": "Colores",
        "primary": "Primario",
        "neutral": "Neutro",
        "fonts": "Tipografías",
        "headlines": "Títulos",
        "body": "Cuerpo",
        "screens": "Pantallas diseñadas",
        "proposal_title": "Propuesta comercial",
        "budget_title": "Presupuesto",
        "roadmap_title": "Plan de ejecución",
        "stars": "estrellas",
        "reviews_count": "reseñas",
        "closed": "Cerrado",
    },
    "en": {
        "lang": "en",
        "title_prefix": "Commercial proposal",
        "tab_business": "Business",
        "tab_design": "Design",
        "tab_proposal": "Proposal",
        "tab_budget": "Budget",
        "tab_roadmap": "Roadmap",
        "business_type": "Business type",
        "rating": "Rating",
        "reviews_title": "Featured reviews",
        "address": "Address",
        "phone": "Phone",
        "hours": "Hours",
        "no_website": "No website currently",
        "has_website": "Current website",
        "design_title": "Proposed design",
        "design_system": "Design system",
        "color_mode": "Color mode",
        "colors": "Colors",
        "primary": "Primary",
        "neutral": "Neutral",
        "fonts": "Typography",
        "headlines": "Headlines",
        "body": "Body",
        "screens": "Designed screens",
        "proposal_title": "Commercial proposal",
        "budget_title": "Budget",
        "roadmap_title": "Execution plan",
        "stars": "stars",
        "reviews_count": "reviews",
        "closed": "Closed",
    },
    "pt": {
        "lang": "pt",
        "title_prefix": "Proposta comercial",
        "tab_business": "Negócio",
        "tab_design": "Design",
        "tab_proposal": "Proposta",
        "tab_budget": "Orçamento",
        "tab_roadmap": "Roadmap",
        "business_type": "Tipo de negócio",
        "rating": "Avaliação",
        "reviews_title": "Avaliações em destaque",
        "address": "Endereço",
        "phone": "Telefone",
        "hours": "Horários",
        "no_website": "Sem site atualmente",
        "has_website": "Site atual",
        "design_title": "Design proposto",
        "design_system": "Sistema de design",
        "color_mode": "Modo de cor",
        "colors": "Cores",
        "primary": "Primário",
        "neutral": "Neutro",
        "fonts": "Tipografia",
        "headlines": "Títulos",
        "body": "Corpo",
        "screens": "Telas projetadas",
        "proposal_title": "Proposta comercial",
        "budget_title": "Orçamento",
        "roadmap_title": "Plano de execução",
        "stars": "estrelas",
        "reviews_count": "avaliações",
        "closed": "Fechado",
    },
}

COUNTRY_LANG = {
    "AR": "es", "MX": "es", "CO": "es", "CL": "es", "PE": "es",
    "ES": "es", "UY": "es", "PY": "es", "EC": "es", "VE": "es",
    "BO": "es", "CR": "es", "DO": "es", "GT": "es", "HN": "es",
    "NI": "es", "PA": "es", "SV": "es", "CU": "es",
    "BR": "pt", "PT": "pt",
}


def detect_language(lead_data: dict | None) -> str:
    if not lead_data:
        return "es"
    region = lead_data.get("postalAddress", {}).get("regionCode", "")
    return COUNTRY_LANG.get(region, "en")


# ── Data loaders ──────────────────────────────────────────────────────────────

def find_lead_data(lead_slug: str) -> dict | None:
    """Searches all leads/ subdirectories for the lead matching the slug."""
    for data_file in LEADS_DIR.rglob("leads_data.json"):
        try:
            leads = json.loads(data_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        for lead in leads:
            name = lead.get("displayName", {}).get("text", "")
            if _slugify(name) == lead_slug or lead_slug in _slugify(name):
                return lead
    return None


def load_stitch(lead_slug: str) -> dict | None:
    stitch_dir = STITCH_DIR / lead_slug
    project_file = stitch_dir / "stitch_project.json"
    if not project_file.exists():
        return None
    data = json.loads(project_file.read_text(encoding="utf-8"))
    data["_screens_b64"] = []
    screens_dir = stitch_dir / "screens"
    for screen in data.get("screens", []):
        img_path = screens_dir / screen["file"]
        if img_path.exists():
            b64 = base64.b64encode(img_path.read_bytes()).decode()
            data["_screens_b64"].append({
                "name": screen.get("title") or screen.get("name", ""),
                "b64": b64,
                "ext": img_path.suffix.lstrip("."),
            })
    return data


def load_text_file(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def find_md_file(directory: Path) -> str:
    """Find the first .md file in a directory (excluding feature-mode files if a main one exists)."""
    if not directory.exists():
        return ""
    md_files = sorted(directory.glob("*.md"))
    if not md_files:
        return ""
    return md_files[0].read_text(encoding="utf-8")


def find_proposal_file(lead_slug: str) -> str:
    proposals_dir = PROPOSALS_DIR / lead_slug
    for name in ("propuesta.txt", "proposal.txt", "proposta.txt"):
        f = proposals_dir / name
        if f.exists():
            return f.read_text(encoding="utf-8")
    return ""


def _slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[áàä]", "a", text)
    text = re.sub(r"[éèë]", "e", text)
    text = re.sub(r"[íìï]", "i", text)
    text = re.sub(r"[óòö]", "o", text)
    text = re.sub(r"[úùü]", "u", text)
    text = re.sub(r"ñ", "n", text)
    text = re.sub(r"[^a-z0-9\- ]", "", text)
    text = re.sub(r"[\s]+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    text = text.strip("-")
    return text or "lead"


# ── Markdown to HTML (minimal) ───────────────────────────────────────────────

def md_to_html(md: str) -> str:
    """Minimal markdown → HTML conversion for tables, headers, lists, bold."""
    lines = md.splitlines()
    html_lines = []
    in_table = False
    in_list = False
    first_row = True

    for line in lines:
        stripped = line.strip()

        # Skip mermaid blocks
        if stripped.startswith("```mermaid"):
            continue
        if stripped.startswith("```") and in_table is False:
            continue

        # Tables
        if stripped.startswith("|"):
            if "---" in stripped:
                continue
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if not in_table:
                html_lines.append('<table>')
                in_table = True
                first_row = True
            if first_row:
                html_lines.append('<tr>' + ''.join(f'<th>{_inline(c)}</th>' for c in cells) + '</tr>')
                first_row = False
            else:
                html_lines.append('<tr>' + ''.join(f'<td>{_inline(c)}</td>' for c in cells) + '</tr>')
            continue
        elif in_table:
            html_lines.append('</table>')
            in_table = False
            first_row = True

        # Lists
        if stripped.startswith("- "):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{_inline(stripped[2:])}</li>')
            continue
        elif in_list and not stripped.startswith("  "):
            html_lines.append('</ul>')
            in_list = False

        # Headers
        if stripped.startswith("# "):
            html_lines.append(f'<h1>{_inline(stripped[2:])}</h1>')
        elif stripped.startswith("## "):
            html_lines.append(f'<h2>{_inline(stripped[3:])}</h2>')
        elif stripped.startswith("### "):
            html_lines.append(f'<h3>{_inline(stripped[4:])}</h3>')
        elif stripped:
            html_lines.append(f'<p>{_inline(stripped)}</p>')

    if in_table:
        html_lines.append('</table>')
    if in_list:
        html_lines.append('</ul>')

    return '\n'.join(html_lines)


def _inline(text: str) -> str:
    """Convert inline markdown (bold, code) to HTML."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text


# ── HTML Template ─────────────────────────────────────────────────────────────

def build_html(
    lead_slug: str,
    lead_data: dict | None,
    stitch: dict | None,
    proposal: str,
    budget_md: str,
    roadmap_md: str,
    t: dict,
) -> str:
    lead_name = ""
    if lead_data:
        lead_name = lead_data.get("displayName", {}).get("text", lead_slug)
    elif stitch:
        lead_name = stitch.get("leadName", lead_slug)
    else:
        lead_name = lead_slug

    # Build each tab's content
    business_html = _build_business_tab(lead_data, t)
    design_html = _build_design_tab(stitch, t)
    proposal_html = _build_proposal_tab(proposal, t)
    budget_html = _build_budget_tab(budget_md, t)
    roadmap_html = _build_roadmap_tab(roadmap_md, t)

    return f"""<!DOCTYPE html>
<html lang="{t['lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{t['title_prefix']} — {_escape(lead_name)}</title>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: #0f172a;
    color: #e2e8f0;
    min-height: 100vh;
}}

/* Header */
.header {{
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-bottom: 1px solid #334155;
    padding: 24px 32px;
}}
.header h1 {{
    font-size: 22px;
    font-weight: 600;
    color: #f8fafc;
}}
.header .subtitle {{
    font-size: 13px;
    color: #94a3b8;
    margin-top: 4px;
}}

/* Tabs */
.tabs {{
    display: flex;
    gap: 0;
    background: #1e293b;
    border-bottom: 1px solid #334155;
    padding: 0 32px;
    overflow-x: auto;
}}
.tab-btn {{
    padding: 14px 24px;
    background: none;
    border: none;
    color: #94a3b8;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
    white-space: nowrap;
}}
.tab-btn:hover {{ color: #e2e8f0; }}
.tab-btn.active {{
    color: #60a5fa;
    border-bottom-color: #3b82f6;
}}

/* Content */
.content {{
    max-width: 1100px;
    margin: 0 auto;
    padding: 32px;
}}
.tab-panel {{ display: none; }}
.tab-panel.active {{ display: block; }}

/* Cards */
.card {{
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
}}
.card h2 {{
    font-size: 16px;
    font-weight: 600;
    color: #f8fafc;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #334155;
}}
.card h3 {{
    font-size: 14px;
    font-weight: 600;
    color: #cbd5e1;
    margin: 16px 0 8px 0;
}}

/* Info grid */
.info-grid {{
    display: grid;
    grid-template-columns: 140px 1fr;
    gap: 8px 16px;
    font-size: 14px;
}}
.info-label {{ color: #94a3b8; font-weight: 500; }}
.info-value {{ color: #e2e8f0; }}

/* Rating */
.rating {{ display: flex; align-items: center; gap: 8px; }}
.stars {{ color: #fbbf24; font-size: 16px; }}
.rating-text {{ color: #94a3b8; font-size: 13px; }}

/* Reviews */
.review {{
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
    font-size: 14px;
    line-height: 1.6;
    color: #cbd5e1;
    font-style: italic;
}}

/* Hours */
.hours-list {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 4px;
    font-size: 13px;
}}
.hours-item {{ color: #94a3b8; }}

/* Design gallery */
.gallery {{
    display: grid;
    grid-template-columns: 1fr;
    gap: 24px;
}}
.screen-card {{
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 8px;
    overflow: hidden;
}}
.screen-card img {{
    width: 100%;
    display: block;
}}
.screen-card .screen-name {{
    padding: 12px 16px;
    font-size: 13px;
    font-weight: 500;
    color: #94a3b8;
    border-top: 1px solid #334155;
}}

/* Color swatches */
.swatches {{
    display: flex;
    gap: 12px;
    margin-top: 8px;
}}
.swatch {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
}}
.swatch-circle {{
    width: 24px;
    height: 24px;
    border-radius: 50%;
    border: 2px solid #475569;
}}

/* Proposal */
.proposal-text {{
    font-size: 15px;
    line-height: 1.8;
    color: #e2e8f0;
    white-space: pre-wrap;
    font-family: 'Segoe UI', system-ui, sans-serif;
}}

/* Tables (budget/roadmap) */
.content table {{
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    font-size: 13px;
}}
.content th {{
    background: #334155;
    color: #f8fafc;
    padding: 10px 14px;
    text-align: left;
    font-weight: 600;
}}
.content td {{
    padding: 10px 14px;
    border-bottom: 1px solid #334155;
    color: #cbd5e1;
}}
.content tr:hover td {{ background: rgba(59, 130, 246, 0.05); }}
.content h1 {{ font-size: 20px; color: #f8fafc; margin-bottom: 16px; }}
.content h2 {{ font-size: 16px; color: #60a5fa; margin: 24px 0 12px 0; border-bottom: 1px solid #334155; padding-bottom: 6px; }}
.content p {{ margin: 8px 0; font-size: 14px; line-height: 1.6; }}
.content ul {{ padding-left: 20px; margin: 8px 0; }}
.content li {{ margin: 4px 0; font-size: 14px; }}
.content strong {{ color: #f8fafc; }}
.content code {{ background: #334155; padding: 2px 6px; border-radius: 3px; font-size: 12px; }}

/* Badge */
.badge {{
    display: inline-block;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
}}
.badge-warn {{ background: #78350f; color: #fbbf24; }}
.badge-ok {{ background: #064e3b; color: #34d399; }}
</style>
</head>
<body>

<div class="header">
    <h1>{_escape(lead_name)}</h1>
    <div class="subtitle">{t['title_prefix']}</div>
</div>

<div class="tabs">
    <button class="tab-btn active" onclick="showTab('business')">{t['tab_business']}</button>
    <button class="tab-btn" onclick="showTab('design')">{t['tab_design']}</button>
    <button class="tab-btn" onclick="showTab('proposal')">{t['tab_proposal']}</button>
    <button class="tab-btn" onclick="showTab('budget')">{t['tab_budget']}</button>
    <button class="tab-btn" onclick="showTab('roadmap')">{t['tab_roadmap']}</button>
</div>

<div class="content">
    <div id="tab-business" class="tab-panel active">{business_html}</div>
    <div id="tab-design" class="tab-panel">{design_html}</div>
    <div id="tab-proposal" class="tab-panel">{proposal_html}</div>
    <div id="tab-budget" class="tab-panel">{budget_html}</div>
    <div id="tab-roadmap" class="tab-panel">{roadmap_html}</div>
</div>

<script>
function showTab(id) {{
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('tab-' + id).classList.add('active');
    event.target.classList.add('active');
}}
</script>
</body>
</html>"""


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _build_business_tab(lead: dict | None, t: dict) -> str:
    if not lead:
        return f'<div class="card"><p>No lead data found.</p></div>'

    name = lead.get("displayName", {}).get("text", "")
    biz_type = lead.get("primaryTypeDisplayName", {}).get("text", "")
    rating = lead.get("rating", 0)
    review_count = lead.get("userRatingCount", 0)
    address = lead.get("formattedAddress", "")
    phone = lead.get("internationalPhoneNumber", "")
    website = lead.get("websiteUri", "")
    hours_list = lead.get("regularOpeningHours", {}).get("weekdayDescriptions", [])
    reviews = lead.get("reviews", [])

    stars_html = "★" * int(rating) + ("½" if rating % 1 >= 0.5 else "")
    website_html = (
        f'<span class="badge badge-ok">{_escape(website)}</span>'
        if website
        else f'<span class="badge badge-warn">{t["no_website"]}</span>'
    )

    reviews_html = ""
    for r in reviews[:4]:
        text = r.get("text", {}).get("text", "")
        if text:
            reviews_html += f'<div class="review">"{_escape(text[:300])}"</div>'

    hours_html = ""
    for h in hours_list:
        hours_html += f'<div class="hours-item">{_escape(h)}</div>'

    return f"""
<div class="card">
    <h2>{_escape(name)}</h2>
    <div class="info-grid">
        <div class="info-label">{t['business_type']}</div>
        <div class="info-value">{_escape(biz_type)}</div>
        <div class="info-label">{t['rating']}</div>
        <div class="info-value">
            <div class="rating">
                <span class="stars">{stars_html}</span>
                <span>{rating}</span>
                <span class="rating-text">({review_count} {t['reviews_count']})</span>
            </div>
        </div>
        <div class="info-label">{t['address']}</div>
        <div class="info-value">{_escape(address)}</div>
        <div class="info-label">{t['phone']}</div>
        <div class="info-value">{_escape(phone)}</div>
        <div class="info-label">Web</div>
        <div class="info-value">{website_html}</div>
    </div>
</div>
<div class="card">
    <h2>{t['hours']}</h2>
    <div class="hours-list">{hours_html}</div>
</div>
{'<div class="card"><h2>' + t["reviews_title"] + '</h2>' + reviews_html + '</div>' if reviews_html else ''}
"""


def _build_design_tab(stitch: dict | None, t: dict) -> str:
    if not stitch:
        return f'<div class="card"><p>No Stitch design found.</p></div>'

    ds = stitch.get("designSystem", {})
    ds_name = ds.get("name", "")
    color_mode = ds.get("colorMode", "")
    primary = ds.get("primaryColor", "")
    neutral = ds.get("neutralColor", "")
    headline_font = ds.get("headlineFont", "")
    body_font = ds.get("bodyFont", "")

    screens_html = ""
    for s in stitch.get("_screens_b64", []):
        screens_html += f"""
<div class="screen-card">
    <img src="data:image/{s['ext']};base64,{s['b64']}" alt="{_escape(s['name'])}">
    <div class="screen-name">{_escape(s['name'])}</div>
</div>"""

    return f"""
<div class="card">
    <h2>{t['design_system']}</h2>
    <div class="info-grid">
        <div class="info-label">Nombre</div>
        <div class="info-value">{_escape(ds_name)}</div>
        <div class="info-label">{t['color_mode']}</div>
        <div class="info-value">{_escape(color_mode)}</div>
        <div class="info-label">{t['fonts']}</div>
        <div class="info-value">{t['headlines']}: {_escape(headline_font)} / {t['body']}: {_escape(body_font)}</div>
    </div>
    <h3>{t['colors']}</h3>
    <div class="swatches">
        <div class="swatch">
            <div class="swatch-circle" style="background:{primary};"></div>
            <span>{t['primary']}: {primary}</span>
        </div>
        <div class="swatch">
            <div class="swatch-circle" style="background:{neutral};"></div>
            <span>{t['neutral']}: {neutral}</span>
        </div>
    </div>
</div>
<div class="card">
    <h2>{t['screens']} ({len(stitch.get('_screens_b64', []))})</h2>
    <div class="gallery">{screens_html}</div>
</div>
"""


def _build_proposal_tab(proposal: str, t: dict) -> str:
    if not proposal:
        return f'<div class="card"><p>No proposal found.</p></div>'
    return f"""
<div class="card">
    <h2>{t['proposal_title']}</h2>
    <div class="proposal-text">{_escape(proposal)}</div>
</div>
"""


def _build_budget_tab(budget_md: str, t: dict) -> str:
    if not budget_md:
        return f'<div class="card"><p>No budget found.</p></div>'
    return f'<div class="card"><h2>{t["budget_title"]}</h2>{md_to_html(budget_md)}</div>'


def _build_roadmap_tab(roadmap_md: str, t: dict) -> str:
    if not roadmap_md:
        return f'<div class="card"><p>No roadmap found.</p></div>'
    return f'<div class="card"><h2>{t["roadmap_title"]}</h2>{md_to_html(roadmap_md)}</div>'


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python build_dashboard.py <lead-slug>", file=sys.stderr)
        return 1

    lead_slug = sys.argv[1]

    # Load all data sources
    print(f"[INFO] Loading data for lead: {lead_slug}", file=sys.stderr)

    lead_data = find_lead_data(lead_slug)
    if lead_data:
        print(f"[OK] Lead data found", file=sys.stderr)
    else:
        print(f"[WARN] No lead data found in leads/", file=sys.stderr)

    stitch = load_stitch(lead_slug)
    if stitch:
        print(f"[OK] Stitch design: {len(stitch.get('_screens_b64', []))} screens", file=sys.stderr)
    else:
        print(f"[WARN] No Stitch design found in stitch_designs/{lead_slug}/", file=sys.stderr)

    roadmap_md = find_md_file(ROADMAPS_DIR / lead_slug)
    print(f"[{'OK' if roadmap_md else 'WARN'}] Roadmap: {'found' if roadmap_md else 'not found'}", file=sys.stderr)

    budget_md = find_md_file(BUDGETS_DIR / lead_slug)
    print(f"[{'OK' if budget_md else 'WARN'}] Budget: {'found' if budget_md else 'not found'}", file=sys.stderr)

    proposal = find_proposal_file(lead_slug)
    print(f"[{'OK' if proposal else 'WARN'}] Proposal: {'found' if proposal else 'not found'}", file=sys.stderr)

    # Detect language from lead location
    lang = detect_language(lead_data)
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    print(f"[INFO] Language: {lang}", file=sys.stderr)

    # Generate HTML
    html = build_html(lead_slug, lead_data, stitch, proposal, budget_md, roadmap_md, t)

    # Write output
    output_dir = PROPOSALS_DIR / lead_slug
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "dashboard.html"
    output_path.write_text(html, encoding="utf-8")

    print(f"[OK] Dashboard: {output_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
