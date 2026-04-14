"use client"

import { Copy, Check } from "lucide-react"
import { useState } from "react"
import { cn } from "@/lib/utils"

// Demo UI Kit — extracted from generated Stitch output
const UI_KIT = {
  colors: [
    { name: "Primary", hex: "#C2410C", usage: "CTAs, headings accent" },
    { name: "Background", hex: "#FFFAF5", usage: "Page background" },
    { name: "Dark Hero", hex: "#1A1108", usage: "Hero section bg" },
    { name: "Cream", hex: "#FEF3C7", usage: "Cards, highlights" },
    { name: "Accent", hex: "#D97706", usage: "Icons, details" },
    { name: "Text", hex: "#292524", usage: "Body text" },
  ],
  typography: [
    { name: "Heading", family: "Playfair Display", weight: "700", size: "48px / 36px / 28px" },
    { name: "Subheading", family: "Playfair Display", weight: "400 italic", size: "24px" },
    { name: "Body", family: "Inter", weight: "400", size: "16px · 1.6 line-height" },
    { name: "UI / Labels", family: "Inter", weight: "500", size: "12-14px" },
  ],
  components: [
    { name: "Primary Button", preview: "Reservar mesa", style: "bg-[#C2410C] text-white px-6 py-3 rounded-lg font-semibold" },
    { name: "Ghost Button", preview: "Ver menú", style: "border border-[#C2410C] text-[#C2410C] px-6 py-3 rounded-lg font-medium" },
    { name: "Card", preview: "Dish card", style: "bg-white rounded-xl p-4 shadow-md" },
  ],
}

export function UIKitTab() {
  return (
    <div className="space-y-5">
      <ColorsSection />
      <TypographySection />
      <ComponentsSection />
      <ExportSection />
    </div>
  )
}

function ColorsSection() {
  return (
    <div>
      <SectionHeader title="Color palette" subtitle="Extracted from generated site" />
      <div className="grid grid-cols-3 gap-2">
        {UI_KIT.colors.map((color) => (
          <ColorChip key={color.name} color={color} />
        ))}
      </div>
    </div>
  )
}

function ColorChip({ color }: { color: (typeof UI_KIT.colors)[0] }) {
  const [copied, setCopied] = useState(false)

  function copy() {
    navigator.clipboard.writeText(color.hex)
    setCopied(true)
    setTimeout(() => setCopied(false), 1500)
  }

  return (
    <button
      onClick={copy}
      className="group rounded-lg overflow-hidden bg-folio-elevated border border-white/[0.06] hover:border-white/[0.12] transition-all text-left"
    >
      <div className="h-10 w-full" style={{ backgroundColor: color.hex }} />
      <div className="p-2">
        <div className="flex items-center justify-between">
          <span className="text-[11px] font-medium text-folio-text-primary">{color.name}</span>
          {copied ? (
            <Check size={10} className="text-emerald-400" />
          ) : (
            <Copy size={10} className="text-folio-text-muted opacity-0 group-hover:opacity-100 transition-opacity" />
          )}
        </div>
        <div className="text-[10px] text-folio-text-muted font-mono">{color.hex}</div>
        <div className="text-[9px] text-folio-text-muted mt-0.5">{color.usage}</div>
      </div>
    </button>
  )
}

function TypographySection() {
  return (
    <div>
      <SectionHeader title="Typography" subtitle="Font stack used in generated site" />
      <div className="rounded-xl bg-folio-elevated border border-white/[0.06] divide-y divide-white/[0.04]">
        {UI_KIT.typography.map((type) => (
          <div key={type.name} className="flex items-center gap-4 px-4 py-3">
            <div className="w-20 shrink-0">
              <div className="text-[10px] text-folio-text-muted">{type.name}</div>
            </div>
            <div className="flex-1">
              <div className="text-sm text-folio-text-primary font-medium">{type.family}</div>
              <div className="text-[10px] text-folio-text-muted">{type.weight} · {type.size}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function ComponentsSection() {
  return (
    <div>
      <SectionHeader title="Components" subtitle="Key UI elements from the generated site" />
      <div className="space-y-3">
        {UI_KIT.components.map((comp) => (
          <div key={comp.name} className="rounded-xl bg-folio-elevated border border-white/[0.06] p-4">
            <div className="text-[10px] text-folio-text-muted mb-3">{comp.name}</div>
            <div className="flex items-center justify-center bg-white/[0.03] rounded-lg py-4 px-6">
              <span
                className={cn(comp.style, "text-sm")}
                style={{ fontFamily: "Georgia, serif" }}
              >
                {comp.preview}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function ExportSection() {
  return (
    <div className="rounded-xl bg-folio-accent/[0.06] border border-folio-accent/20 p-4">
      <div className="text-xs font-semibold text-folio-accent mb-1">Export design tokens</div>
      <p className="text-xs text-folio-text-muted mb-3">
        Download this palette and type scale as a Tailwind config or CSS variables file.
      </p>
      <div className="flex gap-2">
        <button className="px-3 py-1.5 rounded-lg bg-folio-elevated border border-white/[0.08] text-xs text-folio-text-secondary hover:text-folio-text-primary transition-colors">
          tailwind.config.ts
        </button>
        <button className="px-3 py-1.5 rounded-lg bg-folio-elevated border border-white/[0.08] text-xs text-folio-text-secondary hover:text-folio-text-primary transition-colors">
          CSS variables
        </button>
        <button className="px-3 py-1.5 rounded-lg bg-folio-elevated border border-white/[0.08] text-xs text-folio-text-secondary hover:text-folio-text-primary transition-colors">
          Figma styles
        </button>
      </div>
    </div>
  )
}

function SectionHeader({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div className="mb-2">
      <h3 className="text-xs font-semibold text-folio-text-primary">{title}</h3>
      <p className="text-[10px] text-folio-text-muted">{subtitle}</p>
    </div>
  )
}
