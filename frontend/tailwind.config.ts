import type { Config } from "tailwindcss"

const config: Config = {
  darkMode: "class",
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        folio: {
          // Adaptive tokens — resolved via CSS variables in globals.css
          base:    "rgb(var(--folio-base)    / <alpha-value>)",
          surface: "rgb(var(--folio-surface) / <alpha-value>)",
          elevated:"rgb(var(--folio-elevated)/ <alpha-value>)",
          border:  "rgb(var(--folio-border)  / <alpha-value>)",
          text: {
            primary:   "rgb(var(--folio-text-primary)   / <alpha-value>)",
            secondary: "rgb(var(--folio-text-secondary) / <alpha-value>)",
            muted:     "rgb(var(--folio-text-muted)     / <alpha-value>)",
          },
          // Brand accent — warm coral/terracotta (Anthropic-inspired)
          accent: "#D4704A",
          // Semantic lead scores — unchanged, functional
          hot:    "#F59E0B",
          warm:   "#3B82F6",
          cold:   "#6B7280",
        },
      },
      fontFamily: {
        sans:  ["var(--font-inter)",      "system-ui", "sans-serif"],
        serif: ["var(--font-fraunces)",   "Georgia",   "serif"],
        mono:  ["var(--font-mono)",       "Menlo",     "monospace"],
      },
      boxShadow: {
        "border-folio": "0 0 0 1px rgb(var(--folio-border) / 0.08)",
        "glow-hot":     "0 0 0 1px rgba(245,158,11,0.3), 0 4px 20px rgba(245,158,11,0.15)",
        "glow-warm":    "0 0 0 1px rgba(59,130,246,0.3),  0 4px 16px rgba(59,130,246,0.12)",
        "glow-accent":  "0 0 0 1px rgba(212,112,74,0.4),  0 4px 20px rgba(212,112,74,0.18)",
        "card":         "0 1px 3px rgba(0,0,0,0.08), 0 0 0 1px rgb(var(--folio-border) / 0.07)",
        // legacy alias kept for any untouched components
        "border-dark":  "0 0 0 1px rgba(255,255,255,0.08)",
      },
      keyframes: {
        fadeIn: { from: { opacity: "0", transform: "translateY(4px)" }, to: { opacity: "1", transform: "translateY(0)" } },
        pulse:  { "0%, 100%": { opacity: "1" }, "50%": { opacity: "0.4" } },
        blink:  { "0%, 100%": { opacity: "1" }, "50%": { opacity: "0" } },
      },
      animation: {
        "fade-in":    "fadeIn 0.2s ease-out",
        "pulse-slow": "pulse 2s ease-in-out infinite",
        "blink":      "blink 1s step-end infinite",
      },
    },
  },
  plugins: [],
}

export default config
