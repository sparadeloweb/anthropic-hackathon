"use client"

import { Check, AlertCircle } from "lucide-react"
import { cn } from "@/lib/utils"
import type { PipelineStep } from "@/types"

const AGENT_COLORS: Record<string, string> = {
  management: "bg-folio-accent",
  research: "bg-violet-400",
  qualification: "bg-folio-warm",
  design: "bg-emerald-400",
  proposal: "bg-folio-hot",
}

interface StepIndicatorProps {
  steps: PipelineStep[]
}

export function StepIndicator({ steps }: StepIndicatorProps) {
  return (
    <div className="flex items-center gap-0">
      {steps.map((step, i) => (
        <StepItem
          key={step.id}
          step={step}
          isLast={i === steps.length - 1}
          index={i}
        />
      ))}
    </div>
  )
}

interface StepItemProps {
  step: PipelineStep
  isLast: boolean
  index: number
}

function StepItem({ step, isLast }: StepItemProps) {
  const color = AGENT_COLORS[step.agent] ?? "bg-folio-accent"

  return (
    <div className="flex items-center">
      <div className="flex flex-col items-center gap-1.5">
        <StepDot state={step.state} color={color} />
        <span
          className={cn(
            "text-[10px] font-medium whitespace-nowrap",
            step.state === "active"
              ? "text-folio-text-primary"
              : step.state === "complete"
                ? "text-folio-text-secondary"
                : "text-folio-text-muted"
          )}
        >
          {step.label}
        </span>
      </div>

      {isLast ? null : (
        <div
          className={cn(
            "h-px w-8 mx-1 mb-4 transition-colors",
            step.state === "complete"
              ? "bg-folio-border/[0.2]"
              : "bg-folio-border/[0.08]"
          )}
        />
      )}
    </div>
  )
}

interface StepDotProps {
  state: PipelineStep["state"]
  color: string
}

function StepDot({ state, color }: StepDotProps) {
  if (state === "complete") {
    return (
      <div className={cn("w-6 h-6 rounded-full flex items-center justify-center", color)}>
        <Check size={11} className="text-white" strokeWidth={2.5} />
      </div>
    )
  }

  if (state === "active") {
    return (
      <div className={cn("w-6 h-6 rounded-full flex items-center justify-center relative", color)}>
        <div className={cn("absolute inset-0 rounded-full animate-ping opacity-30", color)} />
        <div className="w-2 h-2 rounded-full bg-white" />
      </div>
    )
  }

  if (state === "error") {
    return (
      <div className="w-6 h-6 rounded-full bg-red-500/20 border border-red-500/40 flex items-center justify-center">
        <AlertCircle size={11} className="text-red-400" />
      </div>
    )
  }

  // pending / skipped
  return (
    <div className="w-6 h-6 rounded-full bg-folio-elevated border border-folio-border/[0.1] flex items-center justify-center">
      <div className="w-1.5 h-1.5 rounded-full bg-folio-text-muted" />
    </div>
  )
}
