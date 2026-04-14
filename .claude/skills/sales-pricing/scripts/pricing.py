"""Entry point for the sales-pricing skill.

Locates the most recent roadmap (MD or PDF) produced by sales-roadmap for a
given client+project, extracts hours per role, applies the hourly rates, and
writes a budget MD + PDF under
`budgets/<client_slug>/<project_slug>-<timestamp>.{md,pdf}`.

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
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from parser import parse_roadmap
from render import render, compute_budget

SKILL_ROOT = Path(__file__).resolve().parent.parent
BUDGETS_DIR = SKILL_ROOT / "budgets"
ROADMAPS_DIR = SKILL_ROOT.parent / "sales-roadmap" / "roadmaps"


def _slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[áàä]", "a", text)
    text = re.sub(r"[éèë]", "e", text)
    text = re.sub(r"[íìï]", "i", text)
    text = re.sub(r"[óòö]", "o", text)
    text = re.sub(r"[úùü]", "u", text)
    text = re.sub(r"ñ", "n", text)
    text = re.sub(r"[^a-z0-9\-_ ]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text or "project"


def _find_roadmap_file(client_slug: str, project_slug: str) -> Path:
    """Returns the most recent roadmap file for the given client+project.
    Prefers MD (more robust to parse) over PDF."""
    client_dir = ROADMAPS_DIR / client_slug
    if not client_dir.exists():
        raise FileNotFoundError(
            f"No roadmap folder found for client '{client_slug}': {client_dir}"
        )

    md_files = sorted(
        client_dir.glob(f"{project_slug}-*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if md_files:
        return md_files[0]

    pdf_files = sorted(
        client_dir.glob(f"{project_slug}-*.pdf"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if pdf_files:
        return pdf_files[0]

    raise FileNotFoundError(
        f"No roadmap found for project '{project_slug}' in {client_dir}. "
        f"Generate it first with the sales-roadmap skill."
    )


def _write_pdf(md_text: str, pdf_path: Path, title: str) -> None:
    from markdown_pdf import MarkdownPdf, Section
    pdf = MarkdownPdf(toc_level=2)
    pdf.meta["title"] = title
    pdf.add_section(Section(md_text, toc=False))
    pdf.save(str(pdf_path))


REQUIRED_RATE_KEYS = [
    "backend", "frontend", "architecture", "design",
    "project_management", "product_owner",
]


def _read_input_field(data: dict, *candidates: str, required: bool = True) -> str:
    """Reads the first present field from candidates. Supports legacy Spanish
    keys (`cliente`, `proyecto`) alongside the canonical English ones."""
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

    missing = [k for k in REQUIRED_RATE_KEYS if k not in rates]
    if missing:
        print(f"[ERROR] Missing rates in hourly_rates: {missing}", file=sys.stderr)
        return 1

    client_slug = _slugify(client)
    project_slug = _slugify(project)

    roadmap_file = _find_roadmap_file(client_slug, project_slug)
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

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target_dir = BUDGETS_DIR / client_slug
    target_dir.mkdir(parents=True, exist_ok=True)
    md_path = target_dir / f"{project_slug}-{timestamp}.md"
    pdf_path = target_dir / f"{project_slug}-{timestamp}.pdf"

    md_path.write_text(md, encoding="utf-8")
    _write_pdf(md, pdf_path, title=f"Budget — {project}")

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
