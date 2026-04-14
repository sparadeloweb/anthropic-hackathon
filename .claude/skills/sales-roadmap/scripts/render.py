"""Renders a Roadmap to Markdown with summary, assignments, Mermaid Gantt, and task table.

Client-facing output: does not expose seniority or internal team details."""
from __future__ import annotations

from datetime import date, timedelta

from scheduler import Roadmap


def _working_days_between(start: date, end: date, working_days: list[int], holidays: set[date]) -> int:
    count = 0
    d = start
    while d <= end:
        if d.isoweekday() in working_days and d not in holidays:
            count += 1
        d += timedelta(days=1)
    return count


def render(roadmap: Roadmap, config: dict, holidays: set[date]) -> str:
    lines: list[str] = []
    if roadmap.feature:
        lines.append(f"# Roadmap — {roadmap.project} — {roadmap.feature}")
    else:
        lines.append(f"# Roadmap — {roadmap.project}")
    lines.append("")

    # Executive summary
    total_hours = sum(t.hours for t in roadmap.tasks)
    working = _working_days_between(
        roadmap.effective_start_date, roadmap.end_date, config["working_days"], holidays
    )
    lines.append("## Executive summary")
    lines.append("")
    lines.append(f"- **Desired start date**: {roadmap.desired_start_date.isoformat()}")
    lines.append(f"- **Effective start date**: {roadmap.effective_start_date.isoformat()}")
    if roadmap.shift_days > 0:
        lines.append(f"- **Shift**: +{roadmap.shift_days} days")
        lines.append(f"  - Reason: {roadmap.shift_reason}")
    lines.append(f"- **Estimated end date**: {roadmap.end_date.isoformat()}")
    lines.append(f"- **Duration**: {working} working days")
    lines.append(f"- **Estimated total hours**: {round(total_hours, 1)}")
    lines.append("")

    # Hours by area
    lines.append("## Hours by area")
    lines.append("")
    lines.append("| Area | Hours |")
    lines.append("|---|---:|")
    for d, h in sorted(roadmap.hours_by_dept.items(), key=lambda x: -x[1]):
        lines.append(f"| {d.capitalize()} | {round(h, 1)} |")
    lines.append("")

    # Hours by component
    lines.append("## Hours by component")
    lines.append("")
    lines.append("| Component | Hours |")
    lines.append("|---|---:|")
    for e, h in sorted(roadmap.hours_by_element.items(), key=lambda x: -x[1]):
        lines.append(f"| {e} | {round(h, 1)} |")
    lines.append("")

    # Project phases
    lines.append("## Project phases")
    lines.append("")
    lines.append("| Phase | Start | End | Hours |")
    lines.append("|---|---|---|---:|")
    for f in roadmap.phases_summary:
        lines.append(f"| {f['phase']} | {f['start']} | {f['end']} | {f['hours']} |")
    lines.append("")

    # Assigned team
    lines.append("## Assigned team")
    lines.append("")
    by_emp: dict[str, dict] = {}
    for t in roadmap.tasks:
        d = by_emp.setdefault(
            t.employee_name,
            {"hours": 0.0, "start": t.start, "end": t.end, "dept": t.department},
        )
        d["hours"] += t.hours
        d["start"] = min(d["start"], t.start)
        d["end"] = max(d["end"], t.end)

    lines.append("| Person | Role | Hours | From | To |")
    lines.append("|---|---|---:|---|---|")
    for name, info in sorted(by_emp.items()):
        lines.append(
            f"| {name} | {info['dept'].capitalize()} | {round(info['hours'], 1)} | "
            f"{info['start'].isoformat()} | {info['end'].isoformat()} |"
        )
    lines.append("")

    # Gantt Mermaid
    lines.append("## Schedule")
    lines.append("")
    lines.append("```mermaid")
    lines.append("gantt")
    if roadmap.feature:
        lines.append(f"    title {roadmap.project} — {roadmap.feature}")
    else:
        lines.append(f"    title {roadmap.project}")
    lines.append("    dateFormat YYYY-MM-DD")

    by_phase: dict[str, list] = {}
    for t in roadmap.tasks:
        by_phase.setdefault(t.phase_id, []).append(t)

    for phase_id, tasks in by_phase.items():
        lines.append(f"    section {phase_id.capitalize()}")
        for t in tasks:
            dur = (t.end - t.start).days + 1
            label = f"{t.atomic_name} [{t.employee_name.split()[0]}]"
            label = label.replace(":", "-")
            lines.append(f"    {label} :{t.start.isoformat()}, {dur}d")
    lines.append("```")
    lines.append("")

    # Task details
    lines.append("## Task details")
    lines.append("")
    lines.append("| Start | End | Area | Task | Component | Person | Hours |")
    lines.append("|---|---|---|---|---|---|---:|")
    for t in roadmap.tasks:
        lines.append(
            f"| {t.start.isoformat()} | {t.end.isoformat()} | {t.department.capitalize()} | "
            f"{t.atomic_name} | {t.element_name} | {t.employee_name} | {round(t.hours, 1)} |"
        )
    lines.append("")

    # Warnings
    if roadmap.warnings:
        lines.append("## Notes")
        lines.append("")
        for w in roadmap.warnings:
            lines.append(f"- {w}")
        lines.append("")

    # Assumptions
    lines.append("## Assumptions")
    lines.append("")
    lines.append(f"- Working day: {config['hours_per_day']}h/day, estimated productivity {int(config['productivity']*100)}%.")
    lines.append("- Working days: Monday to Friday.")
    lines.append("- Holidays: Argentine calendar included.")
    lines.append("- Complexity scale: Low x1.0, Medium x1.8, High x3.0.")
    lines.append("")

    return "\n".join(lines)
