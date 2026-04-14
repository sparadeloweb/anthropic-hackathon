# anthropic-hackathon

## Setup

```bash
bash setup.sh
```

This will:
1. Check for Python 3 (install it if missing via apt/brew)
2. Create a virtual environment (`venv/`)
3. Install dependencies from `requirements.txt`
4. Create `.env` from `.env.example` if it doesn't exist

Then edit `.env` and add your API keys:

```bash
GOOGLE_PLACES_API_KEY=your-actual-key-here
```

## Skills

This project uses [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) to extend Claude Code capabilities.

### `/creating-skills`

Base skill for creating new skills following the [official best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

**Usage:**

```
/creating-skills skill-name "description of what it does"
```

Includes:
- Step-by-step guided workflow with progress checklist
- Ready-to-use templates for different skill types (minimal, subagent, user-only, background knowledge, dynamic context)
- Quality validation checklist
- Complete frontmatter field reference

**Structure:**
```
.claude/skills/creating-skills/
├── SKILL.md                  # Main instructions
├── TEMPLATE.md               # Reusable templates
├── CHECKLIST.md              # Quality checklist
└── FRONTMATTER-REFERENCE.md  # Frontmatter reference
```

### `/sales-finding-leads`

Finds business leads using Google Places API (New) with deep grid-based search that goes beyond the default 60-result API limit by subdividing the geographic area into a grid.

**Features:**
- Grid-based search (5x5 = 25 cells by default) to maximize results
- Filter option: all results or only businesses without a website
- Deduplication by place ID across grid cells
- Full data: photos, reviews, opening hours, editorial summaries, payment options
- Interactive HTML report (shadcn-style): compact table with click-to-detail view (photos, reviews, hours), search, sort, filter, and CSV export
- Organized output: `./leads/YYYY-MM-DD/query-slug/`
- Raw JSON output for AI analysis or further processing

**Usage:**
```
/sales-finding-leads
```

Claude will ask for search query, filter preference, and search depth before running.

**Structure:**
```
.claude/skills/sales-finding-leads/
├── SKILL.md                  # Main instructions
├── SETUP.md                  # Google Places API key setup
├── scripts/
│   └── find_leads.py         # Search and report generation script
└── templates/
    └── report_template.html  # HTML report template
```

**Requires:** `GOOGLE_PLACES_API_KEY` environment variable. See `SETUP.md` for details.

### `/design-generating-websites`

Generates a website design in [Google Stitch](https://stitch.withgoogle.com) for **one lead at a time**. Asks design preferences interactively before generating, downloads screenshots locally.

**Features:**
- One lead per run (invoke again for another lead)
- Interactive preferences before generation: project type, platform, colors, color mode, style tone, custom requests
- Project types: **Single Page** (landing), **Multi Page** (website with nav), or **App** (mobile screens)
- Platforms: Desktop, Mobile-first, App (iOS/Android)
- Analyzes photos, reviews, hours, and business type to suggest palette and typography
- Downloads all screenshots to `./stitch_designs/lead-name-slug/`
- Follows premium UI/UX principles from [ui-ux-pro-max](https://skills.sh/kimny1143/claude-code-template/ui-ux-pro-max) and [frontend-design](https://skills.sh/anthropics/skills/frontend-design)

**Usage:**
```
/design-generating-websites
```

**Structure:**
```
.claude/skills/design-generating-websites/
├── SKILL.md                  # Main instructions
├── SETUP-STITCH.md           # Stitch MCP configuration
├── DESIGN-PRINCIPLES.md      # UI/UX design guidelines
└── SCREEN-PROMPTS.md         # Prompt templates per screen type
```

**Requires:** Stitch MCP configured with API key. See `SETUP-STITCH.md` for details.

### `/sales-roadmap`

Estimates project timelines and builds Gantt-style roadmaps for product development. Cross-references requirements against the real team roster and current allocations to produce a schedule with named person assignments.

**Features:**
- Two modes: **New project** (from an existing Stitch design) or **New feature** (for an existing project/client)
- Auto-detects Stitch designs and maps screens to the page catalog
- Phase sequencing: Discovery → Design → Architecture → Backend + Frontend (parallel)
- Seniority-aware scheduling (Junior x1.5, Semi x1.0, Senior x0.7)
- Automatic start date shift if team capacity is insufficient
- Argentine holidays 2026-2028 built in
- Generates both Markdown (with Mermaid Gantt) and PDF outputs
- Feature-mode outputs use the feature name as filename prefix

**Usage:**
```
/sales-roadmap
```

Claude will ask whether you want to estimate a new project or add a feature to an existing one.

**Structure:**
```
.claude/skills/sales-roadmap/
├── SKILL.md                  # Main instructions
├── data/
│   ├── atomic-tasks.yaml     # Base hours per atomic task
│   ├── pages.yaml            # Page catalog
│   ├── features.yaml         # Feature catalog
│   ├── integrations.yaml     # Integration catalog
│   ├── dependencies.yaml     # Phase dependency graph
│   ├── multipliers.yaml      # Difficulty & seniority multipliers
│   ├── config.yaml           # Working hours config
│   └── holidays-ar.yaml      # Argentine holidays
├── roster/
│   ├── employees.yaml        # Team members
│   └── allocations.yaml      # Current project allocations
├── scripts/
│   ├── estimate.py           # Entry point
│   ├── catalog.py            # Catalog loader & validator
│   ├── scheduler.py          # Task expansion & scheduling engine
│   ├── render.py             # Markdown/Gantt renderer
│   └── roster.py             # Roster & availability calculator
└── examples/                 # Input JSON files
# Output goes to <repo_root>/roadmaps/<client_slug>/ (same pattern as stitch_designs/)
```

**Requires:** Python 3.10+, `uv` (dependencies installed on-demand).

### `/sales-proposal`

Generates a professional sales proposal for a lead by combining Stitch design, roadmap, and business data. Produces a ready-to-send message tailored to the client's business type and language.

**Features:**
- Combines three data sources: Stitch design, roadmap estimate, and lead business data
- Auto-detects language from lead location (Spanish, English, Portuguese), asks for confirmation
- Professional but approachable tone — sells results, not technology
- Includes: business-specific opening, design overview, execution timeline, call to action
- Excludes: prices, internal team names, technical jargon, hour breakdowns
- Output follows same folder pattern as `stitch_designs/` and `roadmaps/`

**Usage:**
```
/sales-proposal
```

Claude will list leads that have both a Stitch design and a roadmap, ask which one, confirm language, and generate the proposal.

**Structure:**
```
.claude/skills/sales-proposal/
└── SKILL.md              # Main workflow (7 steps)
# Output goes to <repo_root>/proposals/<lead_slug>/propuesta.txt
```

### `/sales-proposal-web`

Generates a self-contained HTML dashboard that consolidates all pipeline outputs for a lead into a single interactive presentation with tabs: business info, Stitch design, proposal, budget, and roadmap.

**Features:**
- Combines 5 data sources: Google Places lead, Stitch design, roadmap, budget, proposal
- Auto-detects language from lead country (Spanish, English, Portuguese)
- Dark modern dashboard with tabbed navigation
- Stitch screenshots embedded in base64 (fully self-contained, shareable)
- Single HTML file — no dependencies, opens in any browser
- Prerequisite checker: shows which pipeline steps are missing

**Usage:**
```
/sales-proposal-web
```

Claude will list leads that have all prerequisites, generate the dashboard, and output the file path.

**Structure:**
```
.claude/skills/sales-proposal-web/
├── SKILL.md                          # Main workflow
└── scripts/
    └── build_dashboard.py            # Dashboard generator
# Output goes to <repo_root>/proposals/<lead_slug>/dashboard.html
```

**Requires:** Python 3.10+. All pipeline steps must be completed for the lead first.

### `/sales-pricing`

Generates client-ready commercial budgets from roadmaps. Reads a roadmap, extracts hours by role, applies per-role hourly rates, and produces a budget with total investment breakdown.

**Features:**
- Reads roadmaps from `/sales-roadmap` automatically
- Maps Spanish role names to canonical commercial roles (Backend, Frontend, Architecture, Design, PM, PO)
- Supports project-mode and feature-mode roadmaps
- Outputs Markdown + PDF with consistent styling

**Usage:**
```
/sales-pricing
```

**Structure:**
```
.claude/skills/sales-pricing/
├── SKILL.md                  # Main workflow
├── scripts/
│   ├── pricing.py            # Entry point
│   ├── parser.py             # Roadmap parser
│   └── render.py             # Budget renderer
└── examples/
    └── sample-rates.json     # Example input
# Output goes to <repo_root>/budgets/<client_slug>/
```

### `/agency-demo`

Runs the complete agencIA pipeline end-to-end as a demonstration. Picks a random industry and country, searches for leads, generates design, roadmap, budget, proposal, and dashboard. Creates `CLAUDE.md` with full pipeline documentation on success.

**Usage:**
```
/agency-demo
```

**Pipeline executed:**
```
Lead Search → Design (Stitch) → Roadmap → Budget → Proposal → Dashboard Web
```

### `/dev-from-design-to-code`

Converts Stitch designs into production code: Next.js (React) frontend with optional Laravel API backend. Asks if backend is needed, scaffolds the project, splits designs into minimum components, writes Playwright + Pest tests, installs all dependencies, starts dev server with optional public tunnel, and documents everything in Notion.

**Features:**
- Asks if backend (Laravel API) is needed before scaffolding
- Reads Stitch screen HTML and splits into atomic components (`ui/`), composed blocks, and layout elements
- Server Components by default — `'use client'` only when needed
- Follows all 70 rules from [vercel-react-best-practices](https://github.com/vercel-labs/agent-skills) (waterfalls, bundle, server-side, re-renders)
- Follows [next-best-practices](https://github.com/vercel-labs/next-skills) (App Router, RSC, data patterns, image/font optimization)
- Laravel backend follows [laravel-specialist](https://github.com/jeffallan/claude-skills) (Eloquent, API Resources, Pest tests, >85% coverage)
- Playwright E2E tests for frontend, Pest feature tests for backend
- Starts dev server in background and offers public tunnel (Cloudflare/Vercel)
- Generates project documentation in Notion via MCP

**Usage:**
```
/dev-from-design-to-code
```

**Structure:**
```
.claude/skills/dev-from-design-to-code/
├── SKILL.md              # Main workflow (8 steps)
├── REACT-RULES.md        # 70 rules from Vercel (8 categories)
├── NEXTJS-RULES.md       # App Router, RSC, data patterns, image/font
└── LARAVEL-RULES.md      # Full laravel-specialist (templates, checkpoints, MCP)
```

**Requires:** Node.js 18+, Stitch MCP, Notion MCP. Laravel: PHP 8.2+, Composer.

### `/dev-deploy`

Deploys frontend to Vercel and/or backend to Laravel Cloud. Runs pre-deploy checks, deploys via MCP or CLI, verifies production, and generates deployment documentation in Notion if missing.

**Features:**
- Auto-detects project type (Next.js, Laravel, or both)
- Pre-deploy checks: build, lint, Playwright tests, Pest tests
- Frontend: deploys via Vercel MCP (OAuth) or Vercel CLI
- Backend: deploys via Laravel Cloud CLI or manual SSH
- Sets environment variables on deployment target
- Verifies production URL loads and critical flows work
- Generates/updates deployment guide in Notion with URLs, env vars, rollback steps

**Usage:**
```
/dev-deploy
```

**Structure:**
```
.claude/skills/dev-deploy/
├── SKILL.md              # Main workflow (6 steps)
└── SETUP-DEPLOY.md       # Vercel MCP, Vercel CLI, Laravel Cloud setup
```

**Requires:** Vercel MCP or CLI. Laravel Cloud CLI for backend. Notion MCP for docs.

### `/dev-add-feature`

Adds features or fixes bugs in existing code. Creates proper git workflow with branches, commits, and PRs via GitHub CLI. Updates Notion documentation.

**Features:**
- Verifies `gh` CLI is installed and authenticated — guides setup if not
- Asks: feature type (new feature, bug fix, refactor, perf), description, acceptance criteria
- Creates branch with conventional naming (`feat/`, `fix/`, `refactor/`, `perf/`)
- Implements changes following project patterns (React rules, Laravel rules)
- Runs full test suite before committing
- Creates PR via `gh pr create` with summary, test plan, and Co-Authored-By
- Updates Notion documentation if behavior changed

**Usage:**
```
/dev-add-feature
```

**Structure:**
```
.claude/skills/dev-add-feature/
├── SKILL.md              # Main workflow (6 steps)
└── SETUP-GITHUB.md       # GitHub CLI install, auth, verify
```

**Requires:** `gh` CLI installed and authenticated. Git remote configured.

### `/dev-review-pr`

Reviews pull requests for code quality, performance, security, and best practices. Posts review comments directly on GitHub via `gh` CLI.

**Features:**
- Loads full PR context: diff, changed files, comments, description
- Reads every changed file in full context (not just the diff)
- Checks React/Next.js files against [REACT-CHECKLIST.md](REACT-CHECKLIST.md) (performance, architecture, data fetching, security, a11y, testing)
- Checks Laravel files against [LARAVEL-CHECKLIST.md](LARAVEL-CHECKLIST.md) (security, architecture, database, code quality, testing)
- Severity levels: must fix, should fix, suggestion, nitpick
- Posts inline comments on specific lines via `gh api`
- Approves or requests changes with structured review body

**Usage:**
```
/dev-review-pr 123
```

**Structure:**
```
.claude/skills/dev-review-pr/
├── SKILL.md              # Main workflow (4 steps)
├── REACT-CHECKLIST.md    # React/Next.js review checklist
├── LARAVEL-CHECKLIST.md  # Laravel review checklist
└── SETUP-GITHUB.md       # GitHub CLI setup
```

**Requires:** `gh` CLI installed and authenticated. Access to the repository.

### `/dev-tunnels`

Manages public tunnels for local development servers. Creates, lists, and closes tunnels.

**Features:**
- Lists all active tunnels (Cloudflare, Vercel Dev, ngrok, localtunnel)
- Creates new tunnels on any port with provider choice
- Cloudflare recommended (free, no account needed, works via npx)
- Closes tunnels by PID, port, or all at once
- Cleans up tunnel log files

**Usage:**
```
/dev-tunnels
```

**Structure:**
```
.claude/skills/dev-tunnels/
└── SKILL.md              # Commands: list, create, close
```
