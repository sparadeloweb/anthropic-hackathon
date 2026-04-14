"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Navbar } from "@/components/Navbar"
import {
  Plus, X, Play, MapPin, Building2, Zap, Shield, Target,
  SlidersHorizontal, ChevronDown,
} from "lucide-react"
import { cn } from "@/lib/utils"

const INDUSTRY_OPTIONS = [
  "Restaurantes", "Cafeterías", "Bares", "Clínicas dentales",
  "Psicólogos", "Estudios de diseño", "Estudios de arquitectura",
  "Estudios contables", "Abogados", "Peluquerías", "Spas", "Gyms",
]

const BUDGET_SIGNALS = [
  "Premium zone", "Active advertising", "High reviews (4.5+)",
  "Recent renovations", "Staff > 5", "Multiple branches",
]

const NEGATIVE_FILTERS = [
  "Enterprise / franchise", "Government", "NGO",
  "Already has agency", "No website needed", "Closed / inactive",
]

const SIZE_OPTIONS = [
  { id: "micro", label: "Micro", desc: "1–5 people" },
  { id: "small", label: "Small", desc: "5–20 people" },
  { id: "medium", label: "Medium", desc: "20–50 people" },
]

const PIPELINE_STEPS = [
  { agent: "Discovery Agent", model: "Haiku", emoji: "🗺", color: "#A78BFA", desc: "Scans Google Maps for businesses matching your filters" },
  { agent: "Research Agent", model: "Haiku", emoji: "🔍", color: "#60A5FA", desc: "Scrapes current website, social presence, pain points" },
  { agent: "Qualification Agent", model: "Haiku", emoji: "⚖️", color: "#34D399", desc: "Scores 0–100, decides HOT/WARM/COLD. Auto-approves above threshold" },
  { agent: "Design Agent", model: "Sonnet + Stitch", emoji: "🎨", color: "#D4704A", desc: "Generates a redesigned site via Stitch MCP — live at /preview" },
  { agent: "Proposal Agent", model: "Sonnet", emoji: "📄", color: "#F59E0B", desc: "Builds a commercial proposal with 3 budget tiers" },
]

export default function NewHuntPage() {
  const router = useRouter()

  const [industries, setIndustries] = useState<string[]>(["Restaurantes", "Cafeterías"])
  const [city, setCity] = useState("Buenos Aires")
  const [radius, setRadius] = useState(10)
  const [sizes, setSizes] = useState<string[]>(["micro", "small"])
  const [budgetSignals, setBudgetSignals] = useState<string[]>(["Premium zone", "High reviews (4.5+)"])
  const [negativeFilters, setNegativeFilters] = useState<string[]>(["Enterprise / franchise"])
  const [threshold, setThreshold] = useState(65)
  const [previewOpen, setPreviewOpen] = useState(false)

  const estimatedCandidates = industries.length * 20 + radius * 2
  const estimatedHot = Math.round(estimatedCandidates * 0.15)
  const estimatedJobs = Math.round(estimatedHot * 0.7)

  function toggleItem(arr: string[], setArr: (v: string[]) => void, item: string) {
    setArr(arr.includes(item) ? arr.filter((x) => x !== item) : [...arr, item])
  }

  return (
    <div className="min-h-screen bg-folio-base flex flex-col">
      <Navbar />

      <div className="flex-1 max-w-3xl mx-auto w-full px-6 py-8 space-y-6">
        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="font-serif text-2xl font-semibold text-folio-text-primary">New Hunt</h1>
            <p className="text-sm text-folio-text-muted mt-1">
              Define your target — agents will find, score, and pitch leads automatically.
            </p>
          </div>
          <button
            onClick={() => router.push("/dashboard")}
            className="shrink-0 flex items-center gap-2 px-5 py-2.5 rounded-xl bg-folio-accent hover:bg-folio-accent/90 text-white font-semibold text-sm transition-all shadow-glow-accent"
          >
            <Play size={13} fill="white" />
            Launch Hunt
          </button>
        </div>

        {/* Form card */}
        <div className="bg-folio-surface border border-folio-border/[0.08] rounded-2xl shadow-card divide-y divide-folio-border/[0.06]">
          {/* Industries */}
          <Section icon={<Building2 size={13} />} title="Target industries">
            <div className="flex flex-wrap gap-1.5">
              {INDUSTRY_OPTIONS.map((ind) => (
                <Chip
                  key={ind}
                  label={ind}
                  active={industries.includes(ind)}
                  onToggle={() => toggleItem(industries, setIndustries, ind)}
                />
              ))}
            </div>
          </Section>

          {/* Location + Radius */}
          <Section icon={<MapPin size={13} />} title="Location">
            <div className="grid grid-cols-2 gap-6">
              <div>
                <label className="text-[11px] text-folio-text-muted mb-1.5 block">City or neighborhood</label>
                <input
                  type="text"
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  placeholder="Buenos Aires"
                />
              </div>
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="text-[11px] text-folio-text-muted">Search radius</label>
                  <span className="text-[11px] font-semibold text-folio-text-primary">{radius} km</span>
                </div>
                <input
                  type="range"
                  min={1}
                  max={50}
                  value={radius}
                  onChange={(e) => setRadius(Number(e.target.value))}
                  className="w-full mt-2"
                />
                <div className="flex justify-between text-[10px] text-folio-text-muted mt-1">
                  <span>1 km</span>
                  <span>50 km</span>
                </div>
              </div>
            </div>
          </Section>

          {/* Business size + Auto-approve */}
          <Section icon={<Target size={13} />} title="Target business size">
            <div className="grid grid-cols-2 gap-6">
              <div>
                <label className="text-[11px] text-folio-text-muted mb-2 block">Size range</label>
                <div className="grid grid-cols-3 gap-1.5">
                  {SIZE_OPTIONS.map((s) => (
                    <button
                      key={s.id}
                      onClick={() => toggleItem(sizes, setSizes, s.id)}
                      className={cn(
                        "rounded-lg border p-2 text-left transition-all",
                        sizes.includes(s.id)
                          ? "border-folio-accent/40 bg-folio-accent/10 text-folio-accent"
                          : "border-folio-border/[0.08] bg-folio-elevated text-folio-text-muted hover:border-folio-border/[0.18]"
                      )}
                    >
                      <div className="text-xs font-medium">{s.label}</div>
                      <div className="text-[10px] opacity-70">{s.desc}</div>
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="text-[11px] text-folio-text-muted flex items-center gap-1">
                    <SlidersHorizontal size={11} />
                    Auto-approve threshold
                  </label>
                  <span
                    className={cn(
                      "text-[11px] font-bold",
                      threshold >= 70 ? "text-folio-hot" : threshold >= 50 ? "text-folio-warm" : "text-folio-cold"
                    )}
                  >
                    {threshold}
                  </span>
                </div>
                <p className="text-[10px] text-folio-text-muted mb-2">
                  Leads above this score go straight to proposal without your review.
                </p>
                <input
                  type="range"
                  min={0}
                  max={100}
                  value={threshold}
                  onChange={(e) => setThreshold(Number(e.target.value))}
                  className="w-full"
                />
                <div className="flex justify-between text-[10px] text-folio-text-muted mt-1">
                  <span>Review all</span>
                  <span>Auto all</span>
                </div>
              </div>
            </div>
          </Section>

          {/* Budget signals */}
          <Section icon={<Zap size={13} />} title="Budget signals">
            <p className="text-[11px] text-folio-text-muted mb-2">
              Signals that suggest a business can afford good work.
            </p>
            <div className="flex flex-wrap gap-1.5">
              {BUDGET_SIGNALS.map((sig) => (
                <Chip
                  key={sig}
                  label={sig}
                  active={budgetSignals.includes(sig)}
                  onToggle={() => toggleItem(budgetSignals, setBudgetSignals, sig)}
                  variant="accent"
                />
              ))}
            </div>
          </Section>

          {/* Negative filters */}
          <Section icon={<Shield size={13} />} title="Exclude">
            <p className="text-[11px] text-folio-text-muted mb-2">
              Businesses that match these are skipped automatically.
            </p>
            <div className="flex flex-wrap gap-1.5">
              {NEGATIVE_FILTERS.map((f) => (
                <Chip
                  key={f}
                  label={f}
                  active={negativeFilters.includes(f)}
                  onToggle={() => toggleItem(negativeFilters, setNegativeFilters, f)}
                  variant="danger"
                />
              ))}
            </div>
          </Section>
        </div>

        {/* Pipeline preview accordion */}
        <div className="bg-folio-surface border border-folio-border/[0.08] rounded-2xl shadow-card overflow-hidden">
          <button
            onClick={() => setPreviewOpen((v) => !v)}
            className="w-full flex items-center gap-3 px-5 py-4 text-left hover:bg-folio-elevated/40 transition-colors"
          >
            <ChevronDown
              size={14}
              className={cn("text-folio-text-muted transition-transform duration-200", previewOpen && "rotate-180")}
            />
            <span className="text-sm font-medium text-folio-text-primary">What happens when you launch</span>
            <span className="ml-auto text-xs text-folio-text-muted">
              ~{estimatedCandidates} candidates · ~{estimatedHot} hot leads · ~{estimatedJobs} proposals
            </span>
          </button>

          <div className={cn("overflow-hidden transition-all duration-300", previewOpen ? "max-h-[600px]" : "max-h-0")}>
            <div className="px-5 pb-5 border-t border-folio-border/[0.06]">
              <div className="grid grid-cols-3 gap-4 py-4">
                <PipelineStat label="Candidates" value={`~${estimatedCandidates}`} sub="businesses found" />
                <PipelineStat label="HOT leads" value={`~${estimatedHot}`} sub="score ≥ 75" color="text-folio-hot" />
                <PipelineStat label="Proposals" value={`~${estimatedJobs}`} sub="above threshold" color="text-folio-accent" />
              </div>

              <p className="text-xs text-folio-text-muted mb-5 leading-relaxed bg-folio-elevated rounded-lg px-3 py-2.5 border border-folio-border/[0.06]">
                Based on <strong className="text-folio-text-secondary">{industries.length} industries</strong> in{" "}
                <strong className="text-folio-text-secondary">{city}</strong> within a{" "}
                <strong className="text-folio-text-secondary">{radius} km radius</strong>.
                Leads scoring above <strong className="text-folio-text-secondary">{threshold}</strong> skip the approval step.
              </p>

              <div className="space-y-2">
                {PIPELINE_STEPS.map((step, i) => (
                  <div key={step.agent} className="flex gap-3">
                    <div className="flex flex-col items-center shrink-0">
                      <div
                        className="w-7 h-7 rounded-lg flex items-center justify-center text-xs shrink-0"
                        style={{ backgroundColor: step.color + "20", color: step.color }}
                      >
                        {step.emoji}
                      </div>
                      {i < PIPELINE_STEPS.length - 1 ? (
                        <div className="w-px flex-1 bg-folio-border/[0.08] my-0.5" />
                      ) : null}
                    </div>
                    <div className="pb-2">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-semibold text-folio-text-primary">{step.agent}</span>
                        <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-folio-elevated text-folio-text-muted border border-folio-border/[0.06]">
                          {step.model}
                        </span>
                      </div>
                      <p className="text-xs text-folio-text-muted mt-0.5">{step.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

// ─── Sub-components ───────────────────────────────────────────────────────────

function Section({
  icon,
  title,
  children,
}: {
  icon: React.ReactNode
  title: string
  children: React.ReactNode
}) {
  return (
    <div className="p-5">
      <div className="flex items-center gap-2 mb-4">
        <div className="border-l-2 border-folio-accent pl-2.5 flex items-center gap-2">
          <span className="text-folio-text-muted">{icon}</span>
          <h2 className="text-xs font-semibold text-folio-text-secondary uppercase tracking-wider">{title}</h2>
        </div>
      </div>
      {children}
    </div>
  )
}

interface ChipProps {
  label: string
  active: boolean
  onToggle: () => void
  variant?: "default" | "accent" | "danger"
}

function Chip({ label, active, onToggle, variant = "default" }: ChipProps) {
  const activeStyles = {
    default: "bg-folio-elevated border-folio-border/[0.2] text-folio-text-primary",
    accent:  "bg-folio-accent/15 border-folio-accent/30 text-folio-accent",
    danger:  "bg-red-500/10 border-red-500/30 text-red-400",
  }

  return (
    <button
      onClick={onToggle}
      className={cn(
        "flex items-center gap-1 px-2.5 py-1 rounded-full border text-[11px] font-medium transition-all",
        active
          ? activeStyles[variant]
          : "bg-transparent border-folio-border/[0.08] text-folio-text-muted hover:border-folio-border/[0.18] hover:text-folio-text-secondary"
      )}
    >
      {active ? <X size={9} /> : <Plus size={9} />}
      {label}
    </button>
  )
}

function PipelineStat({
  label,
  value,
  sub,
  color = "text-folio-text-primary",
}: {
  label: string
  value: string
  sub: string
  color?: string
}) {
  return (
    <div className="text-center">
      <div className={cn("text-2xl font-bold mb-0.5", color)}>{value}</div>
      <div className="text-xs font-medium text-folio-text-secondary">{label}</div>
      <div className="text-[10px] text-folio-text-muted">{sub}</div>
    </div>
  )
}
