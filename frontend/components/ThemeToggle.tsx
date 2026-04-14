"use client"

import { useTheme } from "next-themes"
import { useEffect, useState } from "react"
import { Sun, Moon } from "lucide-react"
import { cn } from "@/lib/utils"

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  // Avoid hydration mismatch — only render after client mount
  useEffect(() => { setMounted(true) }, [])

  if (!mounted) {
    return <div className="w-7 h-7" />
  }

  const isDark = theme === "dark"

  return (
    <button
      onClick={() => setTheme(isDark ? "light" : "dark")}
      aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
      className={cn(
        "w-7 h-7 rounded-md flex items-center justify-center transition-colors",
        "text-folio-text-muted hover:text-folio-text-secondary",
        "hover:bg-folio-border/[0.08]"
      )}
    >
      {isDark ? <Sun size={14} /> : <Moon size={14} />}
    </button>
  )
}
