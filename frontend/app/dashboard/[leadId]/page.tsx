"use client"

import { use } from "react"
import { Navbar } from "@/components/Navbar"
import { LeadDetailPanel } from "@/components/LeadDetailPanel"

interface Props {
  params: Promise<{ leadId: string }>
}

export default function LeadDetailPage({ params }: Props) {
  const { leadId } = use(params)

  return (
    <div className="h-screen bg-folio-base flex flex-col overflow-hidden">
      <Navbar />
      <div className="flex-1 overflow-hidden">
        <LeadDetailPanel leadId={leadId} showBackButton />
      </div>
    </div>
  )
}
