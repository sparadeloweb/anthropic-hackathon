# agencIA — Automated lead acquisition and project management pipeline

## What is this

agencIA is an automated lead acquisition and qualification pipeline for digital agencies, built as a set of Claude Code skills that run sequentially. It transforms a geographic business search into a complete commercial proposal with web design, development roadmap, budget, and presentation dashboard.

## Pipeline

```
Lead Generation → Scraping → Data Structuring (HTML/JSON)
  → Lead Selection (manual)
    → Design Generation (Stitch) → Assets
      → Roadmap Generation → Budget
        → Business Proposal
          → Dashboard Web
            → Delivery (Email)
```

### 1. `/sales-finding-leads` — Lead acquisition
Finds businesses by industry and geographic area using Google Places API with grid-based search to exceed the 60-result API limit. Generates an interactive HTML report and a JSON with all data.
- **Input**: industry + geographic area
- **Output**: `leads/YYYY-MM-DD/query-slug/{leads_data.json, leads_report.html}`

### 2. `/design-generating-websites` — Web design
Generates a professional website design in Google Stitch for a selected lead. Asks for design preferences (colors, typography, style) and downloads screenshots.
- **Input**: selected lead + design preferences
- **Output**: `stitch_designs/lead-slug/{stitch_project.json, screens/*.png, design-system/}`

### 3. `/sales-roadmap` — Estimation and roadmap
Estimates development timelines by cross-referencing requirements against the real team roster. Generates a Gantt schedule with named person assignments.
- **Input**: screens from Stitch design + start date
- **Output**: `roadmaps/lead-slug/{project.md, project.pdf}`

### 4. `/sales-pricing` — Budget
Takes the roadmap and applies per-role hourly rates to generate a commercial budget.
- **Input**: roadmap + per-role rates
- **Output**: `budgets/lead-slug/{project.md, project.pdf}`

### 5. `/sales-proposal` — Business proposal
Generates a professional business proposal message combining lead data, design, and roadmap. Auto-detects language from the lead's country.
- **Input**: lead + design + roadmap
- **Output**: `proposals/lead-slug/proposal.txt`

### 6. `/sales-proposal-web` — Presentation dashboard
Consolidates the entire pipeline into an interactive HTML dashboard with tabs: business, design, proposal, budget, and roadmap. Self-contained (base64 images).
- **Input**: all previous outputs
- **Output**: `proposals/lead-slug/dashboard.html`

## Development skills

### `/dev-from-design-to-code`
Converts Stitch designs into production code (Next.js frontend + optional Laravel API backend). Includes tests, documentation in Notion.

### `/dev-deploy`
Deploys to Vercel (frontend) and/or Laravel Cloud (backend). Pre-checks, deploy, verification, documentation.

### `/dev-add-feature`
Adds features or fixes bugs with proper git workflow. Branches, PRs via `gh`, tests.

### `/dev-review-pr`
Reviews pull requests against React and Laravel checklists. Posts inline comments on GitHub.

### `/dev-tunnels`
Manages public tunnels for local dev servers (Cloudflare, ngrok, etc).

## Folder structure

```
agencIA/
├── leads/                    # Lead data (Google Places API)
├── stitch_designs/           # Web designs (Stitch)
├── roadmaps/                 # Development roadmaps (MD + PDF)
├── budgets/                  # Commercial budgets (MD + PDF)
├── proposals/                # Proposals + dashboards (TXT + HTML)
└── .claude/skills/           # Pipeline skills
    ├── sales-finding-leads/
    ├── design-generating-websites/
    ├── sales-roadmap/
    ├── sales-pricing/
    ├── sales-proposal/
    ├── sales-proposal-web/
    ├── agency-demo/
    ├── dev-from-design-to-code/
    ├── dev-deploy/
    ├── dev-add-feature/
    ├── dev-review-pr/
    ├── dev-tunnels/
    └── creating-skills/
```

## How to run the full pipeline

1. `/sales-finding-leads` — find leads
2. Pick a lead from the HTML report
3. `/design-generating-websites` — design the website
4. `/sales-roadmap` — estimate timelines
5. `/sales-pricing` — generate budget
6. `/sales-proposal` — write proposal
7. `/sales-proposal-web` — generate dashboard
8. Send to client

Or run `/agency-demo` for an end-to-end demonstration with a random industry and country.
