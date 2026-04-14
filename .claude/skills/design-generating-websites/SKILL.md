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
    ├── screens/
    │   ├── 01-home.png
    │   ├── 02-nosotros.png
    │   ├── ...
    ├── design-system/
    │   ├── color-palette.png     (generated color swatch image)
    │   ├── typography.md         (font choices and scale)
    │   └── tokens.json           (full design system theme dump)
    └── stitch_project.json       (project metadata)
```

**6a. Download screenshots:**
```bash
mkdir -p stitch_designs/lead-name-slug/screens
curl -L -o stitch_designs/lead-name-slug/screens/01-screen-name.png "SCREENSHOT_URL"
```

**6b. Generate and save design system assets:**

Create a color palette swatch image:
```bash
python3 -c "
import struct, zlib

def create_palette_png(colors, labels, path):
    w, h_per = 200, 60
    h = h_per * len(colors)
    def row(r, g, b, width):
        return b'\x00' + bytes([r, g, b]) * width
    raw = b''
    for hex_color in colors:
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2],16), int(hex_color[2:4],16), int(hex_color[4:6],16)
        for _ in range(h_per):
            raw += row(r, g, b, w)
    def png_chunk(ctype, data):
        c = ctype + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 2, 0, 0, 0)
    with open(path, 'wb') as f:
        f.write(sig + png_chunk(b'IHDR', ihdr) + png_chunk(b'IDAT', zlib.compress(raw)) + png_chunk(b'IEND', b''))
    # Also write a text version
    txt_path = path.replace('.png', '.txt')
    with open(txt_path, 'w') as f:
        for color, label in zip(colors, labels):
            f.write(f'{label}: {color}\n')

create_palette_png(
    ['PRIMARY_HEX', 'SECONDARY_HEX', 'ACCENT_HEX', 'NEUTRAL_HEX', 'BACKGROUND_HEX'],
    ['Primary', 'Secondary', 'Accent', 'Neutral', 'Background'],
    'stitch_designs/lead-name-slug/design-system/color-palette.png'
)
"
```

Save typography reference:
```bash
cat > stitch_designs/lead-name-slug/design-system/typography.md << 'EOF'
# Typography — Lead Name

- Headline: FONT_NAME
- Body: FONT_NAME
- Label: FONT_NAME

## Scale
- Hero: 96px
- Section: 48px
- Headline: 30px
- Subhead: 24px
- Body: 16px
- Caption: 14px
EOF
```

Dump full design system tokens:
```bash
python3 -c "
import json
tokens = {
    'colorMode': 'DARK|LIGHT',
    'primaryColor': '#hex',
    'secondaryColor': '#hex',
    'tertiaryColor': '#hex',
    'neutralColor': '#hex',
    'customColor': '#hex',
    'colorVariant': 'VARIANT',
    'headlineFont': 'FONT',
    'bodyFont': 'FONT',
    'labelFont': 'FONT',
    'roundness': 'ROUND_X'
}
json.dump(tokens, open('stitch_designs/lead-name-slug/design-system/tokens.json', 'w'), indent=2)
"
```

**6c. Save project metadata** (`stitch_project.json`) with project ID, lead name, type, design system asset ID, and all screen IDs with their local file paths.

Present the results: total screens, local paths, design system summary, and Stitch project link.

Ask if the user wants to edit any screen (`edit_screens`) or generate variants (`generate_variants`).
