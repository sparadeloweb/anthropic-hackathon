"""Renderiza un Roadmap a Markdown con resumen, asignaciones, Gantt Mermaid y tabla de tareas.

Output pensado para el cliente final: no expone seniority ni detalles internos del equipo."""
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
    if roadmap.feature:
        lines.append(f"# Roadmap — {roadmap.proyecto} — {roadmap.feature}")
    else:
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
    lines.append(f"- **Horas totales estimadas**: {round(total_horas, 1)}")
    lines.append("")

    # Desglose por departamento
    lines.append("## Horas por área")
    lines.append("")
    lines.append("| Área | Horas |")
    lines.append("|---|---:|")
    for d, h in sorted(roadmap.horas_por_depto.items(), key=lambda x: -x[1]):
        lines.append(f"| {d.capitalize()} | {round(h, 1)} |")
    lines.append("")

    # Desglose por elemento
    lines.append("## Horas por componente")
    lines.append("")
    lines.append("| Componente | Horas |")
    lines.append("|---|---:|")
    for e, h in sorted(roadmap.horas_por_elemento.items(), key=lambda x: -x[1]):
        lines.append(f"| {e} | {round(h, 1)} |")
    lines.append("")

    # Resumen de fases
    lines.append("## Fases del proyecto")
    lines.append("")
    lines.append("| Fase | Inicio | Fin | Horas |")
    lines.append("|---|---|---|---:|")
    for f in roadmap.fases_resumen:
        lines.append(f"| {f['fase']} | {f['inicio']} | {f['fin']} | {f['horas']} |")
    lines.append("")

    # Equipo asignado
    lines.append("## Equipo asignado")
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

    lines.append("| Persona | Rol | Horas | Desde | Hasta |")
    lines.append("|---|---|---:|---|---|")
    for nombre, info in sorted(by_emp.items()):
        lines.append(
            f"| {nombre} | {info['depto'].capitalize()} | {round(info['horas'], 1)} | "
            f"{info['inicio'].isoformat()} | {info['fin'].isoformat()} |"
        )
    lines.append("")

    # Gantt Mermaid
    lines.append("## Cronograma")
    lines.append("")
    lines.append("```mermaid")
    lines.append("gantt")
    if roadmap.feature:
        lines.append(f"    title {roadmap.proyecto} — {roadmap.feature}")
    else:
        lines.append(f"    title {roadmap.proyecto}")
    lines.append("    dateFormat YYYY-MM-DD")

    by_phase: dict[str, list] = {}
    for t in roadmap.tareas:
        by_phase.setdefault(t.fase_id, []).append(t)

    for fase_id, tareas in by_phase.items():
        lines.append(f"    section {fase_id.capitalize()}")
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
    lines.append("| Inicio | Fin | Área | Tarea | Componente | Persona | Horas |")
    lines.append("|---|---|---|---|---|---|---:|")
    for t in roadmap.tareas:
        lines.append(
            f"| {t.inicio.isoformat()} | {t.fin.isoformat()} | {t.departamento.capitalize()} | "
            f"{t.atomic_nombre} | {t.elemento_nombre} | {t.empleado_nombre} | {round(t.horas, 1)} |"
        )
    lines.append("")

    # Advertencias
    if roadmap.advertencias:
        lines.append("## Notas")
        lines.append("")
        for a in roadmap.advertencias:
            lines.append(f"- {a}")
        lines.append("")

    # Supuestos
    lines.append("## Supuestos")
    lines.append("")
    lines.append(f"- Jornada laboral: {config['horas_por_dia']}h/día, productividad estimada {int(config['productividad']*100)}%.")
    lines.append("- Días laborales: lunes a viernes.")
    lines.append("- Feriados: calendario de Argentina incluido.")
    lines.append("- Escala de complejidad: Baja x1.0, Media x1.8, Alta x3.0.")
    lines.append("")

    return "\n".join(lines)
