"""Entry point de la skill. Recibe un JSON de input y genera el roadmap en Markdown.

Uso:
    python estimate.py path/to/input.json > roadmap.md
    python estimate.py path/to/input.json -o roadmap.md
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from catalog import load_catalog
from render import render
from roster import load_roster
from scheduler import build_roadmap


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimador de roadmap de producto.")
    parser.add_argument("input", help="Ruta al JSON de input del proyecto")
    parser.add_argument("-o", "--output", help="Ruta del Markdown de salida (default: stdout)")
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

    if args.output:
        Path(args.output).write_text(md, encoding="utf-8")
        print(f"[OK] Roadmap escrito en {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(md)

    return 0


if __name__ == "__main__":
    sys.exit(main())
