---
name: sales-pricing
description: Generates client-ready commercial budgets from roadmaps previously produced by the sales-roadmap skill. Use it when the user asks for a budget, a quote, to price a roadmap, or to put together a commercial proposal for a client. Locates the most recent roadmap PDF for the given client+project, extracts hours by role, applies per-role hourly rates, and writes a Markdown and PDF budget with the total.
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

1. **Source of truth** — roadmaps already live in `../sales-roadmap/roadmaps/<client_slug>/<project_slug>-<timestamp>.{md,pdf}` produced by `sales-roadmap`.
2. **User input** — JSON with `client`, `project`, `hourly_rates` (rates for the six canonical roles) and optional `currency` (default `USD`).
3. **Parser** — finds the most recent file for that client+project, preferring the `.md` sidecar (robust to parse) and falling back to the `.pdf` if the Markdown is missing. Extracts hours by department, phases, and totals.
4. **Normalization** — maps Spanish names to commercial categories: `Arquitectura→Architecture`, `Diseño→Design`, `Discovery→Product Owner`. Backend and Frontend pass through. `Project Management` stays at 0h if the roadmap does not include it.
5. **Output** — Markdown + PDF written to `budgets/<client_slug>/<project_slug>-<timestamp>.{md,pdf}`, with executive summary, breakdown by role, project phases, and assumptions.

## Workflow

When the user asks you to quote a project:

1. **Verify the roadmap exists** — if the user has not generated it yet, tell them to run `sales-roadmap` first. This skill does not compute hours, only prices them.

2. **Collect the input** by asking the user for anything missing:
   - Client / lead name (`client`) — must match the one used when generating the roadmap
   - Project name (`project`) — idem
   - Hourly rates per role (`hourly_rates`): `backend`, `frontend`, `architecture`, `design`, `project_management`, `product_owner`
   - (Optional) `currency` — default `USD`

3. **Save the input** as `examples/<client-slug>-rates.json` (or reuse an existing one).

4. **Run**:
   ```bash
   cd .claude/skills/sales-pricing
   uv run --with pyyaml --with markdown-pdf python scripts/pricing.py examples/<file>.json
   ```
   This writes two files in `budgets/<client_slug>/<project_slug>-<timestamp>.{md,pdf}`.

5. **Present the result** to the user: show the total in the chosen currency, the path to the PDF, and the Markdown content of the budget (breakdown by role and phases).

## Roadmap selection

- Looks in `../sales-roadmap/roadmaps/<client_slug>/` for files matching `<project_slug>-*.md` (or `.pdf` as a fallback).
- When multiple files exist, uses the **most recent** by modification time.
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

Legacy Spanish keys (`cliente`, `proyecto`) are also accepted for backwards compatibility with existing `sales-roadmap` inputs.

## Maintenance

- **Add a new role**: add it to `scripts/parser.py` (`ROLE_MAP` and `CANONICAL_ROLES`) and to `scripts/render.py` (`RATE_KEY_BY_ROLE`).
- **Change default currency**: pass `currency` in the input (not hardcoded).
- **Add taxes / discounts / PM overhead**: extend `scripts/render.py::compute_budget` (out of MVP scope).

## Dependencies

- Python 3.10+
- `pyyaml` + `markdown-pdf` (bring in `pymupdf` for PDF parsing, installed on-demand via `uv run --with`)

## Implicit assumptions

- Roadmap hours are in the "Semi" scale (ideal hours before any seniority adjustment). The budget prices these directly at the role's hourly rate.
- Currency is homogeneous: all rates are in the same unit (`currency`).
- Budget validity: 30 days (editable in `render.py`).
- Excludes taxes, infrastructure, third-party licenses.
