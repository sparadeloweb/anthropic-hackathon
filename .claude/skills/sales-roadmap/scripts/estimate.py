"""Entry point de la skill. Recibe un JSON de input y genera el roadmap en Markdown y PDF.

Guarda ambos archivos bajo <skill_root>/roadmaps/<cliente_slug>/<proyecto_slug>-<timestamp>.{md,pdf}.

Uso:
    python estimate.py path/to/input.json
    python estimate.py path/to/input.json --stdout    # además imprime el MD por stdout
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from catalog import load_catalog
from render import render
from roster import load_roster
from scheduler import build_roadmap

SKILL_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = SKILL_ROOT.parent.parent.parent  # .claude/skills/sales-roadmap -> repo root
ROADMAPS_DIR = REPO_ROOT / "roadmaps"


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
    return text or "proyecto"


def _write_pdf(md_text: str, pdf_path: Path, title: str) -> None:
    from markdown_pdf import MarkdownPdf, Section
    pdf = MarkdownPdf(toc_level=2)
    pdf.meta["title"] = title
    pdf.add_section(Section(md_text, toc=False))
    pdf.save(str(pdf_path))


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimador de roadmap de producto.")
    parser.add_argument("input", help="Ruta al JSON de input del proyecto")
    parser.add_argument(
        "--stdout", action="store_true", help="Imprime también el Markdown por stdout"
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[ERROR] No se encontró el archivo de input: {input_path}", file=sys.stderr)
        return 1

    with open(input_path, encoding="utf-8") as f:
        input_data = json.load(f)

    catalog = load_catalog()
    roster = load_roster()
    roadmap = build_roadmap(input_data, catalog, roster)
    md = render(roadmap, catalog.config, roster.holidays)

    # Organizar por cliente (lead). Si no se pasa, se usa el nombre del proyecto.
    cliente = input_data.get("cliente") or input_data.get("lead") or input_data["proyecto"]
    cliente_slug = _slugify(cliente)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Si es una feature nueva para proyecto existente, usar el nombre de la feature como prefijo.
    feature = input_data.get("feature")
    if feature:
        file_prefix = _slugify(feature)
        pdf_title = f"Roadmap — {input_data['proyecto']} — Feature: {feature}"
    else:
        file_prefix = _slugify(input_data["proyecto"])
        pdf_title = f"Roadmap — {input_data['proyecto']}"

    target_dir = ROADMAPS_DIR / cliente_slug
    target_dir.mkdir(parents=True, exist_ok=True)

    md_path = target_dir / f"{file_prefix}-{timestamp}.md"
    pdf_path = target_dir / f"{file_prefix}-{timestamp}.pdf"

    md_path.write_text(md, encoding="utf-8")
    _write_pdf(md, pdf_path, title=pdf_title)

    print(f"[OK] Markdown: {md_path}", file=sys.stderr)
    print(f"[OK] PDF:      {pdf_path}", file=sys.stderr)

    if args.stdout:
        sys.stdout.write(md)

    return 0


if __name__ == "__main__":
    sys.exit(main())
