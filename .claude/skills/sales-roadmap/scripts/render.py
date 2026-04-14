"""Renderiza un Roadmap a Markdown con resumen, asignaciones, Gantt Mermaid y tabla de tareas."""
from __future__ import annotations

from datetime import date, timedelta

from scheduler import Roadmap


def _working_days_between(inicio: date, fin: date, dias_laborables: list[int], holidays: set[date]) -> int:
    count = 0
    d = inicio
    while d <= fin:
        if d.isoweekday() in dias_laborables and d not in holidays:
            count += 1
        d += timedelta(days=1)
    return count


def render(roadmap: Roadmap, config: dict, holidays: set[date]) -> str:
    lines: list[str] = []
    lines.append(f"# Roadmap — {roadmap.proyecto}")
    lines.append("")

    # Resumen ejecutivo
    total_horas = sum(t.horas for t in roadmap.tareas)
    dias_lab = _working_days_between(
        roadmap.fecha_inicio_efectiva, roadmap.fecha_fin, config["dias_laborables"], holidays
    )
    lines.append("## Resumen ejecutivo")
    lines.append("")
    lines.append(f"- **Fecha de inicio deseada**: {roadmap.fecha_inicio_deseada.isoformat()}")
    lines.append(f"- **Fecha de inicio efectiva**: {roadmap.fecha_inicio_efectiva.isoformat()}")
    if roadmap.corrimiento_dias > 0:
        lines.append(f"- **Corrimiento**: +{roadmap.corrimiento_dias} días")
        lines.append(f"  - Motivo: {roadmap.razon_corrimiento}")
    lines.append(f"- **Fecha estimada de fin**: {roadmap.fecha_fin.isoformat()}")
    lines.append(f"- **Duración**: {dias_lab} días laborales")
    lines.append(f"- **Horas totales**: {round(total_horas, 1)}")
    lines.append("")

    # Desglose por departamento
    lines.append("## Horas por departamento (escala Semi, sin ajuste por seniority)")
    lines.append("")
    lines.append("| Departamento | Horas |")
    lines.append("|---|---:|")
    for d, h in sorted(roadmap.horas_por_depto.items(), key=lambda x: -x[1]):
        lines.append(f"| {d} | {h} |")
    lines.append("")

    # Desglose por elemento
    lines.append("## Horas por elemento")
    lines.append("")
    lines.append("| Elemento | Horas |")
    lines.append("|---|---:|")
    for e, h in sorted(roadmap.horas_por_elemento.items(), key=lambda x: -x[1]):
        lines.append(f"| {e} | {h} |")
    lines.append("")

    # Asignaciones nominales
    lines.append("## Asignaciones nominales")
    lines.append("")
    by_emp: dict[str, dict] = {}
    for t in roadmap.tareas:
        d = by_emp.setdefault(
            t.empleado_nombre,
            {"horas": 0.0, "inicio": t.inicio, "fin": t.fin, "depto": t.departamento},
        )
        d["horas"] += t.horas
        d["inicio"] = min(d["inicio"], t.inicio)
        d["fin"] = max(d["fin"], t.fin)

    lines.append("| Persona | Depto | Horas | Desde | Hasta |")
    lines.append("|---|---|---:|---|---|")
    for nombre, info in sorted(by_emp.items()):
        lines.append(
            f"| {nombre} | {info['depto']} | {round(info['horas'], 1)} | "
            f"{info['inicio'].isoformat()} | {info['fin'].isoformat()} |"
        )
    lines.append("")

    # Resumen de fases
    lines.append("## Fases")
    lines.append("")
    lines.append("| Fase | Inicio | Fin | Horas |")
    lines.append("|---|---|---|---:|")
    for f in roadmap.fases_resumen:
        lines.append(f"| {f['fase']} | {f['inicio']} | {f['fin']} | {f['horas']} |")
    lines.append("")

    # Gantt Mermaid
    lines.append("## Cronograma (Gantt)")
    lines.append("")
    lines.append("```mermaid")
    lines.append("gantt")
    lines.append(f"    title Roadmap — {roadmap.proyecto}")
    lines.append("    dateFormat YYYY-MM-DD")

    by_phase: dict[str, list] = {}
    for t in roadmap.tareas:
        by_phase.setdefault(t.fase_id, []).append(t)

    for fase_id, tareas in by_phase.items():
        lines.append(f"    section {fase_id}")
        for t in tareas:
            dur = (t.fin - t.inicio).days + 1
            nombre = f"{t.atomic_nombre} [{t.empleado_nombre.split()[0]}]"
            nombre = nombre.replace(":", "-")
            lines.append(f"    {nombre} :{t.inicio.isoformat()}, {dur}d")
    lines.append("```")
    lines.append("")

    # Tabla detallada
    lines.append("## Detalle de tareas")
    lines.append("")
    lines.append("| Inicio | Fin | Depto | Tarea | Elemento | Persona | Horas |")
    lines.append("|---|---|---|---|---|---|---:|")
    for t in roadmap.tareas:
        lines.append(
            f"| {t.inicio.isoformat()} | {t.fin.isoformat()} | {t.departamento} | "
            f"{t.atomic_nombre} | {t.elemento_nombre} | {t.empleado_nombre} | {t.horas} |"
        )
    lines.append("")

    # Advertencias
    if roadmap.advertencias:
        lines.append("## Advertencias")
        lines.append("")
        for a in roadmap.advertencias:
            lines.append(f"- {a}")
        lines.append("")

    # Supuestos
    lines.append("## Supuestos")
    lines.append("")
    lines.append(f"- Jornada: {config['horas_por_dia']}h/día, productividad {int(config['productividad']*100)}%.")
    lines.append("- Días laborales: lunes a viernes.")
    lines.append("- Feriados: calendario de Argentina.")
    lines.append("- Multiplicadores dificultad: Baja x1.0, Media x1.8, Alta x3.0.")
    lines.append("- Multiplicadores seniority: Junior x1.5, Semi x1.0, Senior x0.7 (sobre horas base).")
    lines.append("")

    return "\n".join(lines)
