"use client"

import { CheckCircle, XCircle, AlertTriangle, TrendingUp, AlertOctagon } from "lucide-react"
import { cn, verdictBg, verdictLabel } from "@/lib/utils"
import type { Lead } from "@/types"

interface QualificationCardProps {
  lead: Lead
  onApprove: () => void
  onDiscard: () => void
}

export function QualificationCard({ lead, onApprove, onDiscard }: QualificationCardProps) {
  const q = lead.qualification
  if (!q) return null

  const isHot = q.verdict === "HOT_LEAD"

  return (
    <div
      className={cn(
        "rounded-xl border p-5 space-y-4",
        isHot
          ? "bg-folio-hot/[0.05] border-folio-hot/30 shadow-glow-hot"
          : "bg-folio-surface border-folio-border/[0.1] shadow-card"
      )}
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <AlertOctagon size={15} className={isHot ? "text-folio-hot" : "text-folio-warm"} />
          <span className="text-xs font-semibold text-folio-text-primary uppercase tracking-wide">
            Human Checkpoint
          </span>
        </div>
        <span className={cn("text-xs font-bold px-2 py-0.5 rounded-full", verdictBg(q.verdict))}>
          {verdictLabel(q.verdict)} · {q.score}/100
        </span>
      </div>

      {/* Score bar */}
      <div>
        <div className="flex justify-between text-[10px] text-folio-text-muted mb-1.5">
          <span>Lead score</span>
          <span className={cn(isHot ? "text-folio-hot" : "text-folio-warm", "font-semibold")}>
            {q.score}/100
          </span>
        </div>
        <div className="h-1.5 rounded-full bg-folio-border/[0.08] overflow-hidden">
          <div
            className={cn(
              "h-full rounded-full transition-all duration-700",
              isHot ? "bg-folio-hot" : "bg-folio-warm"
            )}
            style={{ width: `${q.score}%` }}
          />
        </div>
      </div>

      {/* Reasons */}
      <div className="space-y-1.5">
        {q.reasons.map((reason, i) => (
          <div key={i} className="flex items-start gap-2 text-xs text-folio-text-secondary">
            <TrendingUp size={11} className="text-emerald-400 mt-0.5 shrink-0" />
            <span>{reason}</span>
          </div>
        ))}
      </div>

      {/* Risks */}
      {q.risks.length > 0 ? (
        <div className="space-y-1.5 pt-1 border-t border-folio-border/[0.08]">
          {q.risks.map((risk, i) => (
            <div key={i} className="flex items-start gap-2 text-xs text-folio-text-muted">
              <AlertTriangle size={11} className="text-folio-hot/60 mt-0.5 shrink-0" />
              <span>{risk}</span>
            </div>
          ))}
        </div>
      ) : null}

      {/* Actions */}
      <div className="flex gap-2 pt-1">
        <button
          onClick={onApprove}
          className="flex-1 flex items-center justify-center gap-1.5 py-2 px-4 rounded-lg bg-folio-accent hover:bg-folio-accent/90 text-white text-xs font-semibold transition-colors shadow-glow-accent"
        >
          <CheckCircle size={13} />
          Approve & continue
        </button>
        <button
          onClick={onDiscard}
          className="flex items-center justify-center gap-1.5 py-2 px-3 rounded-lg bg-folio-elevated hover:bg-red-500/10 text-folio-text-secondary hover:text-red-400 text-xs font-medium transition-colors border border-folio-border/[0.08] hover:border-red-500/20"
        >
          <XCircle size={13} />
          Discard
        </button>
      </div>
    </div>
  )
}
