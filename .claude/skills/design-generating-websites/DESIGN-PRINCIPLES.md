# Design Principles

Core principles for generating website designs that look professional, not AI-generated. Derived from [ui-ux-pro-max](https://skills.sh/kimny1143/claude-code-template/ui-ux-pro-max) and [frontend-design](https://skills.sh/anthropics/skills/frontend-design).

---

## Five Fundamental Rules

1. **Question before creating** — challenge necessity of every element. Build without questionable components first. If unsure, delete.
2. **Single hero per section** — identify and commit to one primary focal point before generating. Never allow two elements to compete.
3. **Reject uniform prominence** — create 120pt hero elements with 60pt supporting. Never use equivalent visual weight across siblings.
4. **Propose deletion over addition** — when uncertain, recommend removing elements rather than adding features.
5. **Critique before improvement** — identify 3+ existing problems before suggesting solutions or new screens.

## Design Direction

Before generating, commit to a **bold aesthetic direction** appropriate to the business. Do not default to "clean and modern" for everything.

| Business Type | Aesthetic Direction | Tone |
|---|---|---|
| Law / Finance | Luxury minimal | Authoritative, restrained |
| Medical / Health | Clinical clean | Trustworthy, precise |
| Restaurant / Food | Warm editorial | Inviting, tactile |
| Tech / Startup | Sharp geometric | Forward, confident |
| Real Estate | Bold typographic | Solid, aspirational |
| Creative / Design | Maximalist / Brutalist | Distinctive, expressive |
| Retail / Commerce | Visual-first | Product-focused, immediate |

Establish the tone FIRST, then let every decision (font, color, spacing, imagery) serve that direction.

## Premium Design Formula

**Premium = (image quality x size) + (whitespace) - (decoration)**

Three pillars:
- Large imagery occupying 70-85% of card/hero space
- Generous section spacing (minimum 112px between sections)
- Restraint in effects — every element must justify its existence

## Spacing System

| Token | Value | Use |
|---|---|---|
| Section gap | 112px min | Between major sections |
| Group gap | 64px | Related content groups |
| Element gap | 24px | Individual elements |
| Card gap (2-col) | 48px | Hero sections, comparisons |
| Card gap (3-col) | 32px | Features, pricing |
| Card gap (4-col) | 24px | Product showcase |

## Grid Architecture

- **4 columns**: product/service showcase (24px gaps)
- **3 columns**: features, pricing, team (32px gaps)
- **2 columns**: hero sections, comparisons, about (48px gaps)
- **Asymmetric layouts preferred** — use overlap, offset, and varied column widths to break uniformity

## Typography

### Selection by Business Type

| Business Type | Headline Font | Body Font | Why |
|---|---|---|---|
| Law / Professional | EB_GARAMOND | SOURCE_SANS_THREE | Authority, trust |
| Medical / Health | PLUS_JAKARTA_SANS | NUNITO_SANS | Clean, approachable |
| Restaurant / Food | SORA | DM_SANS | Modern, inviting |
| Tech / Startup | GEIST | SPACE_GROTESK | Contemporary, sharp |
| Real Estate | MONTSERRAT | WORK_SANS | Solid, reliable |
| Creative / Design | EPILOGUE | MANROPE | Distinctive, refined |
| Default / Other | LEXEND | PUBLIC_SANS | Readable, neutral |

### Scale

| Token | Size | Use |
|---|---|---|
| Hero | 96px | Main page headline |
| Section | 48px | Section titles |
| Headline | 30px | Card headings, subheadings |
| Subhead | 24px | Supporting titles |
| Body | 16px | Paragraph text |
| Caption | 14px | Labels, metadata |

### Rules
- Maximum 2 fonts per design (1 headline + 1 body)
- Never use overused fonts for headlines: Inter, Roboto, Arial
- Use distinctive, characterful fonts that reinforce the aesthetic direction
- Body font must prioritize readability

## Color Strategy

### Extraction priority
1. **Extract from lead photos** — identify dominant and accent colors from business imagery
2. **Fall back to business-appropriate defaults** if no photos or unclear palette

### Default palettes by business type

| Type | Primary | Accent | Color Mode |
|---|---|---|---|
| Law | `#1a2744` deep navy | `#c8a45c` gold | LIGHT |
| Medical | `#0d9488` teal | `#ffffff` white | LIGHT |
| Restaurant | `#92400e` warm earth | `#fef3c7` cream | LIGHT |
| Tech | `#1e293b` slate | `#3b82f6` electric blue | DARK |
| Real Estate | `#14532d` forest | `#d4a843` gold | LIGHT |
| Creative | `#18181b` black | `#a78bfa` violet | DARK |
| Nightlife | `#09090b` black | `#f59e0b` amber | DARK |

### Color variant guide
- **TONAL_SPOT** — professional services, balanced
- **VIBRANT** — creative, entertainment, food
- **NEUTRAL** — minimal, luxury, law
- **MONOCHROME** — editorial, photography
- **EXPRESSIVE** — kids, casual, playful
- **FIDELITY** — when extracting exact brand colors from photos

### Rules
- Develop a cohesive palette: one dominant, one accent, one neutral
- No purple gradients or generic blue schemes
- No color-coded CTAs — primary buttons are white/dark or inverse
- Limit brand color usage to 1-2 sections maximum

## Roundness by Tone

| Tone | Roundness | Use for |
|---|---|---|
| Corporate / Serious | ROUND_FOUR | Law, finance, medical |
| Balanced / Modern | ROUND_EIGHT | Most businesses |
| Friendly / Approachable | ROUND_TWELVE | Restaurants, retail, services |
| Playful / Bold | ROUND_FULL | Creative, kids, casual |

## Spatial Composition

Go beyond basic grid layouts:
- **Asymmetry** — offset hero images, unequal column widths
- **Overlap** — elements overlapping sections for depth (text over image, card breaking grid)
- **Diagonal flow** — guide the eye diagonally rather than straight down
- **Grid-breaking** — one element per section that intentionally breaks the grid for emphasis
- **Varied card sizes** — first item hero-sized, rest smaller. Never uniform cards.

## Motion and Interaction

Include in Stitch prompts where appropriate:
- Subtle hover states on cards and buttons (scale 1.02, slight shadow)
- Scroll-triggered fade-in for sections below the fold
- Staggered entrance animations for lists/grids (items appear sequentially)
- Smooth transitions between states

Do NOT include:
- Parallax scrolling (performance issues)
- Auto-playing carousels
- Complex loading animations
- Anything that delays content visibility

## Button Styles

| Type | Style | Use |
|---|---|---|
| Primary CTA | White bg / black text (or inverse in dark mode) | One per section max |
| Secondary | Border only, transparent bg | Supporting actions |
| Disabled | Reduced opacity (white/5 bg, white/70 text) | Inactive states |

Rules:
- No color-coded CTAs (no green "success" buttons, no red "delete" buttons in marketing pages)
- One primary CTA per visible viewport
- Button text: action-oriented, specific ("Agendar Consulta", not "Click aqui")

## Explicit Prohibition List

**NEVER include:**
- Gradient backgrounds (`bg-gradient-to-*`)
- Floating glows or orbs
- Grain textures or noise overlays
- Animation blur effects
- Generic stock photo placeholders
- Emoji as icons (use Lucide Icons or similar)
- `shadow-lg shadow-indigo-500/20` style colored shadows
- Cookie-cutter equal-sized card grids
- Cliched color schemes (purple gradients, teal-to-blue)
- More than 2 font families

**ALWAYS require:**
- Single-color backgrounds per section
- Lucide Icons or similar icon system (no emoji)
- Real data from lead (name, address, phone, reviews) — never Lorem Ipsum
- Explicit whitespace between all sections
- Image-dominant hero sections when photos are available

## Content Strategy from Lead Data

### From reviews
- Extract the highest-rated review for hero testimonial
- Identify recurring positive themes ("profesional", "dedicado", "rapido") for tagline
- Count 5-star reviews for social proof ("98% de clientes satisfechos")
- Use 3-5 reviews verbatim for testimonials page

### From photos
- Analyze visual identity: formal vs casual, modern vs traditional
- Extract dominant color for design system seed
- Use as hero backgrounds, about section imagery, gallery
- If professional office → clean, restrained design
- If casual/retail → warmer, more expressive

### From hours
- Open late/weekends → highlight availability as differentiator
- Structure as a clean schedule component
- Identify "Abierto ahora" as real-time CTA opportunity

### From rating
- 4.5+ → prominently feature in hero with star display
- 4.0-4.5 → include in about section, not hero
- Below 4.0 → de-emphasize, focus on services and reviews content

### From business type
- Infer services to display on services page
- Choose appropriate section naming ("Nuestros Servicios", "Areas de Practica", "Especialidades")
- Determine CTA language ("Agendar Consulta" for law, "Reservar" for restaurants)

## Pre-Delivery Validation

Before considering a design complete, verify:

- [ ] Single hero per section — squint test passes (business identifiable with narrowed eyes)
- [ ] No uniform prominence — clear visual hierarchy in every section
- [ ] Section gaps >= 112px
- [ ] Images are dominant (70-85% of hero/card space)
- [ ] No prohibited elements (gradients, glows, grain, emoji)
- [ ] Primary CTA is white/dark, not colored
- [ ] Max 2 fonts used
- [ ] Real lead data used throughout (no placeholder text)
- [ ] WCAG 2.1 AA contrast: normal text 4.5:1, large text 3:1, UI components 3:1
- [ ] Responsive consideration: prompts specify both desktop and mobile

## Reference Benchmarks

For quality inspiration, reference these levels of craft:
- **Spitfire Audio** — product imagery dominance, whitespace mastery
- **Native Instruments** — typography hierarchy, dark UI excellence
- **iZotope** — premium grid layouts, restrained color use
- **Stripe** — clean information architecture, subtle animation
- **Linear** — modern SaaS, sharp geometric aesthetic
