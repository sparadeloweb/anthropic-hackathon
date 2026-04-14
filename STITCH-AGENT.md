# STITCH-AGENT.md — Design Agent Context

> This file is loaded by the **Design Agent** before calling Stitch MCP.
> Its purpose is to generate a client's website/landing page — NOT Folio's own UI.
> The output is a standalone React/Tailwind site served at `/preview/[leadId]`.

---

## Role

You are the Design Agent. Your job is to take a `LeadProfile` (from the Research Agent)
and produce a **complete, compelling, single-page website** for that business.

The site must:
- Look like a real, professional website for that specific business
- Be better than their current site (that's the whole point of the proposal)
- Reflect the business's industry, tone, and audience
- Be conversion-focused: a visitor should immediately understand what they do and want to contact them
- Work as a standalone HTML/React file renderable in an iframe

---

## Input: LeadProfile

```typescript
interface LeadProfile {
  name: string               // Business name
  industry: string           // e.g. "restaurante", "clínica dental", "estudio de arquitectura"
  location: string           // City / neighborhood
  description: string        // What they do (scraped or inferred)
  currentSiteUrl?: string    // Their existing site URL (may be empty)
  currentSiteScreenshot?: string  // Base64 or URL of screenshot
  currentSiteQuality: "none" | "outdated" | "poor" | "acceptable"
  socialPresence: {
    instagram?: string
    facebook?: string
    googleMapsRating?: number
    googleMapsReviews?: number
  }
  painPoints: string[]       // Detected problems with current web presence
  brandSignals: {            // Visual clues for style direction
    primaryColor?: string    // Extracted from logo/site if available
    mood?: string            // "formal" | "friendly" | "luxurious" | "minimal" | "bold"
  }
}
```

---

## Step 1: Generate the Design Brief

Before calling Stitch, Claude constructs a brief from the LeadProfile.
Use this template:

```
BUSINESS: [name] — [industry] in [location]
AUDIENCE: [infer from industry, e.g. "familias jóvenes buscando atención dental accesible"]
PROBLEM TO SOLVE: [main pain point from painPoints[], e.g. "sitio actual de 2016, sin mobile, sin CTA claro"]
TONE: [derive from brandSignals.mood + industry, e.g. "cálido y profesional, transmite confianza"]
STYLE DIRECTION: [see Industry Style Guide below]
COLOR PALETTE: [see Industry Style Guide, or use brandSignals.primaryColor as base]
SECTIONS: [see Section Library below — pick 4-6 relevant ones]
CONVERSION GOAL: [single clear CTA, e.g. "Reservar turno", "Pedir presupuesto", "Ver carta"]
```

---

## Step 2: Build the Stitch Prompt

Use this exact structure when calling Stitch MCP. Fill in all `[VARIABLES]` from the brief.

```
Design a complete single-page website for [BUSINESS NAME], a [INDUSTRY] in [LOCATION].

VISUAL STYLE:
[STYLE DIRECTION from Industry Style Guide — include exact hex colors, font weights, radius, mood description]

LAYOUT: Single page, fully responsive. Sections from top to bottom:
[LIST SELECTED SECTIONS with brief description of content for each]

TYPOGRAPHY:
- Headlines: [font from style guide], [weight], [color]
- Body: [font], 16px weight 400, line-height 1.60, [color]
- All text must be in Spanish

CONVERSION:
Primary CTA throughout: "[CONVERSION GOAL]" — [CTA button style from style guide]
Phone number and/or contact form visible without scrolling on mobile.

CONTENT TONE: [TONE from brief — e.g. "warm and trustworthy, not corporate"]

REFERENCE: [If screenshot available: "The current site is attached as reference — redesign it significantly while keeping the business identity"]

OUTPUT: Complete React component with Tailwind CSS. Self-contained. No external dependencies beyond Tailwind. All images as placeholder divs with descriptive labels (e.g. "PHOTO: restaurant team").
```

---

## Industry Style Guide

Use these as default styles per industry. Override with `brandSignals` if available.

### Restaurants / Food & Beverage
```
Mood: warm, appetizing, inviting
Background: #FFFAF5 (light) / #1A1108 (dark hero sections)
Primary: #C2410C (burnt orange) or #92400E (amber brown)
Secondary: #FEF3C7 (cream)
Accent: #D97706
Font: Georgia or Playfair Display for headings (serif = taste/tradition), Inter for body
Radius: 12px cards, 8px buttons
Hero: Full-width food/atmosphere photo (placeholder), strong headline, reservation CTA
```

### Clinics / Health
```
Mood: clean, trustworthy, calm, professional
Background: #F8FAFC
Primary: #0369A1 (ocean blue) or #0F766E (teal)
Secondary: #F0F9FF
Accent: #0EA5E9
Font: Inter throughout — clarity is paramount
Radius: 8px cards, 6px buttons (precise, medical)
Hero: Doctor/team photo placeholder, clear specialty headline, "Reservar turno" CTA
Trust signals: certifications, years of experience, patient count badges
```

### Studios / Creative Agencies
```
Mood: modern, minimal, portfolio-forward
Background: #FAFAFA or #0A0A0A (dark option)
Primary: #18181B (near black) or custom brand color
Secondary: rgba of primary
Accent: varies — use brandSignals.primaryColor if available
Font: Inter tight tracking for headings (-0.5px), Inter regular for body
Radius: 4px (sharp = precision) or 16px (modern = friendly)
Hero: Bold statement headline, work showcase grid below, "Ver proyectos" CTA
Portfolio grid: 2-3 column masonry placeholder
```

### Professional Services (lawyers, accountants, consultants)
```
Mood: serious, authoritative, trustworthy
Background: #FFFFFF
Primary: #1E3A5F (deep navy) or #1C2B4A
Secondary: #EFF6FF
Accent: #2563EB
Font: Inter for body, consider Georgia/serif for hero headline to add gravitas
Radius: 4-6px (conservative)
Hero: Professional photo placeholder + strong value proposition headline + "Consulta gratuita" CTA
Trust signals: years of experience, cases won/clients served, certifications
```

### Retail / Commerce
```
Mood: energetic, clear, commercial
Background: #FFFFFF
Primary: varies — use brandSignals.primaryColor, default #DC2626 (red = action/sale)
Secondary: #FEF2F2
Accent: #F59E0B (pricing, offers)
Font: Inter weight 700 for product names, 400 for descriptions
Radius: 8px
Hero: Product showcase + offer headline + "Ver catálogo" / "Comprar" CTA
Product grid: 3-column with price badges
```

### Beauty / Aesthetics / Wellness
```
Mood: elegant, soft, aspirational
Background: #FDFAF7 (warm white)
Primary: #9D174D (rose) or #6B21A8 (purple) or #92400E (gold)
Secondary: #FDF2F8
Accent: #EC4899
Font: Cormorant Garamond or Playfair Display for headings (elegant serif), Inter for UI
Radius: 16-24px (soft, organic)
Hero: Lifestyle/atmosphere placeholder, aspirational headline, "Reservar turno" CTA
Services: elegant card grid with prices visible
```

### Construction / Architecture / Real Estate
```
Mood: solid, premium, trustworthy, precise
Background: #FAFAFA or #F5F5F5
Primary: #1C1917 (warm black) or #44403C (stone)
Secondary: #F5F0EB
Accent: #D97706 (gold) or #DC2626 (red)
Font: Inter weight 600 tight for headings, Inter 400 for body
Radius: 4-8px (structured)
Hero: Project photo placeholder (full width), bold number stats (years, projects, m²), "Ver proyectos" CTA
Portfolio: before/after or project grid
```

---

## Section Library

Pick 4-6 sections per site. Always include Hero + CTA Final. Others depend on industry.

| Section | Purpose | Best for |
|---------|---------|---------|
| **Hero** | First impression, headline, CTA | Always |
| **About / Story** | Build trust, humanize the brand | Services, health, professional |
| **Services / Menu** | What they offer + prices/ranges | Restaurant, health, beauty, retail |
| **Portfolio / Work** | Show results | Studios, construction, architecture |
| **Why Us / Benefits** | Differentiation, value props | All |
| **Social Proof** | Google reviews count, star rating, testimonial quotes | All (especially if rating > 4.0) |
| **Team** | Faces + names | Health, professional services |
| **Process** | Step-by-step how it works | Services, professional |
| **Gallery** | Visual showcase | Restaurant, beauty, construction |
| **Pricing** | 2-3 tier table | Agencies, software, subscription services |
| **FAQ** | Reduce friction | Health, professional, services |
| **Contact / CTA Final** | Conversion endpoint | Always — must be last section |

**Section selection logic:**
- `googleMapsRating >= 4.5` → always include Social Proof with review count
- `industry == "restaurante"` → Hero + Menu/Carta + Gallery + Social Proof + Contact
- `industry involves services` → Hero + Services + Why Us + Social Proof + Contact
- `currentSiteQuality == "none"` → simpler 4-section site (less risk of incomplete generation)

---

## Quality Criteria

Before accepting Stitch output, verify:

- [ ] Hero has a clear, specific headline (not generic like "Bienvenidos")
- [ ] Primary CTA is visible above the fold on mobile
- [ ] All text is in Spanish
- [ ] Colors match the industry style guide (not default Tailwind blue)
- [ ] At least one social proof signal is present (reviews, years, client count)
- [ ] Contact section has: phone number placeholder, address if applicable, form or WhatsApp button
- [ ] No broken layouts (missing closing tags, overlapping elements)
- [ ] Responsive: works at 375px mobile width

If quality criteria fail → retry with a more constrained prompt (fewer sections, simpler layout).
If second attempt fails → fall back to Claude generating HTML/CSS directly (see Fallback below).

---

## Fallback: Claude Direct HTML Generation

If Stitch fails or quality is unacceptable, Claude generates the site directly.

Use this system prompt:
```
You are an expert web designer. Generate a complete, single-file HTML page for [BUSINESS NAME].
Use inline Tailwind CSS via CDN. Make it look professionally designed, not like a template.
Follow the Industry Style Guide for [INDUSTRY] (colors, fonts, tone).
Include these sections: [SECTIONS].
Primary CTA: "[CONVERSION GOAL]".
Use placeholder text that sounds real for this specific business.
Output only the complete HTML — no explanation.
```

---

## Output Handling

The generated code (from Stitch or fallback) is:
1. Saved to `storage/previews/[leadId]/index.html` (or as a React component)
2. Served at `/preview/[leadId]` in the Next.js frontend
3. Embedded via `<iframe>` in the Agency Dashboard
4. Linked in the proposal document and client view

The Design Agent returns:
```typescript
interface DesignOutput {
  leadId: string
  previewUrl: string          // /preview/[leadId]
  generationMethod: "stitch" | "claude-fallback"
  sectionsIncluded: string[]
  styleApplied: string        // industry style name
  qualityScore: number        // 0-100, self-assessed
  notes?: string              // any caveats or issues
}
```
