---
name: agency-demo
model: opus
description: Runs the complete agencIA pipeline end-to-end as a demo. Picks a random industry and country, finds leads, generates design, roadmap, budget, proposal, and dashboard. Creates CLAUDE.md with full pipeline documentation on success. Use to demonstrate the full agency workflow.
---

# Full agencIA pipeline demo

This skill runs the entire sales pipeline from start to finish as a demonstration, picking a random industry and country.

## When to use

- "Run a demo of the full pipeline"
- "Test the entire agency flow"
- `/agency-demo`

## Full pipeline

```
1. Lead Generation ──→ 2. Scraping ──→ 3. Report (HTML/JSON)
         │
         ▼
4. Lead Selection (manual) ──→ 5. Design (Stitch) ──→ 6. Assets
         │
         ▼
7. Roadmap ──→ 8. Budget ──→ 9. Proposal ──→ 10. Dashboard Web
```

## Workflow

### Step 0 — Pick random industry and country

Pick one at random from each list:

**Countries** (Americas and Europe, Latin alphabet only):
- Argentina, Mexico, Colombia, Chile, Uruguay, Spain, Portugal, France, Italy, Germany, Netherlands, Sweden, Norway, Denmark, Finland, Poland, Czech Republic, Romania, Hungary, Croatia, Brazil, Peru, Ecuador, Costa Rica, Panama

**Industries**:
- Dentists, Veterinary clinics, Architecture studios, Real estate agencies, Gyms, Restaurants, Hair salons, Yoga studios, Auto repair shops, Florists, Physiotherapy clinics, Photography studios, Language schools, Law firms, Opticians, Specialty coffee shops, Bicycle shops, Bookstores, Tattoo studios, Artisan bakeries

Show the user: "Demo: searching for **[industry]** in **[city], [country]**"

Use a major city from the chosen country (capital or large city).

### Step 1 — Find leads

Run `/sales-finding-leads` with:
- Query: the chosen industry + "in" + city, country
- Filter: without website only (to find leads we can offer services to)
- Depth: quick (1x1, to save API calls)

### Step 2 — Pick a lead

From the results, pick the first lead that:
- Has at least 10 reviews
- Has rating >= 4.0
- Does not have a website

If none match, pick the first available.

Show the user: "Selected lead: **[name]** (★[rating], [reviews] reviews)"

### Step 3 — Generate Stitch design

Run `/design-generating-websites` for the selected lead.

**IMPORTANT**: This step is interactive — the design skill will ask the user for their preferences (project type, colors, style, etc). Wait for responses before continuing.

### Step 4 — Generate roadmap

Run `/sales-roadmap` in Mode A (new project from Stitch):
- Use the freshly generated design
- Map screens automatically
- Start date: next working Monday
- Confirm with the user before running

### Step 5 — Generate budget

Run `/sales-pricing`:
- Use the freshly generated roadmap
- Default rates in USD:
  - Backend: $55/h
  - Frontend: $50/h
  - Architecture: $70/h
  - Design: $45/h
  - Project Management: $50/h
  - Product Owner: $60/h

### Step 6 — Generate business proposal

Run `/sales-proposal`:
- Use the selected lead
- Language: auto-detect from the lead's country

### Step 7 — Generate web dashboard

Run the `/sales-proposal-web` script:
```bash
cd .claude/skills/sales-proposal-web
python scripts/build_dashboard.py <lead-slug>
```

### Step 8 — Create CLAUDE.md

If the entire pipeline completed successfully, create a `CLAUDE.md` file at the project root with the complete agencIA workflow documentation. See the template in the CLAUDE.md section below.

### Step 9 — Show summary

Show the user a summary of everything generated:

```
Pipeline complete for: [lead name]
   Country: [country] | Industry: [industry]

   leads/...                  → [N] leads found
   stitch_designs/[slug]/     → [N] screens designed
   roadmaps/[slug]/           → [duration] working days
   budgets/[slug]/            → [total] [currency]
   proposals/[slug]/proposal  → language: [language]
   proposals/[slug]/dashboard → dashboard.html
   CLAUDE.md                  → pipeline documentation
```
