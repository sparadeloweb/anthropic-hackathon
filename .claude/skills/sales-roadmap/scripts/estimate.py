"""Entry point de la skill. Recibe un JSON de input y genera el roadmap en Markdown y PDF.

Guarda ambos archivos bajo <repo_root>/roadmaps/<cliente_slug>/<nombre>.{md,pdf}.

Uso:
    python estimate.py path/to/input.json
    python estimate.py path/to/input.json --stdout    # además imprime el MD por stdout
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from catalog import load_catalog
from render import render
from roster import load_roster
from scheduler import build_roadmap

SKILL_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = SKILL_ROOT.parent.parent.parent  # .claude/skills/sales-roadmap -> repo root
ROADMAPS_DIR = REPO_ROOT / "roadmaps"

# CSS para el PDF — diseño profesional orientado al cliente.
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
    text = re.sub(r"-{2,}", "-", text)  # colapsar guiones múltiples
    text = text.strip("-")
    return text or "proyecto"


def _write_pdf(md_text: str, pdf_path: Path, title: str) -> None:
    from markdown_pdf import MarkdownPdf, Section
    pdf = MarkdownPdf(toc_level=2)
    pdf.meta["title"] = title
    styled_md = PDF_CSS + "\n\n" + md_text
    pdf.add_section(Section(styled_md, toc=False))
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

    # Carpeta del cliente: usar cliente_slug explícito si viene en el input,
    # sino generar desde el nombre del cliente/lead.
    if input_data.get("cliente_slug"):
        cliente_slug = input_data["cliente_slug"]
    else:
        cliente = input_data.get("cliente") or input_data.get("lead") or input_data["proyecto"]
        cliente_slug = _slugify(cliente)

    # Nombre del archivo: feature slug o proyecto slug (sin timestamp).
    feature = input_data.get("feature")
    if feature:
        file_prefix = _slugify(feature)
        pdf_title = f"Roadmap — {input_data['proyecto']} — {feature}"
    else:
        file_prefix = _slugify(input_data["proyecto"])
        pdf_title = f"Roadmap — {input_data['proyecto']}"

    target_dir = ROADMAPS_DIR / cliente_slug
    target_dir.mkdir(parents=True, exist_ok=True)

    md_path = target_dir / f"{file_prefix}.md"
    pdf_path = target_dir / f"{file_prefix}.pdf"

    md_path.write_text(md, encoding="utf-8")
    _write_pdf(md, pdf_path, title=pdf_title)

    print(f"[OK] Markdown: {md_path}", file=sys.stderr)
    print(f"[OK] PDF:      {pdf_path}", file=sys.stderr)

    if args.stdout:
        sys.stdout.write(md)

    return 0


if __name__ == "__main__":
    sys.exit(main())
