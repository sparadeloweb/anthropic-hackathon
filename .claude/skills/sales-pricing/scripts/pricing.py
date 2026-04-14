"""Entry point for the sales-pricing skill.

Locates the most recent roadmap (MD or PDF) produced by sales-roadmap for a
given client+project, extracts hours per role, applies the hourly rates, and
writes a budget MD + PDF under
`<repo_root>/budgets/<client_slug>/<project_slug>.{md,pdf}`.

Both the source roadmaps (`<repo_root>/roadmaps/`) and the generated budgets
(`<repo_root>/budgets/`) live at the repo root, mirroring the convention used
by the sales-roadmap skill.

Usage:
    python pricing.py path/to/input.json
    python pricing.py path/to/input.json --stdout

Expected input JSON:
    {
      "client": "Clínica San Martín",
      "project": "SaaS de gestión de turnos",
      "currency": "USD",
      "hourly_rates": {
        "backend": 55,
        "frontend": 50,
        "architecture": 70,
        "design": 45,
        "project_management": 50,
        "product_owner": 60
      }
    }

Optional fields:
    - "client_slug": override the auto-generated slug (useful to match an
      existing roadmap folder name).
    - "feature": price a feature-mode roadmap (`<feature_slug>.md`) instead
      of the full project one.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from parser import parse_roadmap
from render import render, compute_budget

SKILL_ROOT = Path(__file__).resolve().parent.parent
# .claude/skills/sales-pricing -> repo root is 3 levels up
REPO_ROOT = SKILL_ROOT.parent.parent.parent
ROADMAPS_DIR = REPO_ROOT / "roadmaps"
BUDGETS_DIR = REPO_ROOT / "budgets"

# Shared PDF styling, kept in sync with sales-roadmap for a consistent look.
PDF_CSS = """
<style>
body {
    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    font-size: 13px;
    line-height: 1.6;
    color: #1a1a1a;
}
h1 {
    font-size: 26px;
    font-weight: 700;
    color: #111;
    border-bottom: 3px solid #2563eb;
    padding-bottom: 10px;
    margin-bottom: 24px;
}
h2 {
    font-size: 17px;
    font-weight: 600;
    color: #1e40af;
    margin-top: 28px;
    margin-bottom: 12px;
    border-bottom: 1px solid #e5e7eb;
    padding-bottom: 6px;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 20px 0;
    font-size: 12px;
}
thead tr, tr:first-child {
    background-color: #1e40af;
    color: #ffffff;
}
th, td {
    padding: 8px 12px;
    border: 1px solid #d1d5db;
    text-align: left;
}
tr:nth-child(even) { background-color: #f8fafc; }
tr:nth-child(odd) { background-color: #ffffff; }
ul { margin: 8px 0; padding-left: 20px; }
li { margin-bottom: 4px; }
strong { color: #111; }
code {
    background: #f3f4f6;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 12px;
}
</style>
"""


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
    return text or "project"


def _find_roadmap_file(client_slug: str, project_slug: str, feature_slug: str | None) -> Path:
    """Returns the roadmap file for the given client+project (or feature).
    Prefers MD (robust to parse) over PDF. If multiple timestamped files exist
    (legacy), returns the most recent by mtime."""
    client_dir = ROADMAPS_DIR / client_slug
    if not client_dir.exists():
        raise FileNotFoundError(
            f"No roadmap folder found for client '{client_slug}': {client_dir}"
        )

    slug = feature_slug or project_slug
    # Exact match first (new convention: `<slug>.md`).
    for ext in (".md", ".pdf"):
        exact = client_dir / f"{slug}{ext}"
        if exact.exists():
            return exact

    # Legacy timestamped files: `<slug>-<timestamp>.{md,pdf}`.
    for ext in (".md", ".pdf"):
        matches = sorted(
            client_dir.glob(f"{slug}-*{ext}"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if matches:
            return matches[0]

    raise FileNotFoundError(
        f"No roadmap found for '{slug}' in {client_dir}. "
        f"Generate it first with the sales-roadmap skill."
    )


def _write_pdf(md_text: str, pdf_path: Path, title: str) -> None:
    from markdown_pdf import MarkdownPdf, Section
    pdf = MarkdownPdf(toc_level=2)
    pdf.meta["title"] = title
    styled_md = PDF_CSS + "\n\n" + md_text
    pdf.add_section(Section(styled_md, toc=False))
    pdf.save(str(pdf_path))


REQUIRED_RATE_KEYS = [
    "backend", "frontend", "architecture", "design",
    "project_management", "product_owner",
]


def _read_input_field(data: dict, *candidates: str, required: bool = True) -> str:
    """Returns the first present field among candidates. Accepts legacy
    Spanish keys (`cliente`, `proyecto`) alongside the canonical English ones."""
    for key in candidates:
        if key in data and data[key]:
            return data[key]
    if required:
        raise KeyError(f"Missing required input field (any of): {candidates}")
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pricing layer on top of sales-roadmap."
    )
    parser.add_argument("input", help="Path to input JSON (client, project, hourly_rates)")
    parser.add_argument("--stdout", action="store_true", help="Also print the MD to stdout")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[ERROR] Input file not found: {input_path}", file=sys.stderr)
        return 1

    data = json.loads(input_path.read_text(encoding="utf-8"))
    client = _read_input_field(data, "client", "cliente")
    project = _read_input_field(data, "project", "proyecto")
    currency = data.get("currency", "USD")
    rates = data.get("hourly_rates", {})
    feature = data.get("feature")

    missing = [k for k in REQUIRED_RATE_KEYS if k not in rates]
    if missing:
        print(f"[ERROR] Missing rates in hourly_rates: {missing}", file=sys.stderr)
        return 1

    # Honor explicit client_slug (used by sales-roadmap to pin the folder name).
    client_slug = data.get("client_slug") or data.get("cliente_slug") or _slugify(client)
    project_slug = _slugify(project)
    feature_slug = _slugify(feature) if feature else None
    file_prefix = feature_slug or project_slug

    roadmap_file = _find_roadmap_file(client_slug, project_slug, feature_slug)
    print(f"[INFO] Using roadmap: {roadmap_file}", file=sys.stderr)

    parsed = parse_roadmap(roadmap_file)
    if not parsed["hours_by_role"]:
        print(
            "[ERROR] Could not extract hours by department from the roadmap. "
            "Check the source file format.",
            file=sys.stderr,
        )
        return 1

    md = render(parsed, rates, client=client, project=project, currency=currency)
    title = f"Budget — {project}" + (f" — {feature}" if feature else "")

    target_dir = BUDGETS_DIR / client_slug
    target_dir.mkdir(parents=True, exist_ok=True)
    md_path = target_dir / f"{file_prefix}.md"
    pdf_path = target_dir / f"{file_prefix}.pdf"

    md_path.write_text(md, encoding="utf-8")
    _write_pdf(md, pdf_path, title=title)

    budget = compute_budget(parsed["hours_by_role"], rates)
    print(
        f"[OK] Total: {currency} {budget['total']:,.2f}  "
        f"({budget['total_hours']:.1f} hours)",
        file=sys.stderr,
    )
    print(f"[OK] Markdown: {md_path}", file=sys.stderr)
    print(f"[OK] PDF:      {pdf_path}", file=sys.stderr)

    if args.stdout:
        sys.stdout.write(md)

    return 0


if __name__ == "__main__":
    sys.exit(main())
