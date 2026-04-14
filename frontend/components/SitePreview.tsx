"use client"

import { useState } from "react"
import { Monitor, Smartphone, ExternalLink, RefreshCw } from "lucide-react"
import { cn } from "@/lib/utils"

interface SitePreviewProps {
  previewUrl: string
  leadName: string
}

export function SitePreview({ previewUrl, leadName }: SitePreviewProps) {
  const [device, setDevice] = useState<"desktop" | "mobile">("desktop")
  const [key, setKey] = useState(0)

  function refresh() {
    setKey((k) => k + 1)
  }

  return (
    <div className="flex flex-col h-full gap-3">
      {/* Toolbar */}
      <div className="flex items-center gap-2">
        <div className="flex items-center gap-1 bg-folio-elevated rounded-lg p-1 border border-white/[0.06]">
          <DeviceButton
            icon={<Monitor size={13} />}
            label="Desktop"
            active={device === "desktop"}
            onClick={() => setDevice("desktop")}
          />
          <DeviceButton
            icon={<Smartphone size={13} />}
            label="Mobile"
            active={device === "mobile"}
            onClick={() => setDevice("mobile")}
          />
        </div>

        <button
          onClick={refresh}
          className="p-2 rounded-lg bg-folio-elevated border border-white/[0.06] text-folio-text-muted hover:text-folio-text-secondary transition-colors"
          title="Reload preview"
        >
          <RefreshCw size={13} />
        </button>

        <a
          href={previewUrl}
          target="_blank"
          rel="noreferrer"
          className="ml-auto flex items-center gap-1.5 text-xs text-folio-text-muted hover:text-folio-accent transition-colors"
        >
          <ExternalLink size={12} />
          Open full
        </a>
      </div>

      {/* Frame */}
      <div
        className={cn(
          "flex-1 bg-folio-elevated rounded-xl border border-white/[0.06] overflow-hidden flex items-center justify-center transition-all duration-300",
          device === "mobile" ? "py-4" : "p-0"
        )}
      >
        <div
          className={cn(
            "relative transition-all duration-300 overflow-hidden rounded-lg",
            device === "mobile"
              ? "w-[375px] h-[667px] shadow-[0_0_0_1px_rgba(255,255,255,0.1),0_20px_60px_rgba(0,0,0,0.6)]"
              : "w-full h-full"
          )}
        >
          {/* Mobile notch decoration */}
          {device === "mobile" ? (
            <div className="absolute top-0 left-0 right-0 h-6 bg-black/80 z-10 flex items-center justify-center">
              <div className="w-16 h-1.5 rounded-full bg-folio-elevated" />
            </div>
          ) : null}

          <iframe
            key={key}
            src={previewUrl}
            title={`Preview — ${leadName}`}
            className={cn(
              "w-full h-full border-0",
              device === "mobile" ? "pt-6" : ""
            )}
            sandbox="allow-scripts allow-same-origin"
          />
        </div>
      </div>
    </div>
  )
}

interface DeviceButtonProps {
  icon: React.ReactNode
  label: string
  active: boolean
  onClick: () => void
}

function DeviceButton({ icon, label, active, onClick }: DeviceButtonProps) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-xs transition-colors",
        active
          ? "bg-folio-accent/20 text-folio-accent"
          : "text-folio-text-muted hover:text-folio-text-secondary"
      )}
    >
      {icon}
      <span className="hidden sm:inline">{label}</span>
    </button>
  )
}
