import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
import type { LeadVerdict, LeadStatus } from "@/types"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function verdictLabel(verdict: LeadVerdict) {
  return { HOT_LEAD: "HOT", WARM_LEAD: "WARM", COLD_LEAD: "COLD" }[verdict]
}

export function verdictColor(verdict: LeadVerdict) {
  return {
    HOT_LEAD: "text-folio-hot",
    WARM_LEAD: "text-folio-warm",
    COLD_LEAD: "text-folio-cold",
  }[verdict]
}

export function verdictBg(verdict: LeadVerdict) {
  return {
    HOT_LEAD: "bg-folio-hot/10 text-folio-hot border border-folio-hot/20",
    WARM_LEAD: "bg-folio-warm/10 text-folio-warm border border-folio-warm/20",
    COLD_LEAD: "bg-folio-cold/10 text-folio-cold border border-folio-cold/20",
  }[verdict]
}

export function verdictShadow(verdict: LeadVerdict) {
  return {
    HOT_LEAD: "shadow-glow-hot",
    WARM_LEAD: "shadow-glow-warm",
    COLD_LEAD: "shadow-border-dark",
  }[verdict]
}

export function statusLabel(status: LeadStatus) {
  const labels: Record<LeadStatus, string> = {
    pending: "Pending",
    researching: "Researching...",
    qualifying: "Qualifying...",
    awaiting_approval: "Awaiting approval",
    designing: "Designing...",
    proposing: "Building proposal...",
    complete: "Complete",
    discarded: "Discarded",
  }
  return labels[status]
}

export function relativeTime(iso: string) {
  const diff = Date.now() - new Date(iso).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 1) return "just now"
  if (mins < 60) return `${mins}m ago`
  return `${Math.floor(mins / 60)}h ago`
}

export function formatScore(score: number) {
  return score.toString()
}
