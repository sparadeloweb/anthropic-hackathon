"use client"

import { useState } from "react"
import { FileText, Map, DollarSign, CheckCircle, Send } from "lucide-react"
import { cn } from "@/lib/utils"
import type { Lead } from "@/types"

type ProposalTab = "brief" | "roadmap" | "budget"

interface ProposalTabsProps {
  lead: Lead
  onApprove: () => void
}

export function ProposalTabs({ lead, onApprove }: ProposalTabsProps) {
  const [tab, setTab] = useState<ProposalTab>("brief")

  return (
    <div className="flex flex-col h-full gap-3">
      {/* Sub-tab bar */}
      <div className="flex items-center gap-1 border-b border-folio-border/[0.08] pb-3">
        <ProposalTabBtn id="brief" label="Brief" icon={<FileText size={12} />} active={tab === "brief"} onClick={() => setTab("brief")} />
        <ProposalTabBtn id="roadmap" label="Roadmap" icon={<Map size={12} />} active={tab === "roadmap"} onClick={() => setTab("roadmap")} />
        <ProposalTabBtn id="budget" label="Budget" icon={<DollarSign size={12} />} active={tab === "budget"} onClick={() => setTab("budget")} />

        {lead.status === "complete" ? (
          <button
            onClick={onApprove}
            className="ml-auto flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-folio-accent hover:bg-folio-accent/90 text-white text-xs font-semibold transition-colors shadow-glow-accent"
          >
            <Send size={11} />
            Approve & send
          </button>
        ) : null}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto">
        {tab === "brief" ? <BriefTab lead={lead} /> : null}
        {tab === "roadmap" ? <RoadmapTab /> : null}
        {tab === "budget" ? <BudgetTab proposalHtml={lead.proposalHtml} /> : null}
      </div>
    </div>
  )
}

interface ProposalTabBtnProps {
  id: ProposalTab
  label: string
  icon: React.ReactNode
  active: boolean
  onClick: () => void
}

function ProposalTabBtn({ label, icon, active, onClick }: ProposalTabBtnProps) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors",
        active
          ? "bg-folio-elevated text-folio-text-primary"
          : "text-folio-text-muted hover:text-folio-text-secondary"
      )}
    >
      {icon}
      {label}
    </button>
  )
}

// ─── Brief Tab ───────────────────────────────────────────────────────────────

function BriefTab({ lead }: { lead: Lead }) {
  return (
    <div className="space-y-4">
      <Section title="Business Overview">
        <p className="text-sm text-folio-text-secondary leading-relaxed">{lead.description}</p>
        <div className="grid grid-cols-2 gap-3 mt-3">
          <Stat label="Industry" value={lead.industry} />
          <Stat label="Location" value={lead.location} />
          {lead.socialPresence.googleMapsRating ? (
            <Stat
              label="Google Rating"
              value={`${lead.socialPresence.googleMapsRating}★ (${lead.socialPresence.googleMapsReviews} reviews)`}
            />
          ) : null}
          <Stat label="Current site" value={lead.currentSiteQuality === "none" ? "None" : lead.currentSiteQuality} />
        </div>
      </Section>

      <Section title="Pain Points Identified">
        <ul className="space-y-2">
          {lead.painPoints.map((point, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-folio-text-secondary">
              <span className="text-red-400 mt-0.5 shrink-0">✗</span>
              <span>{point}</span>
            </li>
          ))}
        </ul>
      </Section>

      {lead.qualification ? (
        <Section title="Qualification">
          <div className="space-y-1.5">
            {lead.qualification.reasons.map((reason, i) => (
              <div key={i} className="flex items-start gap-2 text-sm text-folio-text-secondary">
                <CheckCircle size={13} className="text-emerald-400 mt-0.5 shrink-0" />
                <span>{reason}</span>
              </div>
            ))}
          </div>
        </Section>
      ) : null}
    </div>
  )
}

// ─── Roadmap Tab ──────────────────────────────────────────────────────────────

const ROADMAP_STEPS = [
  {
    day: "Day 1–2",
    title: "Discovery call + content gathering",
    desc: "Confirm scope, collect photos, menu/service text, brand assets",
    nodeColor: "bg-violet-400",
    isLaunch: false,
    isPostLaunch: false,
  },
  {
    day: "Day 3–4",
    title: "Design & development",
    desc: "Build full site based on the generated preview — adapt copy to real content",
    nodeColor: "bg-blue-400",
    isLaunch: false,
    isPostLaunch: false,
  },
  {
    day: "Day 5",
    title: "Internal review + staging",
    desc: "QA on mobile/desktop, fix any issues before showing the client",
    nodeColor: "bg-blue-400",
    isLaunch: false,
    isPostLaunch: false,
  },
  {
    day: "Day 6",
    title: "Client review",
    desc: "Present staging link — collect feedback, apply up to 2 revision rounds",
    nodeColor: "bg-folio-hot",
    isLaunch: false,
    isPostLaunch: false,
  },
  {
    day: "Day 7",
    title: "Launch 🚀",
    desc: "Deploy to production domain — DNS propagation, SSL, final check",
    nodeColor: "bg-emerald-400",
    isLaunch: true,
    isPostLaunch: false,
  },
  {
    day: "Post-launch",
    title: "Maintenance",
    desc: "Monthly updates included per selected tier",
    nodeColor: "bg-folio-text-muted",
    isLaunch: false,
    isPostLaunch: true,
  },
]

function RoadmapTab() {
  return (
    <div className="relative pl-10 pr-2">
      {/* Continuous left rail */}
      <div className="absolute left-[18px] top-3 bottom-3 w-0.5 bg-folio-border/[0.15] rounded-full" />

      <div className="space-y-5">
        {ROADMAP_STEPS.map((step, i) => (
          <div key={i} className={cn("relative", step.isPostLaunch && "pt-4")}>
            {/* Dashed separator before post-launch */}
            {step.isPostLaunch ? (
              <div className="absolute -top-0 -left-10 right-0 border-t border-dashed border-folio-border/[0.15]" />
            ) : null}

            {/* Node on the rail */}
            <div
              className={cn(
                "absolute -left-[29px] top-0.5 w-5 h-5 rounded-full border-2 flex items-center justify-center shrink-0",
                step.isLaunch
                  ? "border-emerald-400 bg-emerald-400/20 shadow-[0_0_8px_rgba(52,211,153,0.35)]"
                  : "border-folio-border/[0.2] bg-folio-elevated"
              )}
            >
              {step.isLaunch ? (
                <div className="w-2 h-2 rounded-full bg-emerald-400" />
              ) : (
                <div className={cn("w-2 h-2 rounded-full", step.nodeColor)} />
              )}
            </div>

            {/* Content */}
            <div>
              <span
                className={cn(
                  "inline-block text-[10px] font-mono px-1.5 py-0.5 rounded-md mb-1",
                  step.isLaunch
                    ? "bg-emerald-400/10 text-emerald-400"
                    : step.isPostLaunch
                      ? "text-folio-text-muted"
                      : "bg-folio-elevated text-folio-accent"
                )}
              >
                {step.day}
              </span>
              <h4 className={cn("text-sm font-medium mb-0.5", step.isPostLaunch ? "text-folio-text-secondary" : "text-folio-text-primary")}>
                {step.title}
              </h4>
              <p className="text-xs text-folio-text-muted leading-relaxed">{step.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// ─── Budget Tab ───────────────────────────────────────────────────────────────

const BUDGET_TIERS = [
  {
    name: "Basic",
    price: "$350",
    currency: "USD",
    description: "A clean, fast landing page to establish online presence.",
    features: [
      "Landing page (4 sections)",
      "WhatsApp button",
      "Mobile responsive",
      "Basic SEO setup",
    ],
    cta: "Select Basic",
    highlight: false,
  },
  {
    name: "Standard",
    price: "$650",
    currency: "USD",
    description: "Full site with everything needed to convert visitors.",
    features: [
      "All Basic features",
      "Full 6-section site",
      "Digital menu / specials",
      "Gallery + Google reviews",
      "3 months maintenance",
    ],
    cta: "Select Standard",
    highlight: true,
  },
  {
    name: "Premium",
    price: "$1,100",
    currency: "USD",
    description: "Advanced features to build loyalty and drive bookings.",
    features: [
      "All Standard features",
      "Online reservation system",
      "Loyalty email capture",
      "12 months maintenance",
    ],
    cta: "Select Premium",
    highlight: false,
  },
]

function BudgetTab({ proposalHtml }: { proposalHtml?: string }) {
  if (proposalHtml) {
    return (
      <div
        className="prose prose-sm max-w-none"
        dangerouslySetInnerHTML={{ __html: proposalHtml }}
      />
    )
  }

  return (
    <div className="flex items-start gap-3">
      {BUDGET_TIERS.map((tier) => (
        <div
          key={tier.name}
          className={cn(
            "flex-1 rounded-xl border flex flex-col transition-all",
            tier.highlight
              ? "bg-folio-accent/[0.06] border-folio-accent/35 shadow-glow-accent scale-[1.03] origin-bottom"
              : "bg-folio-elevated border-folio-border/[0.08]"
          )}
        >
          <div className="p-4 flex-1">
            {tier.highlight ? (
              <div className="text-[10px] text-folio-accent font-semibold uppercase tracking-widest mb-2">
                ✦ Recommended
              </div>
            ) : (
              <div className="mb-5" />
            )}

            <div className="text-xs font-medium text-folio-text-muted mb-1">{tier.name}</div>
            <div className="flex items-baseline gap-1 mb-1">
              <span className={cn("text-2xl font-bold", tier.highlight ? "text-folio-accent" : "text-folio-text-primary")}>
                {tier.price}
              </span>
              <span className="text-xs text-folio-text-muted">{tier.currency}</span>
            </div>
            <p className="text-[11px] text-folio-text-muted leading-relaxed mb-4">{tier.description}</p>

            <ul className="space-y-1.5">
              {tier.features.map((item, i) => (
                <li key={i} className="flex items-start gap-2 text-xs text-folio-text-secondary">
                  <CheckCircle
                    size={11}
                    className={cn("mt-0.5 shrink-0", tier.highlight ? "text-folio-accent" : "text-emerald-400")}
                  />
                  <span className={i === 0 && tier.name !== "Basic" ? "font-medium text-folio-text-primary" : ""}>
                    {item}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          <div className="px-4 pb-4">
            <button
              className={cn(
                "w-full py-2 rounded-lg text-xs font-semibold transition-colors",
                tier.highlight
                  ? "bg-folio-accent text-white hover:bg-folio-accent/90"
                  : "bg-folio-elevated border border-folio-border/[0.1] text-folio-text-secondary hover:text-folio-text-primary hover:border-folio-border/[0.2]"
              )}
            >
              {tier.cta}
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}

// ─── Shared ───────────────────────────────────────────────────────────────────

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-xl bg-folio-elevated border border-folio-border/[0.08] p-4">
      <h3 className="text-xs font-semibold text-folio-text-secondary uppercase tracking-wider mb-3">{title}</h3>
      {children}
    </div>
  )
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-[10px] text-folio-text-muted mb-0.5">{label}</div>
      <div className="text-sm text-folio-text-primary font-medium">{value}</div>
    </div>
  )
}
