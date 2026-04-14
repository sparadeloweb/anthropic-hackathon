---
name: sales-pricing
model: sonnet
description: Generates client-ready commercial budgets from roadmaps previously produced by the sales-roadmap skill. Use it when the user asks for a budget, a quote, to price a roadmap, or to put together a commercial proposal for a client. Locates the roadmap for the given client+project, extracts hours by role, applies per-role hourly rates, and writes a Markdown and PDF budget with the total.
---

# Pricing layer on top of sales-roadmap

This skill reads a roadmap already produced by `sales-roadmap` and generates a commercial budget by applying hourly rates per role. It normalizes the roadmap's Spanish role names (Backend, Frontend, Arquitectura, Diseño, Discovery) to the canonical English commercial roles (Backend, Frontend, Architecture, Design, Project Management, Product Owner).

## When to use it

- "Put together a budget for this project"
- "Price this roadmap"
- "How much do we charge the client for this?"
- "I need a budget to send to the client"
- "Prepare the commercial proposal for project X for client Y"

## How it works

1. **Source of truth** — roadmaps live in `<repo_root>/roadmaps/<client_slug>/<project_slug>.{md,pdf}` (or `<feature_slug>.{md,pdf}` for feature-mode roadmaps), produced by `sales-roadmap`.
2. **User input** — JSON with `client`, `project`, `hourly_rates` (rates for the six canonical roles) and optional `currency` (default `USD`).
3. **Parser** — finds the roadmap file for that client+project, preferring the `.md` sidecar (robust to parse) and falling back to the `.pdf` if the Markdown is missing. Extracts hours by role, phases, and totals. Tolerates both current (`Horas por área`) and legacy (`Horas por departamento`) section headings.
4. **Normalization** — maps Spanish names to commercial categories: `Arquitectura→Architecture`, `Diseño→Design`, `Discovery→Product Owner`. Backend and Frontend pass through. `Project Management` stays at 0h if the roadmap does not include it.
5. **Output** — Markdown + PDF written to `<repo_root>/budgets/<client_slug>/<project_slug>.{md,pdf}` (or `<feature_slug>.{md,pdf}` when pricing a feature), with executive summary, breakdown by role, project phases, and assumptions.

The PDF uses the same styling as `sales-roadmap`, so the commercial documents keep a consistent visual identity.

## Workflow

When the user asks you to quote a project:

1. **Verify the roadmap exists** — look in `<repo_root>/roadmaps/` for a folder matching the client slug. If it is not there, tell the user to run `sales-roadmap` first. This skill does not compute hours, only prices them.

2. **Collect the input** by asking the user for anything missing:
   - Client / lead name (`client`) — must match the one used when generating the roadmap
   - (Optional) `client_slug` — use this to pin the folder name if the auto-slug would differ from the existing roadmap folder
   - Project name (`project`) — idem
   - (Optional) `feature` — when present, the skill prices a feature-mode roadmap (`<feature_slug>.md`) instead of the project one
   - Hourly rates per role (`hourly_rates`): `backend`, `frontend`, `architecture`, `design`, `project_management`, `product_owner`
   - (Optional) `currency` — default `USD`

3. **Save the input** as `examples/<client-slug>-rates.json` (or reuse an existing one).

4. **Run**:
   ```bash
   cd .claude/skills/sales-pricing
   uv run --with pyyaml --with markdown-pdf python scripts/pricing.py examples/<file>.json
   ```
   This writes two files in `<repo_root>/budgets/<client_slug>/<slug>.{md,pdf}` where `<slug>` is `feature_slug` when pricing a feature, otherwise `project_slug`.

5. **Present the result** to the user: show the total in the chosen currency, the path to the PDF, and the Markdown content of the budget (breakdown by role and phases).

## Roadmap selection

- Looks in `<repo_root>/roadmaps/<client_slug>/` for the file `<project_slug>.md` (or `.pdf` as a fallback).
- If the input has a `feature` field, looks for `<feature_slug>.md` instead.
- Supports legacy timestamped filenames (`<slug>-<timestamp>.{md,pdf}`): picks the most recent by modification time.
- Logs which file was used to stderr: `[INFO] Using roadmap: <path>`.

## Canonical roles

| Commercial role | Source name(s) in the roadmap |
|---|---|
| Backend | Backend |
| Frontend | Frontend |
| Architecture | Arquitectura / Architecture |
| Design | Diseño / Design |
| Project Management | Project Management / PM (not in base roadmap; defaults to 0h) |
| Product Owner | Discovery / Product Owner |

If the roadmap contains a role that is not in the map, the budget will still include it with a 0 rate — extend `scripts/parser.py::ROLE_MAP` to map it formally.

## Expected input (JSON)

```json
{
  "client": "Clínica San Martín",
  "client_slug": "clinica-san-martin",
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
```

Legacy Spanish keys (`cliente`, `proyecto`, `cliente_slug`) are also accepted for backwards compatibility with existing `sales-roadmap` inputs.

## Maintenance

- **Add a new role**: add it to `scripts/parser.py` (`ROLE_MAP` and `CANONICAL_ROLES`) and to `scripts/render.py` (`RATE_KEY_BY_ROLE`).
- **Change default currency**: pass `currency` in the input (not hardcoded).
- **Update PDF styling**: edit `PDF_CSS` in `scripts/pricing.py`. Keep it in sync with `sales-roadmap` for visual consistency.
- **Add taxes / discounts / PM overhead**: extend `scripts/render.py::compute_budget` (out of MVP scope).

## Dependencies

- Python 3.10+
- `pyyaml` + `markdown-pdf` (bring in `pymupdf` for PDF parsing, installed on-demand via `uv run --with`)

## Implicit assumptions

- Roadmap hours are in the "Semi" scale (ideal hours before any seniority adjustment). The budget prices these directly at the role's hourly rate.
- Currency is homogeneous: all rates are in the same unit (`currency`).
- Budget validity: 30 days (editable in `render.py`).
- Excludes taxes, infrastructure, third-party licenses.
