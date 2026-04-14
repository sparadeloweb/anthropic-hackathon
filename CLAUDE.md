# Agency AI — Multi-Agent Ecosystem for Digital Agencies

## What it is

A multi-agent platform that automates the full lead acquisition and proposal cycle for web/digital design agencies. Given a campaign configuration, the system finds local businesses via Google Maps, analyzes them, scores them, generates a redesigned website, and builds a commercial proposal ready to send — all in minutes.

**Context:** Built for the Anthropic/Claude hackathon (5 hours). The demo focus is the Campaign → Leads → Proposal flow.

---

## Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15 + TypeScript + Tailwind CSS |
| Backend | Laravel 11 (PHP) |
| AI | Anthropic Claude API (`claude-sonnet-4-6` / `claude-haiku-4-5-20251001`) |
| UI Generation | Google Stitch MCP |
| Scraping | Firecrawl API |
| Lead Discovery | Google Maps MCP |
| Real-time | Server-Sent Events (SSE) |
| Deploy | Vercel (frontend) + Railway/local (backend) |

---

## Repository Structure

```
/
├── frontend/          ← Next.js 15 app
│   ├── app/
│   │   ├── page.tsx                  ← Campaign settings form
│   │   ├── dashboard/                ← Leads board (ranked list)
│   │   ├── dashboard/[leadId]/       ← Active agent pipeline view
│   │   ├── client/[leadId]/          ← Client-facing proposal view
│   │   └── preview/[leadId]/         ← Generated site (iframe target)
│   └── components/
│       ├── AgentFeed.tsx             ← Real-time agent activity log
│       ├── QualificationCard.tsx     ← Human checkpoint: approve/discard lead
│       ├── SitePreview.tsx           ← iframe of generated site
│       └── ProposalPreview.tsx       ← Modal with commercial proposal
│
├── backend/           ← Laravel 11 API
│   └── app/
│       ├── Http/Controllers/
│       │   ├── LeadController.php          ← POST /api/leads
│       │   └── PipelineController.php      ← GET /api/pipeline/{id}/stream (SSE)
│       └── Services/
│           ├── ManagementAgent.php         ← Main orchestrator
│           ├── DiscoveryAgent.php          ← Google Maps MCP search
│           ├── ResearchAgent.php           ← Scraping + analysis
│           ├── QualificationAgent.php      ← Lead scoring
│           ├── DesignAgent.php             ← Stitch MCP + site generation
│           └── ProposalAgent.php           ← Commercial proposal
│
├── CLAUDE.md
├── DESIGN.md          ← Folio dashboard design system
└── STITCH-AGENT.md    ← Design Agent context for generating client sites
```

---

## Agent Architecture

```
╔══════════════════════════════════════╗
║  STEP 0: CAMPAIGN SETTINGS           ║  ← user configures once
║  • Target industry / niche           ║
║  • Geographic zone (city, radius)    ║
║  • Ideal business size               ║
║  • Budget signals                    ║
║  • Negative filters (enterprise,     ║
║    no web needed, franchise, etc.)   ║
║  • Auto-approval score threshold     ║
╚══════════════════╦═══════════════════╝
                   ↓
┌──────────────────────────────────────┐
│  DISCOVERY AGENT  (Haiku)            │
│  → Google Maps MCP                   │
│  Scans the zone with campaign filters│
│  Returns: name, address, phone,      │
│  rating, category, website URL       │
│  Output: list of candidates          │
└──────────────┬───────────────────────┘
               ↓
┌──────────────────────────────────────┐
│  MANAGEMENT AGENT  (Sonnet)          │
│  Orchestrates pipeline per candidate │
│  Handles errors, decides priority    │
└──────┬───────────────────────────────┘
       │  per candidate (parallel)
    ┌──▼─────────────────┐
    │  RESEARCH AGENT    │  claude-haiku-4-5
    │  Scrape current web│
    │  Social media      │
    │  Industry / niche  │
    │  → LeadProfile JSON│
    └──────┬─────────────┘
           ↓
    ┌──────────────────────┐
    │  QUALIFICATION AGENT │  claude-haiku-4-5
    │  Score 0-100         │
    │  Based on settings   │
    │  HOT / WARM / COLD   │
    └──────┬───────────────┘
           ↓
┌──────────────────────────────────────┐
│  LEADS BOARD  ★ HUMAN REVIEW ★       │
│  Ranked list: HOT → WARM → COLD      │
│  User selects which leads to process │
│  (or uses configured auto threshold) │
└──────┬───────────────────────────────┘
       │  per approved lead
    ┌──▼─────────────────────┐
    │  DESIGN AGENT          │  claude-sonnet-4-6 + Stitch MCP
    │  Generates design brief│
    │  Screenshots current   │
    │  Calls Stitch → HTML   │
    │  Serves at /preview/:id│
    └──────┬─────────────────┘
           ↓
    ┌──────────────────────┐
    │  PROPOSAL AGENT      │  claude-sonnet-4-6
    │  Business analysis   │
    │  Proposed solution   │
    │  Budget (3 tiers)    │
    │  ★ HUMAN CHECKPOINT ★│  ← user reviews before "sending"
    └──────┬───────────────┘
           ↓
    ┌──────────────────────┐
    │  DASHBOARD PREVIEW   │
    │  Site iframe         │
    │  Proposal preview    │
    │  Email preview       │
    └──────────────────────┘
```

---

## Agent Definitions

### Campaign Settings (not an agent — user config)
User defines before launching a search:
```json
{
  "targetIndustries": ["restaurants", "design studios", "dental clinics"],
  "location": { "city": "Buenos Aires", "radiusKm": 10 },
  "businessSize": ["micro", "small"],
  "budgetSignals": ["premium zone", "active advertising", "high reviews"],
  "negativeFilters": ["enterprise", "franchise", "no website needed"],
  "autoApproveThreshold": 65
}
```

### Discovery Agent — `claude-haiku-4-5-20251001`
- Uses **Google Maps MCP** to find businesses in the target zone
- Applies campaign filters to narrow candidates
- Output: candidate list with `{ name, address, phone, rating, category, websiteUrl }`
- Tools: `google_maps_search(query, location, radius)`, `filter_candidates(settings)`

### Management Agent — `claude-sonnet-4-6`
- Orchestrates the pipeline per candidate (can run in parallel)
- Handles errors and falls back if an agent fails
- Notifies the frontend via SSE at each step
- Tools: `run_research`, `run_qualification`, `run_design`, `run_proposal`, `notify_frontend`

### Research Agent — `claude-haiku-4-5-20251001`
- Scrapes current website (Firecrawl)
- Web search for business information
- Output: `LeadProfile { name, industry, description, currentSiteQuality, socialPresence, painPoints }`

### Qualification Agent — `claude-haiku-4-5-20251001`
- Evaluates the lead against the active campaign criteria
- Weighs: site quality, budget signals, business activity
- Output: `{ score: 0-100, verdict: "HOT_LEAD"|"WARM_LEAD"|"COLD_LEAD", reasons[], risks[] }`
- Auto-approves if `score >= settings.autoApproveThreshold`

### Design Agent — `claude-sonnet-4-6` + Stitch MCP
1. Claude generates a design brief (audience, style, sections, problem to solve)
2. Screenshots the current site via Firecrawl
3. Calls Stitch MCP with brief + screenshot as reference
4. Output: React/Tailwind → served at `/preview/[leadId]`
- **Fallback:** Claude generates HTML/CSS directly if Stitch fails
- See `STITCH-AGENT.md` for the full prompt template and industry style guide

### Proposal Agent — `claude-sonnet-4-6`
Generates an HTML proposal with sections:
- Current business analysis
- Identified problem + opportunity
- Proposed solution (link to site preview)
- Investment: Basic / Standard / Premium (with ranges)
- What's included + maintenance policy
- Next steps and CTA

---

## Environment Variables

### Backend (`backend/.env`)
```env
ANTHROPIC_API_KEY=sk-ant-...
FIRECRAWL_API_KEY=fc-...
FRONTEND_URL=http://localhost:3000
```

### Frontend (`frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Stitch MCP (configure before hackathon)
```bash
# 1. Google Cloud setup
gcloud beta services enable stitch.googleapis.com
gcloud auth application-default login

# 2. Add to Claude Code MCP config
npx @_davideast/stitch-mcp proxy
```

---

## How to Run

```bash
# Frontend
cd frontend
npm install
npm run dev          # http://localhost:3000

# Backend
cd backend
composer install
php artisan serve    # http://localhost:8000

# Tunnel for live demo
ngrok http 3000
```

---

## Human Decision Scale

| Decision | Type | Owner |
|----------|------|-------|
| Start lead analysis | Automatic | Agent |
| Score/qualify lead | Automatic | Agent |
| Approve lead for proposal | **Optional** | User (configures threshold) |
| Review generated site | Optional | User |
| Approve proposal before sending | **Required** | Always human |
| Send communication to lead | **Required** | Always human |
| Accept project + start development | **Required** | Always human |

Rule: *anything that builds client trust requires human approval.*

---

## Conventions

- Code in English
- Each agent is a Laravel Service with a `run(array $context): array` method
- The Management Agent is the only one that holds full pipeline state
- SSE events follow the shape: `{ agent, status, data, timestamp }`
- Haiku for fast/cheap tasks (research, qualification), Sonnet for complex synthesis (design, proposal)
- Never fabricate data: if scraping fails, the agent reports `data_unavailable` and Management decides whether to continue with partial data

---

## Demo Script (3 min)

1. Configure a campaign (industry: restaurants, zone: Palermo, Buenos Aires)
2. Watch Discovery Agent scan Google Maps → candidates appear
3. Research + Qualification runs → ranked lead list appears
4. Select a HOT lead → approve at checkpoint
5. Watch Design Agent + Stitch generate the site → iframe appears
6. Watch Proposal Agent → full proposal modal
7. Show "Email Preview" with links to site and proposal
8. Show full architecture slide → mention roadmap (conversation, development, QA)

**Pre-prepared demo leads (scrape before hackathon):**
- HOT lead: active business, poor website, receptive industry → full flow
- COLD lead: enterprise or inactive → shows discard path
- BACKUP lead: in case first fails live

---

## Known Risks

| Risk | Mitigation |
|------|-----------|
| Stitch MCP setup fails | Set up first thing. Fallback: Claude generates HTML directly |
| Scraping blocked | Firecrawl handles this. Fallback: pre-scraped data |
| Demo is slow | Pre-process demo leads. Present streaming as a feature |
| SSE too complex | Fallback: polling every 2 seconds |

---

## Post-Hackathon Roadmap

- [ ] Lead communication channel (email / WhatsApp)
- [ ] Lead conversation (answers questions, negotiates budget)
- [ ] Natural language rescoping → full project briefing
- [ ] Advanced Design Agent: internal component library
- [ ] Development Agent: generates custom site code
- [ ] QA Agent: review before delivery
- [ ] Client Dashboard: client sees project stages, leaves feedback
- [ ] Payment system: activates deliveries and project phases
