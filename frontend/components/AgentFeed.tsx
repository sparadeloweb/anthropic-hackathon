"use client"

import { useEffect, useRef } from "react"
import { cn } from "@/lib/utils"
import type { AgentEvent } from "@/types"

const AGENT_LABELS: Record<string, string> = {
  management: "MGT",
  research: "RES",
  qualification: "QUA",
  design: "DES",
  proposal: "PRO",
}

const AGENT_COLORS: Record<string, string> = {
  management: "text-folio-accent",
  research: "text-violet-400",
  qualification: "text-folio-warm",
  design: "text-emerald-400",
  proposal: "text-folio-hot",
}

const STATUS_PREFIXES: Record<string, string> = {
  start: "→",
  progress: "·",
  complete: "✓",
  error: "✗",
  checkpoint: "★",
}

interface AgentFeedProps {
  events: AgentEvent[]
  isLive?: boolean
}

export function AgentFeed({ events, isLive = false }: AgentFeedProps) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [events.length])

  return (
    <div className="bg-folio-elevated rounded-lg border border-folio-border/[0.08] overflow-hidden">
      <div className="flex items-center justify-between px-3 py-2 border-b border-folio-border/[0.08]">
        <span className="text-[10px] font-mono text-folio-text-muted uppercase tracking-widest">
          Agent Feed
        </span>
        {isLive ? (
          <span className="flex items-center gap-1.5 text-[10px] text-emerald-400 font-mono">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse-slow" />
            LIVE
          </span>
        ) : (
          <span className="text-[10px] text-folio-text-muted font-mono">
            {events.length} events
          </span>
        )}
      </div>

      <div className="h-64 overflow-y-auto p-3 space-y-1 font-mono text-xs">
        {events.length === 0 ? (
          <div className="flex items-center gap-2 text-folio-text-muted">
            <span className="animate-blink">▊</span>
            <span>Waiting for pipeline to start...</span>
          </div>
        ) : (
          events.map((event) => (
            <FeedLine key={event.id} event={event} />
          ))
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  )
}

interface FeedLineProps {
  event: AgentEvent
}

function FeedLine({ event }: FeedLineProps) {
  const agentColor = AGENT_COLORS[event.agent] ?? "text-folio-text-secondary"
  const prefix = STATUS_PREFIXES[event.status] ?? "·"
  const label = AGENT_LABELS[event.agent] ?? event.agent.toUpperCase()
  const time = new Date(event.timestamp).toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  })

  return (
    <div className={cn("flex gap-2 leading-relaxed animate-fade-in", statusColor(event.status))}>
      <span className="text-folio-text-muted shrink-0">{time}</span>
      <span className={cn("shrink-0 font-medium", agentColor)}>[{label}]</span>
      <span className="shrink-0">{prefix}</span>
      <span className="text-folio-text-secondary">{event.message}</span>
    </div>
  )
}

function statusColor(status: AgentEvent["status"]) {
  if (status === "error") return "text-red-400"
  if (status === "complete") return "text-emerald-400/80"
  if (status === "checkpoint") return "text-folio-hot"
  return ""
}
