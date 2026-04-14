"use client"

import Link from "next/link"
import { Star, Globe, Clock } from "lucide-react"
import { cn, verdictBg, verdictLabel, statusLabel, relativeTime } from "@/lib/utils"
import type { Lead } from "@/types"

interface LeadCardProps {
  lead: Lead
  onSelect?: (id: string) => void
  isSelected?: boolean
}

export function LeadCard({ lead, onSelect, isSelected }: LeadCardProps) {
  const isActive = ["researching", "qualifying", "designing", "proposing"].includes(lead.status)
  const isDiscarded = lead.status === "discarded"

  const cardClass = cn(
    "block rounded-xl p-4 transition-all duration-200 w-full text-left",
    isSelected
      ? "bg-folio-elevated ring-1 ring-folio-accent/30 shadow-glow-accent"
      : "bg-folio-surface hover:bg-folio-elevated",
    !isSelected && isActive && "shadow-glow-accent",
    !isSelected && !isActive && "shadow-card",
    isDiscarded && "opacity-40 hover:opacity-60"
  )

  const cardContent = (
    <div className="flex items-start gap-3">
      {/* Score badge */}
      {lead.qualification ? (
        <div className="shrink-0 mt-0.5">
          <div className={cn("w-10 h-10 rounded-lg flex items-center justify-center text-sm font-bold", scoreBackground(lead.qualification.score))}>
            {lead.qualification.score}
          </div>
        </div>
      ) : (
        <div className="shrink-0 mt-0.5 w-10 h-10 rounded-lg bg-folio-elevated border border-folio-border/[0.08] flex items-center justify-center">
          <div className="w-4 h-0.5 bg-folio-text-muted rounded animate-pulse-slow" />
        </div>
      )}

      {/* Content */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-0.5">
          <span className="text-sm font-semibold text-folio-text-primary truncate">{lead.name}</span>
          {lead.qualification ? (
            <span className={cn("text-[10px] font-semibold px-1.5 py-0.5 rounded-full shrink-0", verdictBg(lead.qualification.verdict))}>
              {verdictLabel(lead.qualification.verdict)}
            </span>
          ) : null}
        </div>

        <div className="flex items-center gap-3 text-xs text-folio-text-muted mb-2">
          <span>{lead.industry}</span>
          <span>·</span>
          <span className="truncate">{lead.location}</span>
        </div>

        <div className="flex items-center gap-3 text-[11px]">
          {lead.socialPresence.googleMapsRating ? (
            <span className="flex items-center gap-1 text-folio-text-secondary">
              <Star size={10} className="text-folio-hot fill-folio-hot" />
              {lead.socialPresence.googleMapsRating}
              <span className="text-folio-text-muted">({lead.socialPresence.googleMapsReviews})</span>
            </span>
          ) : null}

          {lead.currentSiteUrl ? (
            <span className="flex items-center gap-1 text-folio-text-muted">
              <Globe size={10} />
              {siteQualityLabel(lead.currentSiteQuality)}
            </span>
          ) : (
            <span className="text-red-400/70 flex items-center gap-1">
              <Globe size={10} />
              No website
            </span>
          )}

          <span className="flex items-center gap-1 text-folio-text-muted ml-auto">
            <Clock size={10} />
            {relativeTime(lead.createdAt)}
          </span>
        </div>
      </div>

      {/* Status */}
      <div className="shrink-0">
        <StatusPill status={lead.status} />
      </div>
    </div>
  )

  if (onSelect) {
    return (
      <button onClick={() => onSelect(lead.id)} className={cardClass}>
        {cardContent}
      </button>
    )
  }

  return (
    <Link href={`/dashboard/${lead.id}`} className={cardClass}>
      {cardContent}
    </Link>
  )
}

function StatusPill({ status }: { status: Lead["status"] }) {
  const isActive = ["researching", "qualifying", "designing", "proposing"].includes(status)

  return (
    <span
      className={cn(
        "text-[10px] px-2 py-0.5 rounded-full font-medium",
        isActive && "bg-folio-accent/10 text-folio-accent border border-folio-accent/20",
        status === "complete" && "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20",
        status === "awaiting_approval" && "bg-folio-hot/10 text-folio-hot border border-folio-hot/20",
        status === "discarded" && "bg-folio-elevated text-folio-text-muted border border-folio-border/[0.06]",
        status === "pending" && "bg-folio-elevated text-folio-text-muted border border-folio-border/[0.06]",
      )}
    >
      {isActive ? (
        <span className="flex items-center gap-1">
          <span className="w-1 h-1 rounded-full bg-folio-accent animate-pulse-slow" />
          {statusLabel(status)}
        </span>
      ) : (
        statusLabel(status)
      )}
    </span>
  )
}

function scoreBackground(score: number) {
  if (score >= 75) return "bg-folio-hot/15 text-folio-hot"
  if (score >= 50) return "bg-folio-warm/15 text-folio-warm"
  return "bg-folio-cold/15 text-folio-cold"
}

function siteQualityLabel(quality: Lead["currentSiteQuality"]) {
  const labels = {
    none: "No site",
    outdated: "Outdated",
    poor: "Poor",
    acceptable: "Acceptable",
  }
  return labels[quality]
}
