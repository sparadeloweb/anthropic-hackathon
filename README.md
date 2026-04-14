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

## Prerequisites

| Tool | Version | Required for | Install |
|------|---------|-------------|---------|
| **Claude Code** | latest | Everything | `npm i -g @anthropic-ai/claude-code` |
| **Python** | 3.10+ | Sales pipeline scripts | [python.org](https://www.python.org/downloads/) |
| **uv** | latest | sales-roadmap, sales-pricing (runs deps on the fly) | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **Node.js** | 18+ | Dev skills (Next.js, Playwright) | [nodejs.org](https://nodejs.org/) |
| **GitHub CLI** | latest | dev-add-feature, dev-review-pr | `brew install gh` / `sudo apt install gh` / `winget install GitHub.cli` |
| **Git** | 2.x | Version control | Pre-installed on most systems |

## Setup

### 1. Clone and run the setup script

```bash
git clone https://github.com/sparadeloweb/anthropic-hackathon.git agencIA
cd agencIA
bash setup.sh
```

This creates a Python virtual environment, installs dependencies (`requests`, `python-dotenv`), and copies `.env.example` → `.env`.

### 2. Configure API keys

Edit `.env` with your keys:

```bash
# Google Places API — used by /sales-finding-leads
# Get yours at: https://console.cloud.google.com/apis/credentials
# Enable "Places API (New)" in APIs & Services > Library
GOOGLE_PLACES_API_KEY=your-api-key-here

# Google Stitch API — used by /design-generating-websites
# Get yours at: https://stitch.withgoogle.com (Settings > API Keys)
STITCH_API_KEY=your-api-key-here
```

### 3. Configure MCP servers

These MCP servers need to be registered in Claude Code:

**Stitch** (required for `/design-generating-websites`):

```bash
claude mcp add stitch \
  --transport http https://stitch.googleapis.com/mcp \
  --header "X-Goog-Api-Key: YOUR-STITCH-API-KEY" \
  -s user
```

**Notion** (optional — used by dev skills for documentation):

> Configured via Claude Code's built-in Notion integration at [claude.ai](https://claude.ai) under Settings > Integrations.

**Vercel** (optional — used by `/dev-deploy`):

```bash
claude mcp add vercel --transport http https://mcp.vercel.com -s user
```

**Gmail** (optional — future email delivery):

> Configured via Claude Code's built-in Gmail integration.

### 4. Authenticate GitHub CLI (for dev skills)

```bash
gh auth login
gh repo set-default OWNER/REPO
```

### 5. Verify everything

```bash
source venv/bin/activate
python3 -c "import requests, dotenv; print('Python deps OK')"
uv --version          # should print version
gh auth status        # should show logged in
claude --version      # should print version
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
