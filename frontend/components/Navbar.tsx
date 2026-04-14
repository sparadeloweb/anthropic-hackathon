"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { ThemeToggle } from "@/components/ThemeToggle"

const NAV_ITEMS = [
  { href: "/dashboard", label: "Leads" },
  { href: "/hunt",      label: "New Hunt" },
]

export function Navbar() {
  const pathname = usePathname()

  return (
    <header className="sticky top-0 z-50 h-12 bg-folio-base/80 backdrop-blur-md border-b border-folio-border/[0.08] flex items-center px-6 gap-6">
      <Link href="/" className="flex items-center gap-2 text-folio-text-primary font-semibold text-sm">
        <span className="w-6 h-6 rounded-md bg-folio-accent flex items-center justify-center text-white text-[11px] font-bold leading-none">
          F
        </span>
        <span className="font-serif tracking-tight">Folio</span>
      </Link>

      <nav className="flex items-center gap-1 ml-2">
        {NAV_ITEMS.map((item) => {
          const isActive = pathname.startsWith(item.href)
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "px-3 py-1.5 text-xs rounded-md transition-colors",
                isActive
                  ? "bg-folio-border/[0.08] text-folio-text-primary font-medium"
                  : "text-folio-text-secondary hover:text-folio-text-primary hover:bg-folio-border/[0.05]"
              )}
            >
              {item.label}
            </Link>
          )
        })}
      </nav>

      <div className="ml-auto flex items-center gap-2">
        <span className="flex items-center gap-1.5 text-xs text-folio-text-muted mr-1">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse-slow" />
          Hunt active
        </span>
        <ThemeToggle />
      </div>
    </header>
  )
}
