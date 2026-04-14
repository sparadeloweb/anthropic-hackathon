# DESIGN.md — Folio

> Design system for Folio: an AI-native lead generation and proposal platform for digital agencies.
> Use this file as the primary context when generating UI with Stitch or any AI design tool.

---

## 1. Visual Theme & Atmosphere

Folio lives at the intersection of two worlds: the precision of a developer tool and the warmth of a creative agency. The interface should feel like a **smart colleague who never sleeps** — alert, organized, and capable. Not cold and robotic (no clinical blues), not warm and artsy (no expressive curves). Think: the operations dashboard of a well-run agency, built by people who care about craft.

The core tension Folio resolves visually: **automated intelligence that earns trust**. Every screen must communicate "this system is working hard for you" while the human always feels in control. Agent activity is visible, data is scannable, and checkpoints are unmissable.

**Dark mode** is the primary personality: dark surfaces (`#0C0C0E`) with a luminous violet accent (`#6366F1`), sparse borders, and dense information laid out with surgical precision. Like monitoring a live system — calm, focused, everything in its place.

**Light mode** flips to clean whites and warm off-whites, keeping the violet accent but softening the overall tone for client-facing views. A client opening their proposal link should feel like stepping into a polished agency website, not a developer dashboard.

**Key Characteristics:**
- Indigo/violet accent (`#6366F1`) — sophisticated, AI-native, not corporate
- Dark mode base: near-black with cool undertone (`#0C0C0E`, `#111113`, `#1A1A1E`)
- Light mode base: warm near-white (`#FAFAFA`, `#FFFFFF`, `#F4F4F6`)
- Shadow-as-border technique borrowed from Vercel — no heavy CSS borders
- Inter as the sole typeface — no custom fonts, maximum readability
- Agent activity shown as live terminal/log feed — monospace for AI output
- Color-coded lead scores: emerald (HOT), amber (WARM), slate (COLD)
- Two distinct layout personas: Agency Dashboard (dense, technical) and Client View (spacious, editorial)

---

## 2. Color Palette & Roles

### Brand
- **Folio Indigo** (`#6366F1`): Primary accent — buttons, active states, links, agent highlights, score rings. The only saturated color in the system.
- **Indigo Hover** (`#4F46E5`): Darker variant for hover/pressed states on primary elements.
- **Indigo Subtle** (`rgba(99,102,241,0.10)`): Soft indigo tint for hover backgrounds, selected rows, active cards.
- **Indigo Border** (`rgba(99,102,241,0.25)`): Tinted border for focused inputs and active panels.

### Dark Mode Surfaces
- **Base** (`#0C0C0E`): Page background. Near-black with a subtle cool undertone — not pure black.
- **Surface** (`#111113`): Card and panel backgrounds. The primary "layer 1" surface.
- **Elevated** (`#1A1A1E`): Elevated panels, modals, dropdowns. Clearly above surface.
- **Hover** (`#22222A`): Row and card hover state background.
- **Overlay** (`rgba(0,0,0,0.60)`): Modal backdrop.

### Light Mode Surfaces
- **Base** (`#FAFAFA`): Page background. Warm near-white.
- **Surface** (`#FFFFFF`): Cards and panels. Pure white against warm background.
- **Elevated** (`#F4F4F6`): Subtle elevation — sidebar, secondary panels.
- **Hover** (`#F0F0F4`): Row and card hover state.

### Borders
- **Border Default dark** (`rgba(255,255,255,0.07)`): Standard borders on dark surfaces — whisper-level.
- **Border Prominent dark** (`rgba(255,255,255,0.12)`): Emphasized card edges, section dividers.
- **Border Default light** (`rgba(0,0,0,0.08)`): Standard borders on light surfaces.
- **Border Prominent light** (`rgba(0,0,0,0.13)`): Emphasized borders on light.

### Text
- **Primary dark** (`#F1F1F3`): Main text on dark surfaces — not pure white, slightly cool.
- **Secondary dark** (`#8B8B96`): Supporting text, metadata, labels.
- **Tertiary dark** (`#55555F`): Disabled states, placeholders, de-emphasized info.
- **Primary light** (`#111113`): Main text on light surfaces.
- **Secondary light** (`#5C5C6E`): Supporting text on light.
- **Tertiary light** (`#9898A8`): Muted text on light.

### Semantic — Lead Scores
- **HOT** text: `#10B981` (emerald-500), bg: `rgba(16,185,129,0.12)`, border: `rgba(16,185,129,0.25)`
- **WARM** text: `#F59E0B` (amber-500), bg: `rgba(245,158,11,0.12)`, border: `rgba(245,158,11,0.25)`
- **COLD** text: `#6B7280` (gray-500), bg: `rgba(107,114,128,0.10)`, border: `rgba(107,114,128,0.20)`

### Semantic — Agent States
- **Processing** (indigo pulse): `#6366F1`
- **Completed**: `#10B981`
- **Error**: `#EF4444`
- **Waiting**: `#6B7280`
- **Checkpoint** (requires human): `#F59E0B`

---

## 3. Typography Rules

### Font Family
- **All text**: `Inter`, fallback: `system-ui, -apple-system, sans-serif`
- **Agent output / code**: `JetBrains Mono`, fallback: `ui-monospace, SFMono-Regular, monospace`

### Hierarchy

| Role | Size | Weight | Line Height | Letter Spacing | Notes |
|------|------|--------|-------------|----------------|-------|
| Page Title | 28px / 1.75rem | 600 | 1.20 | -0.5px | Dashboard section headers |
| Section Heading | 20px / 1.25rem | 600 | 1.30 | -0.3px | Panel and card titles |
| Card Title | 16px / 1rem | 600 | 1.40 | -0.2px | Lead name, proposal title |
| Body Large | 15px / 0.94rem | 400 | 1.60 | normal | Feature descriptions |
| Body | 14px / 0.88rem | 400 | 1.55 | normal | Standard UI text |
| Body Medium | 14px / 0.88rem | 500 | 1.55 | normal | Navigation, labels |
| Caption | 12px / 0.75rem | 400 | 1.40 | 0.1px | Metadata, timestamps |
| Label | 11px / 0.69rem | 500 | 1.20 | 0.3px | Uppercase badge text |
| Agent Log | 13px / 0.81rem | 400 | 1.70 | normal | Monospace — agent activity |
| Score | 32px / 2rem | 700 | 1.00 | -1px | Lead qualification score |

### Principles
- **Inter at all sizes** — no mixing typefaces in the UI chrome
- **Monospace only for agent output** — JetBrains Mono in the AgentFeed and proposal HTML
- **Three weights only**: 400 (read), 500 (interact/navigate), 600 (announce/headings)
- **Weight 700 reserved** exclusively for the lead score number — the single highest-signal element
- **Tight tracking on headings** (-0.2 to -0.5px) — feels engineered, not casual
- **Generous line-height on body** (1.55–1.70) — dense dashboards need breathing room

---

## 4. Spacing & Layout System

### Base unit: 4px

| Token | Value | Use |
|-------|-------|-----|
| `space-1` | 4px | Micro gaps, icon padding |
| `space-2` | 8px | Component internal spacing |
| `space-3` | 12px | Tight element groups |
| `space-4` | 16px | Standard component padding |
| `space-5` | 20px | Card internal padding |
| `space-6` | 24px | Section gaps, card gutters |
| `space-8` | 32px | Major section dividers |
| `space-10` | 40px | Page-level sections |
| `space-12` | 48px | Hero areas |

### Layout Structure

**Agency Dashboard** (2-column, 3-panel):
```
┌─────────────────────────────────────────────┐
│ Navbar (64px, sticky)                        │
├──────────┬──────────────────────────────────┤
│ Sidebar  │ Main Content                     │
│ (240px)  │                                  │
│ Campaign │ ┌──────────────┬───────────────┐ │
│ Settings │ │ Leads Board  │ Detail Panel  │ │
│ Nav      │ │ (list/cards) │ (agent feed + │ │
│          │ │              │  preview)     │ │
└──────────┴──────────────┴───────────────┴─┘
```

**Client View** (single-column, centered, max-width 800px):
```
┌─────────────────────────────────────────────┐
│ Minimal header (logo + agency name)          │
├─────────────────────────────────────────────┤
│              Content (max 800px)             │
│  - Project status timeline                  │
│  - Site preview (full width)                │
│  - Proposal sections                        │
│  - CTA + contact                            │
└─────────────────────────────────────────────┘
```

---

## 5. Component Patterns

### Buttons

**Primary (Indigo)**
- Background: `#6366F1`
- Text: `#FFFFFF`, 14px Inter weight 500
- Padding: 8px 16px
- Radius: 8px
- Hover: `#4F46E5`
- Shadow: none (flat, accent color carries weight)

**Secondary (Ghost)**
- Background: transparent
- Text: `#F1F1F3` (dark) / `#111113` (light)
- Border: shadow-as-border `rgba(255,255,255,0.12) 0px 0px 0px 1px` (dark) / `rgba(0,0,0,0.10) 0px 0px 0px 1px` (light)
- Padding: 8px 16px
- Radius: 8px
- Hover: bg `rgba(255,255,255,0.05)` (dark) / `rgba(0,0,0,0.04)` (light)

**Destructive**
- Background: `rgba(239,68,68,0.12)`
- Text: `#EF4444`
- Border: shadow-as-border `rgba(239,68,68,0.25) 0px 0px 0px 1px`
- Padding: 8px 16px
- Radius: 8px

**Approve (Checkpoint)**
- Background: `rgba(16,185,129,0.12)`
- Text: `#10B981`
- Border: shadow-as-border `rgba(16,185,129,0.30) 0px 0px 0px 1px`
- Padding: 8px 20px
- Radius: 8px
- Used exclusively at human checkpoints

### Cards & Panels

**Standard Card (dark)**
- Background: `#111113`
- Border: shadow-as-border `rgba(255,255,255,0.07) 0px 0px 0px 1px`
- Radius: 10px
- Padding: 20px
- Hover: bg `#1A1A1E`, border `rgba(255,255,255,0.12) 0px 0px 0px 1px`

**Standard Card (light)**
- Background: `#FFFFFF`
- Border: shadow-as-border `rgba(0,0,0,0.08) 0px 0px 0px 1px`
- Radius: 10px
- Padding: 20px
- Shadow: `rgba(0,0,0,0.04) 0px 2px 8px`

**Active / Selected Card**
- Add: `rgba(99,102,241,0.15) 0px 0px 0px 1px` border
- Add: subtle indigo bg tint `rgba(99,102,241,0.05)`

**Checkpoint Card (requires human action)**
- Left border accent: `3px solid #F59E0B`
- Background: `rgba(245,158,11,0.05)`
- Border: `rgba(245,158,11,0.20) 0px 0px 0px 1px`
- Glow: `rgba(245,158,11,0.08) 0px 0px 0px 4px`

### Lead Score Badge

```
Score number (32px Inter 700, color based on verdict)
Verdict label (11px Inter 500 uppercase, letter-spacing 0.3px)
Background pill with verdict color tint
```

- HOT: `#10B981` text, `rgba(16,185,129,0.12)` bg, pill radius `9999px`
- WARM: `#F59E0B` text, `rgba(245,158,11,0.12)` bg
- COLD: `#6B7280` text, `rgba(107,114,128,0.10)` bg

### Agent Feed (Live Log)

```
Scrollable terminal-like panel
Background: #0C0C0E (darker than surface)
Font: JetBrains Mono 13px, line-height 1.70
Each entry: [timestamp] [agent-tag] message
```

- Timestamp: `#55555F`, `11px`
- Agent tag: colored by agent — indigo (management), cyan (research), amber (qualification), violet (design), emerald (proposal)
- Message: `#C8C8D0`
- Active/running entry: left `2px solid #6366F1` border + indigo pulsing dot
- Completed entry: left `2px solid #10B981`
- Error entry: left `2px solid #EF4444`, message in `#EF4444`

### Step Indicator (Agent Pipeline Progress)

Horizontal progress bar — steps are dynamic, rendered from the active agent pipeline config.
Number of agents is variable; the component adapts to however many exist.

```
[ ● Agent A ] ── [ ● Agent B ] ── [ ▶ Agent C ] ── [ ○ Agent D ] ── [ ○ Agent N ]
     done             done            active            pending          pending
```

- Completed step: filled circle `#10B981`, checkmark icon, label `#10B981`
- Active step: pulsing circle `#6366F1`, label `#6366F1` weight 500
- Pending step: empty circle `rgba(255,255,255,0.15)`, label `#55555F`
- Connector line: `rgba(255,255,255,0.08)`, fills `#10B981` left-to-right as steps complete
- Step label: agent name from pipeline config (e.g. "Discovery", "Research", "Qualify", "Design", "Proposal")
- Overflow: if >6 agents, collapse middle steps to `• • •` pill with count
- Mobile: condenses to `"Agent 3 of 7"` text with a single progress bar beneath

### Qualification Checkpoint Card

```
┌─────────────────────────────────────────────┐  amber border
│  ⚠  Decision required                        │
│                                              │
│  [Score: 78]  [HOT LEAD]                     │
│  Restaurant "La Parrilla" · Buenos Aires     │
│                                              │
│  Why it's worth it:                          │
│  ✓ Outdated website (built in 2018)          │
│  ✓ 4.8★ on Google Maps, 340 reviews         │
│  ✓ Premium dining zone (Palermo)             │
│                                              │
│  Risks:                                      │
│  ↗ Already has social media presence        │
│                                              │
│  [ Continue with proposal ]  [ Discard ]    │
└─────────────────────────────────────────────┘
```

### Inputs & Forms

- Background: `rgba(255,255,255,0.04)` (dark) / `#FFFFFF` (light)
- Border: shadow-as-border `rgba(255,255,255,0.10) 0px 0px 0px 1px` (dark) / `rgba(0,0,0,0.10) 0px 0px 0px 1px` (light)
- Focus: border becomes `rgba(99,102,241,0.50) 0px 0px 0px 1px` + outer ring `rgba(99,102,241,0.15) 0px 0px 0px 3px`
- Padding: 10px 14px
- Radius: 8px
- Font: Inter 14px weight 400
- Placeholder: `#55555F` (dark) / `#9898A8` (light)

**Settings / Campaign Form** (multi-step wizard style):
- Each section is a card with a number indicator
- Tags/chips for multi-select options (industry, signals, negative filters)
- Tag: `rgba(99,102,241,0.12)` bg, `#6366F1` text, `rgba(99,102,241,0.25)` border, `6px` radius, `12px 10px` padding

### Site Preview Frame

```
Browser chrome mockup:
  - Top bar: 40px, bg #1A1A1E, radius 10px 10px 0 0
  - 3 dots (red/amber/green) + URL bar (grayed)
  - iframe below, no border, radius 0 0 10px 10px
  - Outer shadow: rgba(0,0,0,0.40) 0px 20px 60px -10px
```

### Navbar — Agency Mode

```
┌──────────────────────────────────────────────────────┐
│ ◆ Folio          Active campaign ▾      [+ New search]  [⚙] [●] │
└──────────────────────────────────────────────────────┘
```

- Height: 56px
- Background: `rgba(12,12,14,0.85)` + `backdrop-filter: blur(12px)` (dark)
- Border bottom: `rgba(255,255,255,0.07) 0px -1px 0px 0px inset`
- Logo: Inter 16px weight 700, `#F1F1F3`

### Navbar — Client Mode

```
┌──────────────────────────────────────────────────────┐
│  [Agency Logo/Name]                     [Schedule a call] │
└──────────────────────────────────────────────────────┘
```

- Cleaner, no internal nav links
- CTA visible at all times

---

## 6. Shadow & Depth System

| Level | CSS | Use |
|-------|-----|-----|
| Flat | none | Base surfaces, inline text |
| Border | `rgba(255,255,255,0.07) 0px 0px 0px 1px` (dark) | Standard card edges |
| Elevated | border + `rgba(0,0,0,0.30) 0px 4px 16px` | Modals, dropdowns, popovers |
| Deep | `rgba(0,0,0,0.50) 0px 20px 60px -10px` | Site preview frame, proposal modal |
| Glow (accent) | `rgba(99,102,241,0.20) 0px 0px 0px 4px` | Active/focused states |
| Glow (hot lead) | `rgba(16,185,129,0.15) 0px 0px 16px` | HOT lead card ambient |
| Glow (checkpoint) | `rgba(245,158,11,0.12) 0px 0px 20px` | Checkpoint card — draws attention |

**Philosophy**: On dark surfaces, depth comes from background lightness differences and subtle glow halos. Shadows are deep and soft (high blur, low opacity). On light surfaces, whisper shadows + border rings create layering.

---

## 7. Border & Radius System

| Token | Value | Use |
|-------|-------|-----|
| `radius-sm` | 4px | Badges, small tags, code blocks |
| `radius-md` | 8px | Buttons, inputs, small cards |
| `radius-lg` | 10px | Standard cards, panels |
| `radius-xl` | 14px | Large panels, proposal modal |
| `radius-2xl` | 20px | Site preview frame outer |
| `radius-pill` | 9999px | Score badges, status pills |

---

## 8. Motion & Animation Principles

**Philosophy**: Animation communicates agent activity and state transitions. Not decorative. Every animation serves information — "this is happening", "this just changed", "this needs attention".

| Element | Animation | Duration | Easing |
|---------|-----------|----------|--------|
| Agent status dot (active) | `pulse` opacity 1→0.3→1 | 1.5s | ease-in-out, infinite |
| Step indicator progress | slide + fill left-to-right | 400ms | ease-out |
| New agent log entry | slide in from bottom + fade | 200ms | ease-out |
| Card hover | `translateY(-1px)` + shadow intensify | 150ms | ease-out |
| Checkpoint card appear | scale 0.97→1 + fade in | 250ms | ease-out |
| Score badge count-up | number increment animation | 800ms | ease-out |
| Lead card HOT | subtle emerald glow pulse | 3s | ease-in-out, infinite |
| Modal/drawer open | slide up + fade | 250ms | ease-out |
| Theme toggle | cross-fade | 200ms | ease |

**Do not animate**: Layout shifts, text content changes, loading states that block interaction (use skeleton instead).

---

## 9. Tailwind Implementation Notes

```js
// tailwind.config.ts
theme: {
  extend: {
    colors: {
      folio: {
        base:     '#0C0C0E',
        surface:  '#111113',
        elevated: '#1A1A1E',
        hover:    '#22222A',
        accent:   '#6366F1',
        'accent-hover': '#4F46E5',
        'text-primary': '#F1F1F3',
        'text-secondary': '#8B8B96',
        'text-muted': '#55555F',
        hot:   '#10B981',
        warm:  '#F59E0B',
        cold:  '#6B7280',
        error: '#EF4444',
      }
    },
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
      mono: ['JetBrains Mono', 'ui-monospace', 'monospace'],
    },
    boxShadow: {
      'border-dark':    'rgba(255,255,255,0.07) 0px 0px 0px 1px',
      'border-dark-md': 'rgba(255,255,255,0.12) 0px 0px 0px 1px',
      'border-light':   'rgba(0,0,0,0.08) 0px 0px 0px 1px',
      'border-accent':  'rgba(99,102,241,0.40) 0px 0px 0px 1px',
      'glow-accent':    'rgba(99,102,241,0.20) 0px 0px 0px 4px',
      'glow-hot':       'rgba(16,185,129,0.15) 0px 0px 16px',
      'glow-checkpoint':'rgba(245,158,11,0.12) 0px 0px 20px',
      'preview':        'rgba(0,0,0,0.40) 0px 20px 60px -10px',
    }
  }
}
```

### Key Tailwind patterns
```
// Card dark
className="bg-folio-surface shadow-border-dark rounded-[10px] p-5 hover:bg-folio-elevated hover:shadow-border-dark-md transition-all duration-150"

// Primary button
className="bg-folio-accent hover:bg-folio-accent-hover text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors duration-150"

// HOT badge
className="text-emerald-500 bg-emerald-500/12 shadow-[rgba(16,185,129,0.25)_0px_0px_0px_1px] text-[11px] font-medium uppercase tracking-wider px-3 py-1 rounded-full"

// Checkpoint card
className="border-l-[3px] border-amber-500 bg-amber-500/5 shadow-glow-checkpoint rounded-[10px] p-5"

// Agent log entry (active)
className="border-l-2 border-folio-accent font-mono text-[13px] text-folio-text-secondary leading-[1.70] pl-3"

// Input
className="bg-white/4 shadow-border-dark focus:shadow-border-accent focus:shadow-glow-accent rounded-lg px-3.5 py-2.5 text-sm text-folio-text-primary placeholder:text-folio-text-muted outline-none transition-shadow duration-150"
```
