---
name: sales-roadmap
model: sonnet
description: Estimates project timelines and builds Gantt-style roadmaps for product development. Use when the user asks to estimate a project, build a roadmap for a client, calculate how long a build takes based on pages/features/integrations, or plan team allocation. Cross-references requirements against the real team roster and current allocations to produce a Gantt schedule with named person assignments.
---

# Product roadmap estimator

This skill produces a Gantt-style development roadmap with dates, named assignments, and a schedule respecting phase dependencies (Discovery → Design → Architecture → Backend+Frontend in parallel).

## When to use

- "Build me a roadmap for this project"
- "How long will this take?"
- "Let's estimate this project for the client"
- "When can we start given the team we have?"
- "Add a feature to this client's roadmap"

## How it works

1. **Source of truth** — base hours are in `data/` (atomic-tasks, pages, features, integrations) and the team is in `roster/` (employees, allocations).
2. **User input** — JSON with pages, features, integrations (with difficulty `low`/`medium`/`high` and quantity) and `desired_start_date`.
3. **Scheduler** — expands elements to atomic tasks, assigns people based on real availability, shifts the start date if the team is saturated.
4. **Output** — Markdown with summary, hours by department, named assignments, Mermaid Gantt, and task details. Saved to `<repo_root>/roadmaps/<client_slug>/` (same convention as `stitch_designs/`).

## Workflow

When the user invokes this skill, **always start by asking the mode**:

> Do you want to create a **roadmap for a new project** (from an existing Stitch design) or add a **new feature to an existing project**?

---

### Mode A — New project (from Stitch)

Use when estimating a complete project for the first time, typically from an existing Stitch design.

1. **Detect available designs** — list folders inside `<repo_root>/stitch_designs/` and show the user the available leads (read the `leadName` field from each `stitch_project.json`).

2. **User picks a lead** — with the selected `stitch_project.json`, extract:
   - `leadName` → `client` field in the input
   - Folder name from `stitch_designs/` → `client_slug` field in the input (so the `roadmaps/` folder matches exactly)
   - `screens[]` → map **each screen from the design** to a `page.*` from the catalog (`data/pages.yaml`). The roadmap must reflect **only** what exists in the Stitch design — do not add pages, features, or integrations that are not in the mockup. Use this mapping guide:
     - home / landing → `page.landing`
     - login → `page.login`
     - register → `page.register`
     - dashboard → `page.dashboard_simple` or `page.dashboard_advanced`
     - list / listing → `page.list_view`
     - detail → `page.detail_view`
     - profile → `page.profile`
     - settings → `page.settings`
     - contact → `page.landing` (simple variant)
     - about → `page.landing` (simple variant)
     - services → `page.list_view` (variant)
     - reviews / testimonials → `page.detail_view` (variant)
   - If a screen doesn't match any `page.*`, ask the user.

3. **Show the mapping and confirm** with the user before proceeding:
   - Present the table of design screens → catalog pages
   - Ask for project name (`project` field)
   - Ask for desired start date (`YYYY-MM-DD` format)
   - Confirm/adjust difficulty for each page
   - **Only if the user asks**, add features (`data/features.yaml`) or integrations (`data/integrations.yaml`) beyond what's in the design
   - (Optional) `employee_ids` to restrict the team

4. **Save the input** as `examples/<project-slug>.json`.

5. **Run**:
   ```bash
   cd .claude/skills/sales-roadmap
   uv run --with pyyaml --with markdown-pdf python scripts/estimate.py examples/<file>.json
   ```
   Generates: `roadmaps/<client_slug>/<project_slug>.{md,pdf}`.

6. **Show the result** to the user: provide the PDF path and paste the Markdown content (with Mermaid Gantt).

7. **Review assumptions** — flag any date shift, warnings, total hours by department.

---

### Mode B — New feature for existing project

Use when the client already has an estimated project and wants to add new functionality. Generates a separate roadmap focused on just the feature, filed in the same client folder.

1. **Identify the lead/client** — list existing folders in `roadmaps/` and/or `stitch_designs/` for the user to pick. If the user already mentioned one, use that. Use the existing folder name as the `client_slug` field to keep the same folder.

2. **Collect feature data** by talking to the user:
   - Feature name (`feature` field) — defines the output file prefix
   - Original project name (`project` field) — shown in the title
   - Desired start date (`YYYY-MM-DD` format)
   - New pages the feature requires (`data/pages.yaml`)
   - Catalog features that apply (`data/features.yaml`)
   - New integrations required (`data/integrations.yaml`)
   - Difficulty and quantity for each element
   - (Optional) `employee_ids` to restrict the team

3. **Save the input** as `examples/<client-slug>-<feature-slug>.json`. The JSON must include the `feature` field:
   ```json
   {
     "client": "Client name",
     "client_slug": "existing-folder-name",
     "project": "Original project name",
     "feature": "New feature name",
     "desired_start_date": "YYYY-MM-DD",
     "pages": [...],
     "features": [...],
     "integrations": [...]
   }
   ```

4. **Run** same as Mode A:
   ```bash
   cd .claude/skills/sales-roadmap
   uv run --with pyyaml --with markdown-pdf python scripts/estimate.py examples/<file>.json
   ```
   Generates: `roadmaps/<client_slug>/<feature_slug>.{md,pdf}` (note: uses the feature name as prefix, not the project name).

5. **Show the result** to the user and review assumptions.

---

### Notes common to both modes

- Valid IDs are in:
  - `data/pages.yaml` (e.g., `page.login`, `page.dashboard_simple`)
  - `data/features.yaml` (e.g., `feature.notifications`, `feature.roles_permissions`)
  - `data/integrations.yaml` (e.g., `integration.stripe`, `integration.sendgrid`)
- If the user mentions something not in the catalog, **ask** if you should add it to the YAMLs before continuing.

## Maintenance

- **New employee**: add in `roster/employees.yaml`.
- **Employee allocated to a project**: add in `roster/allocations.yaml`.
- **New recurring integration/feature/page**: add in the corresponding `data/` catalog.
- **Calibrate base times**: edit `base_hours` in `data/atomic-tasks.yaml` based on real project learnings.
- **Update holidays**: at year end, extend `data/holidays-ar.yaml`.

## Validation

Before running with new input, verify:
```bash
python scripts/catalog.py --validate
python scripts/roster.py --validate
```

## Dependencies

- Python 3.10+
- `pyyaml` + `markdown-pdf` (installed on-demand with `uv run --with`)

## Difficulty scale

| Level | Multiplier | When to use |
|---|---|---|
| low | x1.0 | Standard case, no surprises |
| medium | x1.8 | Custom validations, moderate logic, non-trivial UX |
| high | x3.0 | Complex state, realtime, compliance, many business rules |

## Implicit assumptions

- 5 working days/week, 8h/day, 6h productive (75%).
- Argentine holidays 2026-2028 loaded.
- Seniority: Junior x1.5, Semi x1.0, Senior x0.7 on base hours.
- Sequential phases: Discovery → Design → Architecture → (Backend || Frontend). QA not in MVP.
