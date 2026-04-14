// ─── Lead pipeline types ────────────────────────────────────────────────────

export type SiteQuality = "none" | "outdated" | "poor" | "acceptable"
export type LeadVerdict = "HOT_LEAD" | "WARM_LEAD" | "COLD_LEAD"
export type LeadStatus =
  | "pending"
  | "researching"
  | "qualifying"
  | "awaiting_approval"
  | "designing"
  | "proposing"
  | "complete"
  | "discarded"

export interface LeadProfile {
  id: string
  name: string
  industry: string
  location: string
  description: string
  currentSiteUrl?: string
  currentSiteQuality: SiteQuality
  socialPresence: {
    instagram?: string
    facebook?: string
    googleMapsRating?: number
    googleMapsReviews?: number
  }
  painPoints: string[]
  brandSignals: {
    primaryColor?: string
    mood?: string
  }
}

export interface QualificationResult {
  score: number
  verdict: LeadVerdict
  reasons: string[]
  risks: string[]
  autoApproved: boolean
}

export interface Lead extends LeadProfile {
  status: LeadStatus
  qualification?: QualificationResult
  previewUrl?: string
  proposalHtml?: string
  createdAt: string
}

// ─── Campaign settings ───────────────────────────────────────────────────────

export interface CampaignSettings {
  targetIndustries: string[]
  location: { city: string; radiusKm: number }
  businessSize: ("micro" | "small" | "medium")[]
  budgetSignals: string[]
  negativeFilters: string[]
  autoApproveThreshold: number
}

// ─── Agent feed events ───────────────────────────────────────────────────────

export type AgentName = "management" | "research" | "qualification" | "design" | "proposal"
export type EventStatus = "start" | "progress" | "complete" | "error" | "checkpoint"

export interface AgentEvent {
  id: string
  agent: AgentName
  status: EventStatus
  message: string
  timestamp: string
  data?: Record<string, unknown>
}

// ─── Pipeline step ───────────────────────────────────────────────────────────

export type StepState = "pending" | "active" | "complete" | "error" | "skipped"

export interface PipelineStep {
  id: string
  label: string
  agent: AgentName
  state: StepState
}
