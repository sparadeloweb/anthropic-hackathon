---
name: design-generating-websites
description: Generates a website design in Stitch for ONE scraped lead. Asks design preferences before generating. Use when the user wants to design a website, generate a mockup, or create web presence for a lead.
model: opus
allowed-tools: Bash(python *) Bash(curl *) Bash(mkdir *) Read Write Glob Grep mcp__stitch__*
---

# Generate Website Design for a Lead

Creates ONE Stitch project for ONE lead. Never batch-process multiple leads in a single run. If the user wants to design for multiple leads, they must invoke this skill once per lead.

## Prerequisites

- Stitch MCP configured. See [SETUP-STITCH.md](SETUP-STITCH.md).
- Leads data in `./leads/` (from `/sales-finding-leads`).

## Workflow

```
Design Progress:
- [ ] Step 1: Select ONE lead
- [ ] Step 2: Ask design preferences
- [ ] Step 3: Analyze lead data
- [ ] Step 4: Create Stitch project + design system
- [ ] Step 5: Generate screens
- [ ] Step 6: Download screenshots to stitch_designs/
```

### Step 1: Select ONE lead

List available leads and let the user pick ONE:

```bash
python3 -c "
import json, sys, glob
files = sorted(glob.glob('leads/*/*/leads_data.json'))
if not files:
    print('No leads found. Run /sales-finding-leads first.')
    sys.exit(1)
for f in files:
    print(f'\n--- {f} ---')
    data = json.load(open(f))
    for i, l in enumerate(data):
        web = 'NO WEB' if not l.get('websiteUri') else 'has web'
        print(f'  {i}: {l[\"displayName\"][\"text\"]} | {web} | rating: {l.get(\"rating\",\"-\")}')
"
```

The user picks ONE lead by index. Load that lead's full data.

### Step 2: Ask design preferences

Before generating anything, ask the user ALL of the following:

**2a. Project type:**
1. Single Page (Landing) — one scrollable page with all sections
2. Multi Page (Website) — separate page per section with shared navigation
3. App (Mobile) — native mobile app screens

**2b. Platform:**
1. Desktop (generates mobile variant too)
2. Mobile-first (generates desktop variant too)
3. App only (mobile screens, no desktop)

**2c. Color preferences:**
- Suggest a palette based on business type (see [DESIGN-PRINCIPLES.md](DESIGN-PRINCIPLES.md))
- Ask: "Use the suggested palette, or do you have specific colors in mind?"
- If custom: ask for primary color and accent color (hex or description)

**2d. Color mode:**
- Light (default for professional services)
- Dark

**2e. Style tone:**
- Suggest based on business type
- Ask: "Should the design feel more classic/formal or modern/bold?"

**2f. Any specific requests?**
- Free-form: "anything you want to add? specific sections, features, copy?"

Wait for ALL answers before proceeding. Do NOT generate until the user confirms.

### Step 3: Analyze lead data

Extract from the selected lead:

- **Name, address, phone** → contact info and hero content
- **Business type** → informs services, layout, tone
- **Photos** → analyze for color extraction and visual identity
- **Reviews** → extract best quotes for testimonials, identify themes for tagline
- **Rating + count** → social proof display
- **Hours** → schedule section
- **Editorial summary** → hero copy if available

Present a summary to the user:
```
Lead: Fernando Bliman - Asesor Legal
Data available: 9 photos, 5 reviews (all 5★), hours, phone
Suggested palette: navy #1a2744 + gold #c8a45c
Suggested fonts: EB Garamond (headlines) + Source Sans 3 (body)
Suggested tone: Classic, authoritative
```

Confirm with the user before proceeding.

### Step 4: Create Stitch project + design system

**4a. Create project:**
```
mcp__stitch__create_project({ title: "Lead Name - Type" })
```

**4b. Create design system** using preferences from Step 2:
```
mcp__stitch__create_design_system({
  projectId: "PROJECT_ID",
  designSystem: {
    displayName: "Lead Name Brand",
    theme: {
      colorMode: from step 2d,
      headlineFont: from analysis,
      bodyFont: from analysis,
      roundness: from business type,
      customColor: from step 2c,
      colorVariant: from analysis,
      designMd: "instructions combining user preferences + lead analysis"
    }
  }
})
```

See [DESIGN-PRINCIPLES.md](DESIGN-PRINCIPLES.md) for font/color/roundness guidance.

### Step 5: Generate screens

Use `GEMINI_3_1_PRO`. See [SCREEN-PROMPTS.md](SCREEN-PROMPTS.md) for prompt templates.

**Single Page:** 1 screen with all sections (hero, services, testimonials, contact, footer).

**Multi Page:** 5 screens — Home, About, Services, Reviews, Contact. Each with shared nav bar and footer.

**App:** 4-6 screens — Splash, Home, Services, Reviews, Profile/Contact, Booking.

For each screen:
```
mcp__stitch__generate_screen_from_text({
  projectId: "PROJECT_ID",
  prompt: "detailed prompt with real lead data...",
  deviceType: from step 2b,
  modelId: "GEMINI_3_1_PRO"
})
```

After all screens, apply the design system:
```
mcp__stitch__apply_design_system({
  projectId: "PROJECT_ID",
  selectedScreenInstances: [from get_project],
  assetId: "DESIGN_SYSTEM_ASSET_ID"
})
```

### Step 6: Download screenshots to stitch_designs/

After generation completes, download all screenshots locally.

**Output structure:**
```
stitch_designs/
└── lead-name-slug/
    ├── landing.png           (single page)
    ├── home.png              (multi page)
    ├── about.png             (multi page)
    ├── services.png          (multi page)
    ├── reviews.png           (multi page)
    ├── contact.png           (multi page)
    └── stitch_project.json   (project metadata: id, urls, screen ids)
```

For each screen, get the screenshot URL from `get_screen` or the generate response, then download:
```bash
mkdir -p stitch_designs/lead-name-slug
curl -L -o stitch_designs/lead-name-slug/screen-name.png "SCREENSHOT_URL"
```

Save project metadata:
```bash
python3 -c "
import json
meta = {
    'projectId': 'PROJECT_ID',
    'leadName': 'Lead Name',
    'projectType': 'single_page|multi_page|app',
    'screens': [
        {'name': 'landing', 'screenId': 'ID', 'screenshotUrl': 'URL', 'htmlUrl': 'URL'}
    ]
}
json.dump(meta, open('stitch_designs/lead-name-slug/stitch_project.json', 'w'), indent=2)
"
```

Present the results: total screens generated, local file paths, and Stitch project link.

Ask if the user wants to edit any screen (`edit_screens`) or generate variants (`generate_variants`).
