"""Renders a client-ready budget in Markdown from parsed roadmap data and hourly rates."""
from __future__ import annotations

from datetime import datetime

from parser import CANONICAL_ROLES

RATE_KEY_BY_ROLE = {
    "Backend": "backend",
    "Frontend": "frontend",
    "Architecture": "architecture",
    "Design": "design",
    "Project Management": "project_management",
    "Product Owner": "product_owner",
}


def compute_budget(hours_by_role: dict[str, float], rates: dict[str, float]) -> dict:
    """Returns {role: {hours, rate, subtotal}} plus totals.
    Always includes the six canonical roles (even if 0h), and appends any
    non-canonical roles from the roadmap (priced at 0 until mapped)."""
    rows: dict[str, dict] = {}
    for role in CANONICAL_ROLES:
        hrs = float(hours_by_role.get(role, 0.0))
        rate = float(rates.get(RATE_KEY_BY_ROLE[role], 0))
        rows[role] = {"hours": hrs, "rate": rate, "subtotal": round(hrs * rate, 2)}

    for role, hrs in hours_by_role.items():
        if role not in rows:
            rows[role] = {"hours": float(hrs), "rate": 0.0, "subtotal": 0.0}

    total = round(sum(r["subtotal"] for r in rows.values()), 2)
    total_hours = round(sum(r["hours"] for r in rows.values()), 2)
    return {"rows": rows, "total": total, "total_hours": total_hours}


def render(
    parsed: dict,
    rates: dict[str, float],
    client: str,
    project: str,
    currency: str = "USD",
) -> str:
    budget = compute_budget(parsed["hours_by_role"], rates)
    rows = budget["rows"]

    lines: list[str] = []
    lines.append(f"# Budget — {project}")
    lines.append("")
    lines.append(f"**Client:** {client}")
    lines.append(f"**Project:** {project}")
    lines.append(f"**Issue date:** {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"**Currency:** {currency}")
    lines.append("")

    # Executive summary
    lines.append("## Executive summary")
    lines.append("")
    lines.append(f"- **Estimated total hours**: {budget['total_hours']}")
    lines.append(f"- **Total investment**: {currency} {budget['total']:,.2f}")
    if parsed.get("start_date"):
        lines.append(f"- **Estimated start**: {parsed['start_date']}")
    if parsed.get("end_date"):
        lines.append(f"- **Estimated end**: {parsed['end_date']}")
    if parsed.get("duration_working_days"):
        lines.append(f"- **Duration**: {parsed['duration_working_days']} working days")
    lines.append("")

    # Breakdown by role
    lines.append("## Breakdown by role")
    lines.append("")
    lines.append(f"| Role | Hours | Rate ({currency}/h) | Subtotal ({currency}) |")
    lines.append("|---|---:|---:|---:|")
    for role, data in rows.items():
        lines.append(
            f"| {role} | {data['hours']:.1f} | {data['rate']:,.2f} | {data['subtotal']:,.2f} |"
        )
    lines.append(f"| **TOTAL** | **{budget['total_hours']:.1f}** |  | **{budget['total']:,.2f}** |")
    lines.append("")

    # Project phases
    if parsed.get("phases"):
        lines.append("## Project phases")
        lines.append("")
        lines.append("| Phase | Start | End | Hours |")
        lines.append("|---|---|---|---:|")
        for p in parsed["phases"]:
            lines.append(
                f"| {p['phase']} | {p['start']} | {p['end']} | {p['hours']} |"
            )
        lines.append("")

    # Assumptions
    lines.append("## Assumptions")
    lines.append("")
    lines.append(f"- Budget denominated in **{currency}**, based on per-role hourly rates.")
    lines.append("- Hours are derived from the engineering roadmap already approved internally.")
    lines.append("- Budget validity: 30 days from the issue date.")
    lines.append("- Excludes: taxes, infrastructure/third-party service fees, software licenses.")
    lines.append("")

    # Source
    lines.append("## Source")
    lines.append("")
    lines.append(f"- Base roadmap: `{parsed['source_file']}`")
    lines.append("")

    return "\n".join(lines)
