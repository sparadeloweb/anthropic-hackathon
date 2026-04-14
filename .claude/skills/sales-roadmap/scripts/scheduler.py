"""Scheduler: expande el input del proyecto, asigna personas nominales, calcula fechas
respetando dependencias entre fases, feriados AR y corrimiento automático de inicio."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

from catalog import Catalog
from roster import Roster


@dataclass
class TaskAssignment:
    """Una tarea atómica asignada a una persona, con fechas concretas."""
    elemento_id: str              # page/feature/integration al que pertenece
    elemento_nombre: str
    atomic_id: str
    atomic_nombre: str
    departamento: str
    fase_id: str
    empleado_id: str
    empleado_nombre: str
    horas: float
    inicio: date
    fin: date


@dataclass
class Roadmap:
    proyecto: str
    fecha_inicio_deseada: date
    fecha_inicio_efectiva: date
    fecha_fin: date
    corrimiento_dias: int
    razon_corrimiento: str
    tareas: list[TaskAssignment]
    fases_resumen: list[dict] = field(default_factory=list)
    horas_por_depto: dict[str, float] = field(default_factory=dict)
    horas_por_elemento: dict[str, float] = field(default_factory=dict)
    advertencias: list[str] = field(default_factory=list)


# ---------------- helpers ----------------

def _next_working_day(r: Roster, d: date) -> date:
    while not r.is_working_day(d):
        d += timedelta(days=1)
    return d


def _expand_items(
    input_items: list[dict],
    catalog_coll: dict,
    mult_dificultad: dict,
) -> list[dict]:
    """Expande un bloque de input (paginas/features/integraciones) a tareas atómicas
    con horas_ideales (en escala Semi) asignadas. Devuelve lista de dicts:
    {elemento_id, elemento_nombre, atomic_id, horas_ideales}."""
    expanded = []
    for it in input_items:
        if it["id"] not in catalog_coll:
            raise ValueError(f"Elemento desconocido: {it['id']}")
        elem = catalog_coll[it["id"]]
        dif = it.get("dificultad", "media")
        if dif not in mult_dificultad:
            raise ValueError(f"Dificultad inválida: {dif}")
        mdif = mult_dificultad[dif]
        cant_elem = it.get("cantidad", 1)
        for t in elem.tareas:
            horas = t.get("cantidad", 1) * mdif * cant_elem
            expanded.append(
                {
                    "elemento_id": elem.id,
                    "elemento_nombre": elem.nombre,
                    "atomic_id": t["id"],
                    "horas_ideales_por_unidad": horas,
                }
            )
    return expanded


def _dept_capacity_in_window(r: Roster, dept: str, desde: date, dias: int, emp_ids: set[str]) -> float:
    """Suma horas efectivas disponibles del depto en una ventana."""
    total = 0.0
    d = desde
    count = 0
    while count < dias:
        for e in r.employees_by_dept(dept):
            if e.id in emp_ids:
                total += r.effective_hours(e.id, d)
        d += timedelta(days=1)
        count += 1
    return total


def _find_shift_start(r: Roster, depto_inicial: str, fecha_base: date, emp_ids: set[str]) -> tuple[date, str]:
    """Busca la primera fecha con capacidad razonable en el depto de la fase inicial.
    Criterio: al menos una persona del depto con disponibilidad >= 50% de su capacidad."""
    d = _next_working_day(r, fecha_base)
    limit = d + timedelta(days=365)
    while d <= limit:
        if r.is_working_day(d):
            for emp in r.employees_by_dept(depto_inicial):
                if emp.id not in emp_ids:
                    continue
                libre_frac = emp.dedicacion_default - r.allocated_on(emp.id, d)
                if libre_frac >= 0.5:
                    if d == fecha_base:
                        return d, ""
                    return d, (
                        f"La fecha deseada {fecha_base.isoformat()} no tiene capacidad suficiente "
                        f"en {depto_inicial}. Primera fecha con al menos una persona libre al 50%: "
                        f"{d.isoformat()}."
                    )
        d += timedelta(days=1)
    raise RuntimeError(
        f"No se encontró capacidad en {depto_inicial} en el próximo año. "
        f"Revisar roster y allocations."
    )


def _assign_phase(
    r: Roster,
    fase: dict,
    horas_por_depto_ideales: dict[str, float],
    tareas_ideales: list[dict],  # tareas expandidas del input filtradas por esta fase
    catalog: Catalog,
    emp_ids: set[str],
    fecha_desde: date,
) -> tuple[list[TaskAssignment], date]:
    """Asigna las tareas de una fase a personas y devuelve la fecha_fin de la fase.
    Cada depto de la fase corre en paralelo; la fase termina cuando el más lento termina."""
    assignments: list[TaskAssignment] = []
    fase_fin = fecha_desde

    for depto in fase["departamentos"]:
        candidates = [e for e in r.employees_by_dept(depto) if e.id in emp_ids]
        if not candidates:
            # depto sin personal: registrar con fecha fecha_desde si no hay horas
            if horas_por_depto_ideales.get(depto, 0) > 0:
                raise RuntimeError(
                    f"Fase '{fase['id']}' requiere {depto} pero no hay empleados disponibles."
                )
            continue

        # Tareas ideales que caen en este depto
        tareas_depto = [
            t for t in tareas_ideales
            if catalog.atomic[t["atomic_id"]].departamento == depto
        ]
        # Ordenar: tareas más grandes primero (mejor balance)
        tareas_depto.sort(key=lambda t: -t["horas_ideales_total"])

        # Seniority-aware scheduling: para cada tarea, elegir la persona con más horas libres
        # en los próximos días y llenar día a día.
        depto_fin = fecha_desde
        for t in tareas_depto:
            horas_ideales = t["horas_ideales_total"]
            atomic = catalog.atomic[t["atomic_id"]]

            # Elegir persona con mejor "score" inmediato: quien pueda cubrir más rápido
            # (más horas libres efectivas en los próximos ~20 días hábiles)
            persona = _pick_person(r, candidates, fecha_desde, 20)

            mult_sen = r.multipliers["seniority"][persona.seniority]
            horas_reales = horas_ideales * mult_sen  # horas calendario que le toman

            inicio, fin = _schedule_hours(r, persona.id, fecha_desde, horas_reales)
            assignments.append(
                TaskAssignment(
                    elemento_id=t["elemento_id"],
                    elemento_nombre=t["elemento_nombre"],
                    atomic_id=atomic.id,
                    atomic_nombre=atomic.nombre,
                    departamento=depto,
                    fase_id=fase["id"],
                    empleado_id=persona.id,
                    empleado_nombre=persona.nombre,
                    horas=round(horas_reales, 2),
                    inicio=inicio,
                    fin=fin,
                )
            )
            if fin > depto_fin:
                depto_fin = fin

        if depto_fin > fase_fin:
            fase_fin = depto_fin

    return assignments, fase_fin


def _pick_person(r: Roster, candidates: list, fecha_desde: date, ventana_dias: int):
    """Elige a la persona con más horas efectivas libres en la ventana próxima."""
    mejor = None
    mejor_horas = -1.0
    for emp in candidates:
        total = 0.0
        d = _next_working_day(r, fecha_desde)
        dias = 0
        while dias < ventana_dias:
            total += r.available_hours(emp.id, d)
            d += timedelta(days=1)
            dias += 1
        if total > mejor_horas:
            mejor_horas = total
            mejor = emp
    return mejor


# Usage tracking global (reservas hechas en este roadmap, para no doble-asignar)
_usage: dict[tuple[str, date], float] = {}


def _reset_usage():
    _usage.clear()


def _schedule_hours(r: Roster, emp_id: str, fecha_desde: date, horas: float) -> tuple[date, date]:
    """Consume horas de una persona día por día desde fecha_desde hasta completar.
    Registra el uso en _usage para que las siguientes tareas respeten las reservas previas."""
    restante = horas
    inicio: date | None = None
    ultimo: date | None = None
    d = _next_working_day(r, fecha_desde)
    safety = 0
    while restante > 0.01:
        safety += 1
        if safety > 3650:
            raise RuntimeError(f"Loop en _schedule_hours para {emp_id}")
        libre_dia = r.available_hours(emp_id, d) - _usage.get((emp_id, d), 0.0)
        if libre_dia > 0.01:
            usar = min(restante, libre_dia)
            _usage[(emp_id, d)] = _usage.get((emp_id, d), 0.0) + usar
            restante -= usar
            if inicio is None:
                inicio = d
            ultimo = d
        d += timedelta(days=1)
        while not r.is_working_day(d):
            d += timedelta(days=1)

    assert inicio is not None and ultimo is not None
    return inicio, ultimo


# ---------------- entry point ----------------

def build_roadmap(
    input_data: dict,
    catalog: Catalog,
    roster: Roster,
) -> Roadmap:
    _reset_usage()
    proyecto = input_data["proyecto"]
    fecha_deseada = date.fromisoformat(str(input_data["fecha_inicio_deseada"]))

    # Filtrar empleados según input (si se restringe)
    if "empleados_id" in input_data and input_data["empleados_id"]:
        emp_ids = set(input_data["empleados_id"])
    else:
        emp_ids = set(roster.employees.keys())

    mult_dif = catalog.multipliers["dificultad"]

    # Expansión
    exp: list[dict] = []
    exp += _expand_items(input_data.get("paginas", []), catalog.pages, mult_dif)
    exp += _expand_items(input_data.get("features", []), catalog.features, mult_dif)
    exp += _expand_items(input_data.get("integraciones", []), catalog.integrations, mult_dif)

    # Calcular horas_base × horas_ideales_por_unidad para cada atómica expandida
    for t in exp:
        atomic = catalog.atomic[t["atomic_id"]]
        t["horas_ideales_total"] = atomic.horas_base * t["horas_ideales_por_unidad"]

    # Agrupar horas por depto
    horas_por_depto: dict[str, float] = {}
    horas_por_elemento: dict[str, float] = {}
    for t in exp:
        dept = catalog.atomic[t["atomic_id"]].departamento
        horas_por_depto[dept] = horas_por_depto.get(dept, 0.0) + t["horas_ideales_total"]
        horas_por_elemento[t["elemento_nombre"]] = (
            horas_por_elemento.get(t["elemento_nombre"], 0.0) + t["horas_ideales_total"]
        )

    # Corrimiento de inicio según la primera fase
    fases = [f for f in catalog.dependencies if not f.get("opcional") or f["id"] != "qa"]
    primera_fase = fases[0]
    depto_inicial = primera_fase["departamentos"][0]
    fecha_inicio_efectiva, razon = _find_shift_start(roster, depto_inicial, fecha_deseada, emp_ids)
    corrimiento = (fecha_inicio_efectiva - fecha_deseada).days

    # Secuenciar fases respetando dependencias
    fase_fin_by_id: dict[str, date] = {}
    assignments_all: list[TaskAssignment] = []
    fases_resumen = []
    advertencias: list[str] = []

    for fase in fases:
        if fase.get("opcional"):
            continue  # QA solo si se pide explícitamente (no en MVP)

        # Determinar fecha desde la cual puede empezar esta fase
        deps = fase.get("depende_de", [])
        if deps:
            fecha_desde = max(fase_fin_by_id[d] for d in deps) + timedelta(days=1)
            fecha_desde = _next_working_day(roster, fecha_desde)
        else:
            fecha_desde = fecha_inicio_efectiva

        # Horas por depto para esta fase
        horas_fase_depto = {
            d: sum(
                t["horas_ideales_total"]
                for t in exp
                if catalog.atomic[t["atomic_id"]].departamento == d
            )
            for d in fase["departamentos"]
        }

        tareas_fase = [
            t for t in exp
            if catalog.atomic[t["atomic_id"]].departamento in fase["departamentos"]
        ]

        if sum(horas_fase_depto.values()) == 0:
            fase_fin_by_id[fase["id"]] = fecha_desde
            continue

        asignaciones, fase_fin = _assign_phase(
            roster, fase, horas_fase_depto, tareas_fase, catalog, emp_ids, fecha_desde,
        )
        assignments_all.extend(asignaciones)
        fase_fin_by_id[fase["id"]] = fase_fin

        fases_resumen.append(
            {
                "fase": fase["nombre"],
                "inicio": fecha_desde.isoformat(),
                "fin": fase_fin.isoformat(),
                "horas": round(sum(a.horas for a in asignaciones), 2),
            }
        )

    fecha_fin = max(fase_fin_by_id.values()) if fase_fin_by_id else fecha_inicio_efectiva

    return Roadmap(
        proyecto=proyecto,
        fecha_inicio_deseada=fecha_deseada,
        fecha_inicio_efectiva=fecha_inicio_efectiva,
        fecha_fin=fecha_fin,
        corrimiento_dias=corrimiento,
        razon_corrimiento=razon,
        tareas=sorted(assignments_all, key=lambda a: (a.inicio, a.departamento)),
        fases_resumen=fases_resumen,
        horas_por_depto={k: round(v, 2) for k, v in horas_por_depto.items()},
        horas_por_elemento={k: round(v, 2) for k, v in horas_por_elemento.items()},
        advertencias=advertencias,
    )
