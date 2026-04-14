"use client"

import { useState } from "react"
import { Navbar } from "@/components/Navbar"
import { LeadCard } from "@/components/LeadCard"
import { LeadDetailPanel } from "@/components/LeadDetailPanel"
import { MOCK_LEADS } from "@/lib/mock-data"
import { cn } from "@/lib/utils"
import { Play, Pause, Search, Zap, TrendingUp, Clock, CheckCircle2 } from "lucide-react"
import type { LeadVerdict, LeadStatus } from "@/types"

type FilterTab = "all" | LeadVerdict | "awaiting_approval"

const FILTER_TABS: { id: FilterTab; label: string }[] = [
  { id: "all",              label: "All" },
  { id: "HOT_LEAD",         label: "🔥 Hot" },
  { id: "WARM_LEAD",        label: "Warm" },
  { id: "COLD_LEAD",        label: "Cold" },
  { id: "awaiting_approval", label: "Review" },
]

const ACTIVE_STATUSES = new Set<LeadStatus>([
  "researching", "qualifying", "designing", "proposing",
])

export default function DashboardPage() {
  const [filter, setFilter] = useState<FilterTab>("all")
  const [running, setRunning] = useState(true)
  const [selectedLeadId, setSelectedLeadId] = useState<string | null>(null)
  const [search, setSearch] = useState("")

  const activeCount   = MOCK_LEADS.filter((l) => ACTIVE_STATUSES.has(l.status)).length
  const completeCount = MOCK_LEADS.filter((l) => l.status === "complete").length

  const counts: Record<FilterTab, number> = {
    all:               MOCK_LEADS.length,
    HOT_LEAD:          MOCK_LEADS.filter((l) => l.qualification?.verdict === "HOT_LEAD").length,
    WARM_LEAD:         MOCK_LEADS.filter((l) => l.qualification?.verdict === "WARM_LEAD").length,
    COLD_LEAD:         MOCK_LEADS.filter((l) => l.qualification?.verdict === "COLD_LEAD").length,
    awaiting_approval: MOCK_LEADS.filter((l) => l.status === "awaiting_approval").length,
  }

  const needsReviewCount = counts.awaiting_approval

  const filtered = MOCK_LEADS.filter((lead) => {
    const matchesFilter =
      filter === "all" ? true :
      filter === "awaiting_approval" ? lead.status === "awaiting_approval" :
      lead.qualification?.verdict === filter
    const matchesSearch =
      search === "" || lead.name.toLowerCase().includes(search.toLowerCase())
    return matchesFilter && matchesSearch
  })

  return (
    <div className="h-screen bg-folio-base flex flex-col overflow-hidden">
      <Navbar />

      {/* ── Stats bar (full width) ── */}
      <div className="shrink-0 border-b border-folio-border/[0.08] bg-folio-surface">
        <div className="flex items-stretch divide-x divide-folio-border/[0.06]">
          <StatCard
            icon={<TrendingUp size={14} />}
            label="Total leads"
            value={MOCK_LEADS.length}
            sub="in this hunt"
          />
          <StatCard
            icon={<span className="text-sm">🔥</span>}
            label="Hot leads"
            value={counts.HOT_LEAD}
            sub="score ≥ 75"
            valueColor="text-folio-hot"
          />
          <StatCard
            icon={<Clock size={14} />}
            label="Needs review"
            value={needsReviewCount}
            sub="awaiting approval"
            valueColor={needsReviewCount > 0 ? "text-folio-hot" : undefined}
            pulse={needsReviewCount > 0}
          />
          <StatCard
            icon={<Zap size={14} />}
            label="Active agents"
            value={activeCount}
            sub="running now"
            valueColor={activeCount > 0 ? "text-folio-accent" : undefined}
            pulse={activeCount > 0}
          />
          <StatCard
            icon={<CheckCircle2 size={14} />}
            label="Complete"
            value={completeCount}
            sub="proposals ready"
            valueColor="text-emerald-500"
          />
          {/* Run control */}
          <div className="flex items-center px-6 gap-3 ml-auto shrink-0">
            <div className="text-right">
              <div className="text-xs font-semibold text-folio-text-primary">Restaurantes · Palermo</div>
              <div className="text-[10px] text-folio-text-muted">Buenos Aires · 10 km radius</div>
            </div>
            <button
              onClick={() => setRunning((r) => !r)}
              className={cn(
                "flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-semibold transition-colors border",
                running
                  ? "bg-folio-hot/10 border-folio-hot/20 text-folio-hot hover:bg-folio-hot/15"
                  : "bg-folio-elevated border-folio-border/[0.08] text-folio-text-secondary"
              )}
            >
              {running ? <><Pause size={11} />Pause</> : <><Play size={11} />Resume</>}
            </button>
          </div>
        </div>
      </div>

      {/* ── Split layout ── */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left: lead list */}
        <div className="w-[360px] shrink-0 border-r border-folio-border/[0.08] flex flex-col overflow-hidden">
          {/* Search */}
          <div className="px-3 py-2 border-b border-folio-border/[0.08] shrink-0">
            <div className="relative">
              <Search size={12} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-folio-text-muted pointer-events-none" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search leads…"
                className="w-full pl-7 pr-3 py-1.5 text-xs bg-folio-elevated border border-folio-border/[0.08] rounded-lg text-folio-text-primary placeholder:text-folio-text-muted focus:outline-none focus:border-folio-accent/40 transition-colors"
              />
            </div>
          </div>

          {/* Filter tabs */}
          <div className="flex items-center gap-0.5 px-3 py-1.5 border-b border-folio-border/[0.08] shrink-0">
            {FILTER_TABS.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setFilter(tab.id)}
                className={cn(
                  "flex items-center gap-1 px-2.5 py-1 rounded-md text-[11px] font-medium transition-colors whitespace-nowrap",
                  filter === tab.id
                    ? "bg-folio-elevated text-folio-text-primary"
                    : "text-folio-text-muted hover:text-folio-text-secondary"
                )}
              >
                {tab.id === "awaiting_approval" && needsReviewCount > 0 ? (
                  <span className="w-1.5 h-1.5 rounded-full bg-folio-hot animate-pulse-slow shrink-0" />
                ) : null}
                {tab.label}
                <span className={cn(
                  "text-[10px] px-1 rounded-full",
                  filter === tab.id ? "bg-folio-accent/20 text-folio-accent" : "text-folio-text-muted/60"
                )}>
                  {counts[tab.id]}
                </span>
              </button>
            ))}
          </div>

          {/* Lead list */}
          <div className="flex-1 overflow-y-auto p-3 space-y-2">
            {filtered.length === 0 ? (
              <div className="text-center py-10 text-folio-text-muted text-sm">No leads found</div>
            ) : (
              filtered.map((lead) => (
                <LeadCard
                  key={lead.id}
                  lead={lead}
                  onSelect={setSelectedLeadId}
                  isSelected={lead.id === selectedLeadId}
                />
              ))
            )}
          </div>
        </div>

        {/* Right: detail */}
        <div className="flex-1 overflow-hidden">
          {selectedLeadId ? (
            <LeadDetailPanel leadId={selectedLeadId} />
          ) : (
            <NothingSelected />
          )}
        </div>
      </div>
    </div>
  )
}

// ─── Sub-components ───────────────────────────────────────────────────────────

function StatCard({
  icon,
  label,
  value,
  sub,
  valueColor = "text-folio-text-primary",
  pulse = false,
}: {
  icon: React.ReactNode
  label: string
  value: number
  sub: string
  valueColor?: string
  pulse?: boolean
}) {
  return (
    <div className="flex items-center gap-4 px-6 py-4 flex-1 min-w-0">
      <div className="text-folio-text-muted shrink-0">{icon}</div>
      <div>
        <div className="flex items-baseline gap-1.5">
          <span className={cn("text-2xl font-bold tabular-nums leading-none", valueColor)}>{value}</span>
          {pulse ? (
            <span className={cn("w-1.5 h-1.5 rounded-full animate-pulse-slow shrink-0", valueColor?.replace("text-", "bg-"))} />
          ) : null}
        </div>
        <div className="text-xs font-medium text-folio-text-secondary mt-0.5">{label}</div>
        <div className="text-[10px] text-folio-text-muted">{sub}</div>
      </div>
    </div>
  )
}

function NothingSelected() {
  return (
    <div className="h-full flex flex-col items-center justify-center gap-4 text-center p-8">
      <div className="w-14 h-14 rounded-2xl bg-folio-elevated border border-folio-border/[0.08] flex items-center justify-center">
        <span className="text-2xl">🎯</span>
      </div>
      <div>
        <p className="font-serif text-base font-medium text-folio-text-secondary">Select a lead</p>
        <p className="text-xs text-folio-text-muted mt-1 max-w-[200px]">
          Click any lead to view the pipeline, generated site, and proposal
        </p>
      </div>
    </div>
  )
}
