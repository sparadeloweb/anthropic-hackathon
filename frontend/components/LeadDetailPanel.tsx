"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { AgentFeed } from "@/components/AgentFeed"
import { StepIndicator } from "@/components/StepIndicator"
import { QualificationCard } from "@/components/QualificationCard"
import { SitePreview } from "@/components/SitePreview"
import { ProposalTabs } from "@/components/ProposalTabs"
import { UIKitTab } from "@/components/UIKitTab"
import { MOCK_LEADS, MOCK_EVENTS_001, MOCK_STEPS_001 } from "@/lib/mock-data"
import { cn, verdictBg, verdictLabel } from "@/lib/utils"
import { ArrowLeft, Star, Globe, ExternalLink, Zap, MonitorPlay } from "lucide-react"
import type { LeadStatus, PipelineStep } from "@/types"

type MainTab = "proposal" | "website" | "uikit"

const MAIN_TABS: { id: MainTab; label: string }[] = [
  { id: "proposal", label: "Proposal" },
  { id: "website", label: "Website" },
  { id: "uikit", label: "UI Kit" },
]

interface LeadDetailPanelProps {
  leadId: string
  showBackButton?: boolean
  onBack?: () => void
}

export function LeadDetailPanel({ leadId, showBackButton = false, onBack }: LeadDetailPanelProps) {
  const router = useRouter()
  const [activeTab, setActiveTab] = useState<MainTab>("proposal")
  const [approved, setApproved] = useState(false)

  const lead = MOCK_LEADS.find((l) => l.id === leadId) ?? MOCK_LEADS[0]
  const events = leadId === "lead-001" ? MOCK_EVENTS_001 : []
  const steps = leadId === "lead-001" ? MOCK_STEPS_001 : buildStepsFromStatus(lead.status)

  const showCheckpoint = lead.status === "awaiting_approval" && !approved
  const isLive = ["researching", "qualifying", "designing", "proposing"].includes(lead.status)

  function handleBack() {
    if (onBack) onBack()
    else router.push("/dashboard")
  }

  function handleDiscard() {
    if (onBack) onBack()
    else router.push("/dashboard")
  }

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Sub-header */}
      <div className="flex items-center gap-3 px-5 py-3 border-b border-folio-border/[0.08] bg-folio-surface/60 shrink-0">
        {showBackButton ? (
          <button
            onClick={handleBack}
            className="text-folio-text-muted hover:text-folio-text-secondary transition-colors"
          >
            <ArrowLeft size={16} />
          </button>
        ) : null}

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h2 className="text-sm font-semibold text-folio-text-primary truncate">{lead.name}</h2>
            {lead.qualification ? (
              <span className={cn("text-[10px] font-bold px-1.5 py-0.5 rounded-full shrink-0", verdictBg(lead.qualification.verdict))}>
                {verdictLabel(lead.qualification.verdict)} · {lead.qualification.score}
              </span>
            ) : null}
          </div>
          <div className="flex items-center gap-2 text-xs text-folio-text-muted flex-wrap mt-0.5">
            <span>{lead.industry}</span>
            <span className="text-folio-border/30">·</span>
            <span className="truncate max-w-[120px]">{lead.location}</span>
            {lead.socialPresence.googleMapsRating ? (
              <>
                <span className="text-folio-border/30">·</span>
                <span className="flex items-center gap-0.5">
                  <Star size={9} className="text-folio-hot fill-folio-hot" />
                  {lead.socialPresence.googleMapsRating}
                  <span className="text-folio-text-muted/60">({lead.socialPresence.googleMapsReviews})</span>
                </span>
              </>
            ) : null}
            {lead.currentSiteUrl ? (
              <>
                <span className="text-folio-border/30">·</span>
                <a
                  href={lead.currentSiteUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="flex items-center gap-0.5 hover:text-folio-accent transition-colors"
                >
                  <Globe size={9} />
                  {lead.currentSiteQuality}
                </a>
              </>
            ) : (
              <>
                <span className="text-folio-border/30">·</span>
                <span className="flex items-center gap-0.5 text-red-400/70">
                  <Globe size={9} />
                  No site
                </span>
              </>
            )}
          </div>
        </div>

        {lead.previewUrl ? (
          <a
            href={`/client/${lead.id}`}
            target="_blank"
            rel="noreferrer"
            className="shrink-0 flex items-center gap-1 text-xs text-folio-text-muted hover:text-folio-accent transition-colors"
          >
            <ExternalLink size={11} />
            <span className="hidden sm:inline">Client view</span>
          </a>
        ) : null}
      </div>

      {/* Main content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left panel */}
        <div className="w-72 shrink-0 border-r border-folio-border/[0.08] flex flex-col gap-3 p-4 overflow-y-auto">
          {/* Pipeline steps */}
          <div className="bg-folio-elevated rounded-xl border border-folio-border/[0.08] p-4">
            <p className="text-[10px] text-folio-text-muted uppercase tracking-widest font-mono mb-3">
              Pipeline
            </p>
            <StepIndicator steps={steps} />
          </div>

          {/* Qualification checkpoint — most prominent when visible */}
          {showCheckpoint ? (
            <QualificationCard
              lead={lead}
              onApprove={() => setApproved(true)}
              onDiscard={handleDiscard}
            />
          ) : null}

          {/* Agent feed */}
          <AgentFeed events={events} isLive={isLive} />
        </div>

        {/* Right panel */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Tab bar */}
          <div className="flex items-center gap-1 px-4 py-2.5 border-b border-folio-border/[0.08] shrink-0">
            {MAIN_TABS
              .filter((tab) => showBackButton || tab.id === "proposal")
              .map((tab) => (
                <MainTabBtn
                  key={tab.id}
                  tab={tab}
                  active={activeTab === tab.id}
                  disabled={tab.id !== "proposal" && !lead.previewUrl}
                  onClick={() => setActiveTab(tab.id)}
                />
              ))}
          </div>

          {/* Tab content */}
          <div className="flex-1 overflow-y-auto p-5">
            {activeTab === "proposal" ? (
              <>
                <ProposalTabs lead={lead} onApprove={() => setApproved(true)} />
                {/* Site preview CTA — shown below proposal when preview is ready */}
                {lead.previewUrl && !showBackButton ? (
                  <div className="mt-5 rounded-xl border border-folio-border/[0.08] bg-folio-elevated overflow-hidden">
                    <div className="flex items-center justify-between px-4 py-3">
                      <div className="flex items-center gap-2">
                        <MonitorPlay size={14} className="text-folio-accent" />
                        <span className="text-sm font-medium text-folio-text-primary">Generated site ready</span>
                      </div>
                      <a
                        href={`/dashboard/${lead.id}`}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-folio-accent hover:bg-folio-accent/90 text-white text-xs font-semibold transition-colors"
                      >
                        Open full view
                        <ExternalLink size={10} />
                      </a>
                    </div>
                    <div className="h-32 overflow-hidden opacity-60 hover:opacity-80 transition-opacity">
                      <SitePreview previewUrl={lead.previewUrl} leadName={lead.name} />
                    </div>
                  </div>
                ) : null}
              </>
            ) : null}
            {activeTab === "website" ? (
              lead.previewUrl ? (
                <div className="h-full">
                  <SitePreview previewUrl={lead.previewUrl} leadName={lead.name} />
                </div>
              ) : (
                <PendingState icon={<Zap size={18} />} message="Website will appear here once the Design Agent completes" />
              )
            ) : null}
            {activeTab === "uikit" ? (
              lead.previewUrl ? (
                <UIKitTab />
              ) : (
                <PendingState icon={<Zap size={18} />} message="UI Kit will be extracted after site generation" />
              )
            ) : null}
          </div>
        </div>
      </div>
    </div>
  )
}

// ─── Sub-components ───────────────────────────────────────────────────────────

interface MainTabBtnProps {
  tab: { id: MainTab; label: string }
  active: boolean
  disabled: boolean
  onClick: () => void
}

function MainTabBtn({ tab, active, disabled, onClick }: MainTabBtnProps) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={cn(
        "px-3.5 py-1.5 rounded-lg text-sm font-medium transition-colors",
        active
          ? "bg-folio-elevated text-folio-text-primary border border-folio-border/[0.1]"
          : disabled
            ? "text-folio-text-muted/30 cursor-not-allowed"
            : "text-folio-text-muted hover:text-folio-text-secondary hover:bg-folio-elevated/60"
      )}
    >
      {tab.label}
    </button>
  )
}

function PendingState({ icon, message }: { icon: React.ReactNode; message: string }) {
  return (
    <div className="flex flex-col items-center justify-center h-48 gap-3 text-center">
      <div className="w-10 h-10 rounded-full bg-folio-elevated border border-folio-border/[0.08] flex items-center justify-center text-folio-text-muted">
        {icon}
      </div>
      <p className="text-sm text-folio-text-muted max-w-[240px]">{message}</p>
    </div>
  )
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function buildStepsFromStatus(status: LeadStatus): PipelineStep[] {
  const allSteps: PipelineStep[] = [
    { id: "research", label: "Research", agent: "research", state: "pending" },
    { id: "qualify", label: "Qualify", agent: "qualification", state: "pending" },
    { id: "design", label: "Design", agent: "design", state: "pending" },
    { id: "proposal", label: "Proposal", agent: "proposal", state: "pending" },
  ]

  const statusOrder: Record<LeadStatus, number> = {
    pending: -1,
    researching: 0,
    qualifying: 1,
    awaiting_approval: 1,
    designing: 2,
    proposing: 3,
    complete: 4,
    discarded: -1,
  }

  const currentIdx = statusOrder[status] ?? -1

  return allSteps.map((step, i) => ({
    ...step,
    state: i < currentIdx ? "complete" : i === currentIdx ? "active" : "pending",
  }))
}
