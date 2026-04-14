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

### `/dev-from-design-to-code`

Converts Stitch designs into production code: Next.js (React) frontend with optional Laravel API backend. Asks if backend is needed, scaffolds the project, splits designs into minimum components, writes Playwright + Pest tests, installs all dependencies, and documents everything in Notion.

**Includes:** REACT-RULES.md, NEXTJS-RULES.md, LARAVEL-RULES.md

### `/dev-deploy`

Deploys frontend to Vercel and/or backend to Laravel Cloud. Runs pre-deploy checks (build, lint, tests), deploys via MCP or CLI, verifies production, and generates deployment documentation in Notion if missing.

### `/dev-add-feature`

Adds features or fixes bugs in existing code. Verifies GitHub CLI setup, creates branches with conventional naming, implements changes following project patterns, runs tests, creates PRs via `gh`, and updates Notion documentation.

### `/dev-review-pr`

Reviews pull requests for code quality, performance, security, and best practices. Reads the full diff, checks against React and Laravel checklists, and posts review comments directly on GitHub via `gh` CLI.

**Includes:** REACT-CHECKLIST.md, LARAVEL-CHECKLIST.md
