import type { Lead, AgentEvent, PipelineStep } from "@/types"

// ─── Proposal HTML must be declared before MOCK_LEADS references it ──────────

export const PROPOSAL_HTML_001 = `
<div style="font-family: Georgia, serif; max-width: 700px; margin: 0 auto; color: #1a1a1a; line-height: 1.7;">
  <div style="background: #FFFAF5; padding: 40px; border-radius: 12px; margin-bottom: 24px; border-left: 4px solid #C2410C;">
    <p style="font-size: 13px; text-transform: uppercase; letter-spacing: 0.1em; color: #C2410C; margin: 0 0 8px;">Commercial Proposal</p>
    <h1 style="font-size: 28px; margin: 0 0 8px; color: #1A1108;">La Parrilla de Juan</h1>
    <p style="color: #78716C; margin: 0;">Website redesign · Palermo, Buenos Aires · April 2026</p>
  </div>

  <h2 style="font-size: 18px; color: #1A1108; border-bottom: 1px solid #E7E5E4; padding-bottom: 8px;">Current Situation</h2>
  <p>Your business has <strong>4.8 stars and 412 Google reviews</strong> — an excellent reputation built over 15 years. But your current website, built in 2014, doesn't reflect that quality. It's not mobile-friendly in a city where 70% of searches happen on phones. There's no way to book a table, no visible menu, no WhatsApp button. Your competitors have all of that.</p>

  <h2 style="font-size: 18px; color: #1A1108; border-bottom: 1px solid #E7E5E4; padding-bottom: 8px; margin-top: 32px;">What We Propose</h2>
  <p>A complete website redesign that turns your online presence into a reservation machine:</p>
  <ul style="padding-left: 20px; color: #44403C;">
    <li>Modern, mobile-first design that loads in under 2 seconds</li>
    <li>Digital menu with your signature dishes and weekly specials</li>
    <li>WhatsApp reservation button visible on every screen</li>
    <li>Gallery section showcasing your best plates and atmosphere</li>
    <li>Google reviews badge with your 4.8★ prominently displayed</li>
    <li>SEO-optimized so you rank above competitors in Google Maps</li>
  </ul>
  <p style="margin-top: 16px;"><a href="/preview/lead-001" style="color: #C2410C; font-weight: bold;">→ View the preview of your new site</a></p>

  <h2 style="font-size: 18px; color: #1A1108; border-bottom: 1px solid #E7E5E4; padding-bottom: 8px; margin-top: 32px;">Investment</h2>
  <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-top: 16px;">
    <div style="background: #FAFAF9; padding: 20px; border-radius: 8px; border: 1px solid #E7E5E4; text-align: center;">
      <p style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: #78716C; margin: 0 0 8px;">Basic</p>
      <p style="font-size: 26px; font-weight: bold; color: #1A1108; margin: 0 0 8px;">$350 USD</p>
      <ul style="font-size: 13px; color: #44403C; text-align: left; padding-left: 16px;">
        <li>Landing page (4 sections)</li>
        <li>WhatsApp button</li>
        <li>Mobile responsive</li>
        <li>Basic SEO</li>
      </ul>
    </div>
    <div style="background: #FFF7ED; padding: 20px; border-radius: 8px; border: 2px solid #C2410C; text-align: center; position: relative;">
      <div style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background: #C2410C; color: white; font-size: 11px; padding: 2px 10px; border-radius: 20px;">Recommended</div>
      <p style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: #C2410C; margin: 0 0 8px;">Standard</p>
      <p style="font-size: 26px; font-weight: bold; color: #1A1108; margin: 0 0 8px;">$650 USD</p>
      <ul style="font-size: 13px; color: #44403C; text-align: left; padding-left: 16px;">
        <li>Full 6-section site</li>
        <li>Online menu / weekly specials</li>
        <li>Gallery + Google reviews</li>
        <li>3 months maintenance</li>
      </ul>
    </div>
    <div style="background: #FAFAF9; padding: 20px; border-radius: 8px; border: 1px solid #E7E5E4; text-align: center;">
      <p style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.08em; color: #78716C; margin: 0 0 8px;">Premium</p>
      <p style="font-size: 26px; font-weight: bold; color: #1A1108; margin: 0 0 8px;">$1,100 USD</p>
      <ul style="font-size: 13px; color: #44403C; text-align: left; padding-left: 16px;">
        <li>Everything in Standard</li>
        <li>Online reservation system</li>
        <li>Loyalty email capture</li>
        <li>12 months maintenance</li>
      </ul>
    </div>
  </div>

  <h2 style="font-size: 18px; color: #1A1108; border-bottom: 1px solid #E7E5E4; padding-bottom: 8px; margin-top: 32px;">Next Steps</h2>
  <ol style="padding-left: 20px; color: #44403C;">
    <li>Reply to this proposal to schedule a 20-minute call</li>
    <li>We finalize your content (photos, menu text, hours)</li>
    <li>Site live in 7 business days</li>
  </ol>
  <div style="margin-top: 32px; background: #C2410C; color: white; padding: 20px; border-radius: 8px; text-align: center;">
    <p style="margin: 0 0 4px; font-size: 18px; font-weight: bold;">Ready to get more reservations?</p>
    <p style="margin: 0; font-size: 14px; opacity: 0.9;">Reply to this email or WhatsApp us at +54 11 XXXX-XXXX</p>
  </div>
</div>
`

// ─── Demo leads ──────────────────────────────────────────────────────────────

export const MOCK_LEADS: Lead[] = [
  {
    id: "lead-001",
    name: "La Parrilla de Juan",
    industry: "Restaurante",
    location: "Palermo, Buenos Aires",
    description:
      "Parrilla argentina tradicional con más de 15 años en el barrio. Especialidad en cortes premium, empanadas caseras y asados los fines de semana.",
    currentSiteUrl: "http://laparrillajuan.com.ar",
    currentSiteQuality: "outdated",
    socialPresence: {
      instagram: "@laparrillajuan",
      googleMapsRating: 4.8,
      googleMapsReviews: 412,
    },
    painPoints: [
      "Site built in 2014, no mobile version",
      "No online reservations (competitors do)",
      "Menu not visible without scrolling far down",
      "Missing WhatsApp contact button",
    ],
    brandSignals: {
      primaryColor: "#8B2500",
      mood: "warm",
    },
    status: "complete",
    qualification: {
      score: 87,
      verdict: "HOT_LEAD",
      reasons: [
        "Site severely outdated — low bar to impress",
        "High Google rating (4.8) signals active business",
        "No mobile version in a 70% mobile city",
        "Premium zone (Palermo) = willingness to pay",
        "412 reviews = large existing audience to retain",
      ],
      risks: [
        "Owner may be set in their ways ('I've been here 15 years')",
        "Might negotiate on price",
      ],
      autoApproved: true,
    },
    previewUrl: "/preview/lead-001",
    proposalHtml: PROPOSAL_HTML_001,
    createdAt: "2026-04-14T10:23:00Z",
  },
  {
    id: "lead-002",
    name: "Estudio Dental Bernal",
    industry: "Clínica Dental",
    location: "Recoleta, Buenos Aires",
    description:
      "Clínica dental familiar con atención en ortodoncia, implantes y estética dental. 3 profesionales en staff, atención de lunes a sábado.",
    currentSiteUrl: "http://dentalbernal.com.ar",
    currentSiteQuality: "poor",
    socialPresence: {
      facebook: "EstudioDentalBernal",
      googleMapsRating: 4.3,
      googleMapsReviews: 89,
    },
    painPoints: [
      "Site loads in 6+ seconds",
      "No online appointment booking",
      "Missing trust signals (credentials, years)",
      "Generic stock photos, no real team",
    ],
    brandSignals: {
      mood: "formal",
    },
    status: "awaiting_approval",
    qualification: {
      score: 64,
      verdict: "WARM_LEAD",
      reasons: [
        "Poor site quality = easy improvement pitch",
        "Health sector is receptive to digital upgrades",
        "Established practice (active reviews)",
      ],
      risks: [
        "Score slightly below auto-approve threshold (65)",
        "Conservative sector, longer sales cycle",
      ],
      autoApproved: false,
    },
    createdAt: "2026-04-14T10:24:00Z",
  },
  {
    id: "lead-003",
    name: "Estudio Rolle",
    industry: "Estudio de Diseño",
    location: "Villa Crespo, Buenos Aires",
    description:
      "Estudio de branding y diseño gráfico fundado en 2019. Clientes en moda, gastronomía y cultura. Portfolio con +60 proyectos.",
    currentSiteUrl: "http://estudiorolle.com",
    currentSiteQuality: "poor",
    socialPresence: {
      instagram: "@estudiorolle",
      googleMapsRating: 4.6,
      googleMapsReviews: 34,
    },
    painPoints: [
      "Portfolio page not loading on mobile",
      "No case studies — just thumbnail grid",
      "Contact form broken (tested)",
      "No clear positioning or niche statement",
    ],
    brandSignals: {
      primaryColor: "#1A1A1A",
      mood: "minimal",
    },
    status: "qualifying",
    qualification: {
      score: 79,
      verdict: "HOT_LEAD",
      reasons: [
        "Broken contact form = direct business loss",
        "Design studio with poor site = credibility gap",
        "High Instagram presence = growth mindset",
      ],
      risks: ["May want to handle redesign internally"],
      autoApproved: true,
    },
    createdAt: "2026-04-14T10:25:00Z",
  },
  {
    id: "lead-004",
    name: "Carrefour Palermo",
    industry: "Supermercado",
    location: "Palermo, Buenos Aires",
    description: "Sucursal de cadena internacional de supermercados.",
    currentSiteUrl: "https://www.carrefour.com.ar",
    currentSiteQuality: "acceptable",
    socialPresence: {
      googleMapsRating: 3.9,
      googleMapsReviews: 1240,
    },
    painPoints: [],
    brandSignals: {},
    status: "discarded",
    qualification: {
      score: 8,
      verdict: "COLD_LEAD",
      reasons: ["Enterprise franchise — has internal digital team", "Corporate site managed centrally"],
      risks: ["Not a viable client for a boutique agency"],
      autoApproved: false,
    },
    createdAt: "2026-04-14T10:26:00Z",
  },
  {
    id: "lead-005",
    name: "Café Minerva",
    industry: "Cafetería",
    location: "San Telmo, Buenos Aires",
    description: "Cafetería de especialidad con tostadas artesanales, tartas y almuerzos. Espacio de trabajo remoto amigable.",
    currentSiteUrl: undefined,
    currentSiteQuality: "none",
    socialPresence: {
      instagram: "@cafeminerva",
      googleMapsRating: 4.5,
      googleMapsReviews: 203,
    },
    painPoints: [
      "No website at all — just Instagram",
      "Losing customers who search Google",
      "Can't show hours or menu online",
    ],
    brandSignals: {
      primaryColor: "#2D5016",
      mood: "friendly",
    },
    status: "researching",
    qualification: {
      score: 72,
      verdict: "HOT_LEAD",
      reasons: [
        "No website = 0 to 100 impact",
        "Active Instagram = engaged owner",
        "4.5 stars = quality product worth showcasing",
      ],
      risks: ["Small budget expected for a café"],
      autoApproved: true,
    },
    createdAt: "2026-04-14T10:27:00Z",
  },
]

// ─── Demo agent events ────────────────────────────────────────────────────────

export const MOCK_EVENTS_001: AgentEvent[] = [
  {
    id: "e1",
    agent: "management",
    status: "start",
    message: "Pipeline started for La Parrilla de Juan",
    timestamp: "2026-04-14T10:23:00Z",
  },
  {
    id: "e2",
    agent: "research",
    status: "start",
    message: "Scraping laparrillajuan.com.ar via Firecrawl...",
    timestamp: "2026-04-14T10:23:02Z",
  },
  {
    id: "e3",
    agent: "research",
    status: "progress",
    message: "Site found — built 2014, no responsive design, 4 pages",
    timestamp: "2026-04-14T10:23:08Z",
  },
  {
    id: "e4",
    agent: "research",
    status: "progress",
    message: "Google Maps: 4.8★ · 412 reviews · Open Mon-Sun",
    timestamp: "2026-04-14T10:23:11Z",
  },
  {
    id: "e5",
    agent: "research",
    status: "complete",
    message: "Lead profile built — 4 pain points identified",
    timestamp: "2026-04-14T10:23:14Z",
  },
  {
    id: "e6",
    agent: "qualification",
    status: "start",
    message: "Scoring against campaign criteria...",
    timestamp: "2026-04-14T10:23:15Z",
  },
  {
    id: "e7",
    agent: "qualification",
    status: "complete",
    message: "Score: 87/100 · HOT LEAD · Auto-approved ✓",
    timestamp: "2026-04-14T10:23:18Z",
  },
  {
    id: "e8",
    agent: "design",
    status: "start",
    message: "Generating design brief for restaurant (warm/appetizing)...",
    timestamp: "2026-04-14T10:23:19Z",
  },
  {
    id: "e9",
    agent: "design",
    status: "progress",
    message: "Taking screenshot of current site...",
    timestamp: "2026-04-14T10:23:24Z",
  },
  {
    id: "e10",
    agent: "design",
    status: "progress",
    message: "Calling Stitch MCP — sections: Hero + Menu + Gallery + Social Proof + Contact",
    timestamp: "2026-04-14T10:23:26Z",
  },
  {
    id: "e11",
    agent: "design",
    status: "complete",
    message: "Site generated via Stitch — quality score: 91/100",
    timestamp: "2026-04-14T10:24:05Z",
  },
  {
    id: "e12",
    agent: "proposal",
    status: "start",
    message: "Building commercial proposal...",
    timestamp: "2026-04-14T10:24:06Z",
  },
  {
    id: "e13",
    agent: "proposal",
    status: "complete",
    message: "Proposal ready — 3 budget tiers — awaiting human approval",
    timestamp: "2026-04-14T10:24:28Z",
  },
]

// ─── Demo pipeline steps ──────────────────────────────────────────────────────

export const MOCK_STEPS_001: PipelineStep[] = [
  { id: "research", label: "Research", agent: "research", state: "complete" },
  { id: "qualify", label: "Qualify", agent: "qualification", state: "complete" },
  { id: "design", label: "Design", agent: "design", state: "complete" },
  { id: "proposal", label: "Proposal", agent: "proposal", state: "complete" },
]

