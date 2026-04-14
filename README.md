# agencIA

Automated lead acquisition and project management pipeline for digital agencies, built with Claude Code Skills.

## Pipeline

```
1. Lead acquisition             →  /sales-finding-leads
   (area + industry)

2. Scraping + Report            →  Output: leads/  (HTML + JSON)

3. Lead selection               →  Manual (from the report)

4. Design generation            →  /design-generating-websites
   (interactive preferences)

5. Asset download               →  Output: stitch_designs/  (screenshots + design system)

6. Estimation + Roadmap         →  /sales-roadmap

7. Roadmap output               →  Output: roadmaps/  (MD + PDF with Gantt)

8. Commercial budget            →  /sales-pricing

9. Business proposal            →  /sales-proposal

10. Presentation dashboard      →  /sales-proposal-web
    (single HTML with everything)

11. Email delivery              →  Gmail MCP (coming soon)
```

```
Lead Generation → Scraping → Data Structuring (HTML/JSON)
  → Lead Selection (manual)
    → Design Generation (Stitch) → Assets
      → Roadmap Generation → Budget
        → Business Proposal
          → Dashboard Web
            → Delivery (Email)
```

## Folder structure

```
agencIA/
├── leads/                    # Lead data (Google Places API)
├── stitch_designs/           # Web designs (Stitch)
├── roadmaps/                 # Development roadmaps (MD + PDF)
├── budgets/                  # Commercial budgets (MD + PDF)
├── proposals/                # Proposals + dashboards (TXT + HTML)
└── .claude/skills/           # Pipeline skills
    ├── sales-finding-leads/      # Step 1-2: find leads
    ├── design-generating-websites/ # Step 4-5: Stitch design
    ├── sales-roadmap/            # Step 6-7: estimation
    ├── sales-pricing/            # Step 8: budget
    ├── sales-proposal/           # Step 9: proposal
    ├── sales-proposal-web/       # Step 10: dashboard
    ├── agency-demo/              # End-to-end demo
    ├── dev-from-design-to-code/  # Dev: design → code
    ├── dev-deploy/               # Dev: deployment
    ├── dev-add-feature/          # Dev: features/bugs
    ├── dev-review-pr/            # Dev: code review
    ├── dev-tunnels/              # Dev: tunnels
    └── creating-skills/          # Meta: create skills
```

## Setup

```bash
bash setup.sh
```

Then edit `.env` and add your API keys:

```bash
GOOGLE_PLACES_API_KEY=your-actual-key-here
```

## Skills — Sales Pipeline

### `/sales-finding-leads`

Finds business leads by industry and geographic area using Google Places API with grid-based search (5x5). Filters for businesses without a website. Generates interactive HTML report + JSON.

**Output:** `leads/YYYY-MM-DD/query-slug/{leads_data.json, leads_report.html}`

### `/design-generating-websites`

Generates a professional website design in Google Stitch for one lead. Asks for preferences (colors, typography, style), downloads screenshots.

**Output:** `stitch_designs/lead-slug/{stitch_project.json, screens/*.png, design-system/}`

### `/sales-roadmap`

Estimates development timelines by cross-referencing requirements against the real team roster. Two modes: new project from Stitch design or new feature for an existing project.

**Output:** `roadmaps/lead-slug/{project.md, project.pdf}`

### `/sales-pricing`

Takes a roadmap and applies per-role hourly rates to generate a commercial budget with investment breakdown.

**Output:** `budgets/lead-slug/{project.md, project.pdf}`

### `/sales-proposal`

Generates a professional business proposal combining lead data, design, and roadmap. Auto-detects language from the lead's country.

**Output:** `proposals/lead-slug/proposal.txt`

### `/sales-proposal-web`

Self-contained HTML dashboard with 5 tabs: business info, design, proposal, budget, roadmap. Images embedded in base64, automatic i18n.

**Output:** `proposals/lead-slug/dashboard.html`

### `/agency-demo`

Runs the complete pipeline end-to-end as a demo. Picks a random industry and country, finds leads, designs, estimates, budgets, proposes, and generates the dashboard.

## Skills — Development

### `/dev-from-design-to-code`

Converts Stitch designs into production code: Next.js frontend + optional Laravel API backend. Tests with Playwright + Pest, documentation in Notion.

### `/dev-deploy`

Deploys to Vercel (frontend) and/or Laravel Cloud (backend). Pre-checks, deploy, verification, documentation.

### `/dev-add-feature`

Adds features or fixes bugs. Conventional branch naming, PRs via `gh`, tests, documentation.

### `/dev-review-pr`

Reviews PRs against React and Laravel checklists. Posts inline comments via `gh api`.

### `/dev-tunnels`

Public tunnels for local dev. Cloudflare (free), Vercel Dev, ngrok, localtunnel.

## Skills — Meta

### `/creating-skills`

Creates new skills following official best practices. Templates, quality checklist, frontmatter reference.
