# Design Principles

Core principles for generating website designs that look professional, not AI-generated.

## Philosophy

**Design is about what you eliminate, not what you add.**

- Question every element before including it
- One hero focal point per section — never equal visual weight
- Premium = (image quality x size) + (whitespace) - (decoration)

## Layout Rules

- Section spacing: minimum 112px between sections
- Related content spacing: 64px
- Individual element spacing: 24px
- Images should occupy 70-85% of card/hero space
- Never use uniform prominence — create clear hierarchy (120pt hero, 60pt supporting)

## What to Avoid

- Gradient backgrounds
- Floating glows, orbs, grain textures
- Animation blur effects
- Multiple font choices (max 2: one headline, one body)
- Color-coded CTAs — use white/black primary buttons
- Cookie-cutter layouts with equal-sized cards
- Overused fonts: Inter, Roboto, Arial (for headlines)
- Purple gradients, generic blue schemes

## Typography by Business Type

| Business Type | Headline Font | Body Font | Why |
|---|---|---|---|
| Law / Professional | EB_GARAMOND | SOURCE_SANS_THREE | Authority, trust |
| Medical / Health | PLUS_JAKARTA_SANS | NUNITO_SANS | Clean, approachable |
| Restaurant / Food | SORA | DM_SANS | Modern, inviting |
| Tech / Startup | GEIST | SPACE_GROTESK | Contemporary, sharp |
| Real Estate | MONTSERRAT | WORK_SANS | Solid, reliable |
| Creative / Design | EPILOGUE | MANROPE | Distinctive, refined |
| Default / Other | LEXEND | PUBLIC_SANS | Readable, neutral |

## Color Strategy

1. **Extract from photos** — if lead has photos, identify dominant and accent colors
2. **Business-appropriate defaults:**
   - Law: deep navy `#1a2744`, gold accent `#c8a45c`
   - Medical: clean teal `#0d9488`, white
   - Restaurant: warm earth `#92400e`, cream
   - Tech: slate `#1e293b`, electric blue `#3b82f6`
   - Real Estate: forest `#14532d`, gold `#d4a843`
3. **Color mode:** default LIGHT. Use DARK for tech, nightlife, creative
4. **Color variant:** TONAL_SPOT for professional, VIBRANT for creative, NEUTRAL for minimal

## Roundness by Tone

| Tone | Roundness | Use for |
|---|---|---|
| Corporate / Serious | ROUND_FOUR | Law, finance, medical |
| Balanced / Modern | ROUND_EIGHT | Most businesses |
| Friendly / Approachable | ROUND_TWELVE | Restaurants, retail, services |
| Playful / Bold | ROUND_FULL | Creative, kids, casual |

## Content Strategy from Lead Data

### From reviews:
- Extract the top-rated review quote for hero testimonial
- Identify recurring positive themes (e.g., "professional", "caring", "fast") for tagline
- Count 5-star reviews for social proof ("98% positive reviews")

### From photos:
- Use photo analysis to understand the business aesthetic
- If professional office → clean, minimal design
- If casual/retail → warmer, more colorful

### From hours:
- If open late/weekends → highlight availability as selling point
- Structure hours into a clean schedule component

### From rating:
- 4.5+ → prominently feature rating with stars in hero
- 4.0-4.5 → include in about section
- Below 4.0 → de-emphasize, focus on other strengths

## WCAG Compliance

All designs must meet WCAG 2.1 AA:
- Normal text: 4.5:1 contrast minimum
- Large text (18px+ bold, 24px+): 3:1 minimum
- UI components/icons: 3:1 minimum
