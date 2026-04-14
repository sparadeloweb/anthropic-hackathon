"use client"

import Link from "next/link"
import { Navbar } from "@/components/Navbar"
import { ArrowRight } from "lucide-react"

const AGENTS = [
  {
    emoji: "🗺",
    name: "Discovery",
    model: "Haiku",
    desc: "Scans Google Maps for businesses in your target area that match your criteria.",
    color: "#A78BFA",
  },
  {
    emoji: "🔍",
    name: "Research",
    model: "Haiku",
    desc: "Visits each website, reads reviews, detects pain points and digital gaps.",
    color: "#60A5FA",
  },
  {
    emoji: "⚖️",
    name: "Qualification",
    model: "Haiku",
    desc: "Scores each lead 0–100. Auto-approves above your threshold, flags the rest.",
    color: "#34D399",
  },
  {
    emoji: "🎨",
    name: "Design",
    model: "Sonnet + Stitch",
    desc: "Generates a redesigned website for the business — a live, navigable preview.",
    color: "#D4704A",
  },
  {
    emoji: "📄",
    name: "Proposal",
    model: "Sonnet",
    desc: "Builds a tailored commercial proposal with 3 budget tiers, ready to send.",
    color: "#F59E0B",
  },
]

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-folio-base flex flex-col">
      <Navbar />

      <main className="flex-1 flex flex-col">
        {/* ── Hero ── */}
        <section className="flex-1 flex flex-col items-center justify-center text-center px-6 pt-20 pb-16">
          <div className="max-w-2xl mx-auto">
            <p className="text-xs font-mono uppercase tracking-widest text-folio-accent mb-6">
              For digital agencies
            </p>

            <h1 className="font-serif text-5xl md:text-6xl font-semibold text-folio-text-primary leading-tight mb-6">
              From Google Maps
              <br />
              <span className="text-folio-accent">to signed proposal,</span>
              <br />
              in minutes.
            </h1>

            <p className="text-lg text-folio-text-secondary leading-relaxed max-w-xl mx-auto mb-10">
              Folio runs a team of AI agents that find local businesses, identify
              the ones worth approaching, design a new site for them, and write
              the proposal — all before you finish your coffee.
            </p>

            <div className="flex items-center gap-3 justify-center">
              <Link
                href="/hunt"
                className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-folio-accent hover:bg-folio-accent/90 text-white font-semibold text-sm transition-all shadow-glow-accent"
              >
                Start a Hunt
                <ArrowRight size={15} />
              </Link>
              <Link
                href="/dashboard"
                className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-folio-elevated border border-folio-border/[0.1] text-folio-text-secondary hover:text-folio-text-primary text-sm font-medium transition-colors"
              >
                View dashboard
              </Link>
            </div>
          </div>
        </section>

        {/* ── Agent pipeline ── */}
        <section className="border-t border-folio-border/[0.08] bg-folio-surface px-6 py-14">
          <div className="max-w-4xl mx-auto">
            <p className="text-center text-xs font-mono uppercase tracking-widest text-folio-text-muted mb-10">
              Five agents, one seamless pipeline
            </p>

            <div className="grid grid-cols-1 md:grid-cols-5 gap-0">
              {AGENTS.map((agent, i) => (
                <div key={agent.name} className="flex md:flex-col items-start md:items-center gap-4 md:gap-3 relative">
                  {/* Connector */}
                  {i < AGENTS.length - 1 ? (
                    <div className="hidden md:block absolute top-5 left-[calc(50%+20px)] right-0 h-px border-t border-dashed border-folio-border/[0.15]" />
                  ) : null}

                  {/* Icon */}
                  <div
                    className="shrink-0 w-10 h-10 rounded-xl flex items-center justify-center text-xl relative z-10"
                    style={{ backgroundColor: agent.color + "20" }}
                  >
                    {agent.emoji}
                  </div>

                  {/* Text */}
                  <div className="md:text-center">
                    <div className="flex items-center gap-1.5 md:justify-center mb-0.5">
                      <span className="text-xs font-semibold text-folio-text-primary">{agent.name}</span>
                      <span
                        className="text-[10px] px-1.5 py-0.5 rounded-full font-mono"
                        style={{ backgroundColor: agent.color + "18", color: agent.color }}
                      >
                        {agent.model}
                      </span>
                    </div>
                    <p className="text-[11px] text-folio-text-muted leading-relaxed md:max-w-[130px]">
                      {agent.desc}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── Footer CTA ── */}
        <section className="border-t border-folio-border/[0.08] py-10 px-6 text-center">
          <p className="text-sm text-folio-text-muted mb-4">
            Human approval at every critical step. You stay in control.
          </p>
          <Link
            href="/hunt"
            className="inline-flex items-center gap-2 text-folio-accent hover:text-folio-accent/80 text-sm font-medium transition-colors"
          >
            Start your first Hunt <ArrowRight size={13} />
          </Link>
        </section>
      </main>
    </div>
  )
}
