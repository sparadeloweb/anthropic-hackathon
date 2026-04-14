"""Scheduler: expands project input, assigns named people, calculates dates
respecting phase dependencies, AR holidays, and automatic start date shifting."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

from catalog import Catalog
from roster import Roster


@dataclass
class TaskAssignment:
    """An atomic task assigned to a person, with concrete dates."""
    element_id: str              # page/feature/integration it belongs to
    element_name: str
    atomic_id: str
    atomic_name: str
    department: str
    phase_id: str
    employee_id: str
    employee_name: str
    hours: float
    start: date
    end: date


@dataclass
class Roadmap:
    project: str
    desired_start_date: date
    effective_start_date: date
    end_date: date
    shift_days: int
    shift_reason: str
    tasks: list[TaskAssignment]
    phases_summary: list[dict] = field(default_factory=list)
    hours_by_dept: dict[str, float] = field(default_factory=dict)
    hours_by_element: dict[str, float] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    feature: str = ""  # Feature name if this is an incremental roadmap


# ---------------- helpers ----------------

def _next_working_day(r: Roster, d: date) -> date:
    while not r.is_working_day(d):
        d += timedelta(days=1)
    return d


def _expand_items(
    input_items: list[dict],
    catalog_coll: dict,
    mult_difficulty: dict,
) -> list[dict]:
    """Expands an input block (pages/features/integrations) into atomic tasks
    with ideal_hours (Semi scale) assigned. Returns list of dicts:
    {element_id, element_name, atomic_id, ideal_hours}."""
    expanded = []
    for it in input_items:
        if it["id"] not in catalog_coll:
            raise ValueError(f"Unknown element: {it['id']}")
        elem = catalog_coll[it["id"]]
        dif = it.get("difficulty", "medium")
        if dif not in mult_difficulty:
            raise ValueError(f"Invalid difficulty: {dif}")
        mdif = mult_difficulty[dif]
        qty_elem = it.get("quantity", 1)
        for t in elem.tasks:
            hours = t.get("quantity", 1) * mdif * qty_elem
            expanded.append(
                {
                    "element_id": elem.id,
                    "element_name": elem.name,
                    "atomic_id": t["id"],
                    "ideal_hours_per_unit": hours,
                }
            )
    return expanded


def _dept_capacity_in_window(r: Roster, dept: str, from_date: date, days: int, emp_ids: set[str]) -> float:
    """Sum effective available hours for a department in a window."""
    total = 0.0
    d = from_date
    count = 0
    while count < days:
        for e in r.employees_by_dept(dept):
            if e.id in emp_ids:
                total += r.effective_hours(e.id, d)
        d += timedelta(days=1)
        count += 1
    return total


def _find_shift_start(r: Roster, initial_dept: str, base_date: date, emp_ids: set[str]) -> tuple[date, str]:
    """Finds the first date with reasonable capacity in the initial phase department.
    Criterion: at least one person in the department with availability >= 50% of their capacity."""
    d = _next_working_day(r, base_date)
    limit = d + timedelta(days=365)
    while d <= limit:
        if r.is_working_day(d):
            for emp in r.employees_by_dept(initial_dept):
                if emp.id not in emp_ids:
                    continue
                free_frac = emp.default_allocation - r.allocated_on(emp.id, d)
                if free_frac >= 0.5:
                    if d == base_date:
                        return d, ""
                    return d, (
                        f"The desired date {base_date.isoformat()} does not have sufficient capacity "
                        f"in {initial_dept}. First date with at least one person free at 50%: "
                        f"{d.isoformat()}."
                    )
        d += timedelta(days=1)
    raise RuntimeError(
        f"No capacity found in {initial_dept} within the next year. "
        f"Review roster and allocations."
    )


def _assign_phase(
    r: Roster,
    phase: dict,
    hours_by_dept_ideal: dict[str, float],
    ideal_tasks: list[dict],  # expanded input tasks filtered for this phase
    catalog: Catalog,
    emp_ids: set[str],
    from_date: date,
) -> tuple[list[TaskAssignment], date]:
    """Assigns tasks of a phase to people and returns the phase end date.
    Each department in the phase runs in parallel; the phase ends when the slowest finishes."""
    assignments: list[TaskAssignment] = []
    phase_end = from_date

    for dept in phase["departments"]:
        candidates = [e for e in r.employees_by_dept(dept) if e.id in emp_ids]
        if not candidates:
            # Department without staff: register with from_date if no hours
            if hours_by_dept_ideal.get(dept, 0) > 0:
                raise RuntimeError(
                    f"Phase '{phase['id']}' requires {dept} but no employees are available."
                )
            continue

        # Ideal tasks that fall in this department
        dept_tasks = [
            t for t in ideal_tasks
            if catalog.atomic[t["atomic_id"]].department == dept
        ]
        # Sort: largest tasks first (better balance)
        dept_tasks.sort(key=lambda t: -t["ideal_hours_total"])

        # Seniority-aware scheduling: for each task, pick the person with the most free hours
        # in the next days and fill day by day.
        dept_end = from_date
        for t in dept_tasks:
            ideal_hours = t["ideal_hours_total"]
            atomic = catalog.atomic[t["atomic_id"]]

            # Pick person with best immediate "score": whoever can cover it fastest
            # (most free effective hours in the next ~20 working days)
            person = _pick_person(r, candidates, from_date, 20)

            mult_sen = r.multipliers["seniority"][person.seniority]
            real_hours = ideal_hours * mult_sen  # calendar hours it takes them

            start, end = _schedule_hours(r, person.id, from_date, real_hours)
            assignments.append(
                TaskAssignment(
                    element_id=t["element_id"],
                    element_name=t["element_name"],
                    atomic_id=atomic.id,
                    atomic_name=atomic.name,
                    department=dept,
                    phase_id=phase["id"],
                    employee_id=person.id,
                    employee_name=person.name,
                    hours=round(real_hours, 2),
                    start=start,
                    end=end,
                )
            )
            if end > dept_end:
                dept_end = end

        if dept_end > phase_end:
            phase_end = dept_end

    return assignments, phase_end


def _pick_person(r: Roster, candidates: list, from_date: date, window_days: int):
    """Picks the person with the most free effective hours in the upcoming window."""
    best = None
    best_hours = -1.0
    for emp in candidates:
        total = 0.0
        d = _next_working_day(r, from_date)
        days = 0
        while days < window_days:
            total += r.available_hours(emp.id, d)
            d += timedelta(days=1)
            days += 1
        if total > best_hours:
            best_hours = total
            best = emp
    return best


# Global usage tracking (reservations made in this roadmap, to avoid double-assigning)
_usage: dict[tuple[str, date], float] = {}


def _reset_usage():
    _usage.clear()


def _schedule_hours(r: Roster, emp_id: str, from_date: date, hours: float) -> tuple[date, date]:
    """Consumes hours from a person day by day from from_date until complete.
    Records usage in _usage so subsequent tasks respect previous reservations."""
    remaining = hours
    start: date | None = None
    last: date | None = None
    d = _next_working_day(r, from_date)
    safety = 0
    while remaining > 0.01:
        safety += 1
        if safety > 3650:
            raise RuntimeError(f"Loop in _schedule_hours for {emp_id}")
        free_day = r.available_hours(emp_id, d) - _usage.get((emp_id, d), 0.0)
        if free_day > 0.01:
            use = min(remaining, free_day)
            _usage[(emp_id, d)] = _usage.get((emp_id, d), 0.0) + use
            remaining -= use
            if start is None:
                start = d
            last = d
        d += timedelta(days=1)
        while not r.is_working_day(d):
            d += timedelta(days=1)

    assert start is not None and last is not None
    return start, last


# ---------------- entry point ----------------

def build_roadmap(
    input_data: dict,
    catalog: Catalog,
    roster: Roster,
) -> Roadmap:
    _reset_usage()
    project = input_data["project"]
    desired_date = date.fromisoformat(str(input_data["desired_start_date"]))

    # Filter employees by input (if restricted)
    if "employee_ids" in input_data and input_data["employee_ids"]:
        emp_ids = set(input_data["employee_ids"])
    else:
        emp_ids = set(roster.employees.keys())

    mult_dif = catalog.multipliers["difficulty"]

    # Expansion
    exp: list[dict] = []
    exp += _expand_items(input_data.get("pages", []), catalog.pages, mult_dif)
    exp += _expand_items(input_data.get("features", []), catalog.features, mult_dif)
    exp += _expand_items(input_data.get("integrations", []), catalog.integrations, mult_dif)

    # Calculate base_hours x ideal_hours_per_unit for each expanded atomic task
    for t in exp:
        atomic = catalog.atomic[t["atomic_id"]]
        t["ideal_hours_total"] = atomic.base_hours * t["ideal_hours_per_unit"]

    # Group hours by department
    hours_by_dept: dict[str, float] = {}
    hours_by_element: dict[str, float] = {}
    for t in exp:
        dept = catalog.atomic[t["atomic_id"]].department
        hours_by_dept[dept] = hours_by_dept.get(dept, 0.0) + t["ideal_hours_total"]
        hours_by_element[t["element_name"]] = (
            hours_by_element.get(t["element_name"], 0.0) + t["ideal_hours_total"]
        )

    # Start date shifting based on the first phase
    phases = [f for f in catalog.dependencies if not f.get("optional") or f["id"] != "qa"]
    first_phase = phases[0]
    initial_dept = first_phase["departments"][0]
    effective_start_date, reason = _find_shift_start(roster, initial_dept, desired_date, emp_ids)
    shift = (effective_start_date - desired_date).days

    # Sequence phases respecting dependencies
    phase_end_by_id: dict[str, date] = {}
    all_assignments: list[TaskAssignment] = []
    phases_summary = []
    warnings: list[str] = []

    for phase in phases:
        if phase.get("optional"):
            continue  # QA only if explicitly requested (not in MVP)

        # Determine the date from which this phase can start
        deps = phase.get("depends_on", [])
        if deps:
            from_date = max(phase_end_by_id[d] for d in deps) + timedelta(days=1)
            from_date = _next_working_day(roster, from_date)
        else:
            from_date = effective_start_date

        # Hours by department for this phase
        phase_hours_by_dept = {
            d: sum(
                t["ideal_hours_total"]
                for t in exp
                if catalog.atomic[t["atomic_id"]].department == d
            )
            for d in phase["departments"]
        }

        phase_tasks = [
            t for t in exp
            if catalog.atomic[t["atomic_id"]].department in phase["departments"]
        ]

        if sum(phase_hours_by_dept.values()) == 0:
            phase_end_by_id[phase["id"]] = from_date
            continue

        assignments, phase_end = _assign_phase(
            roster, phase, phase_hours_by_dept, phase_tasks, catalog, emp_ids, from_date,
        )
        all_assignments.extend(assignments)
        phase_end_by_id[phase["id"]] = phase_end

        phases_summary.append(
            {
                "phase": phase["name"],
                "start": from_date.isoformat(),
                "end": phase_end.isoformat(),
                "hours": round(sum(a.hours for a in assignments), 2),
            }
        )

    end_date = max(phase_end_by_id.values()) if phase_end_by_id else effective_start_date

    return Roadmap(
        project=project,
        desired_start_date=desired_date,
        effective_start_date=effective_start_date,
        end_date=end_date,
        shift_days=shift,
        shift_reason=reason,
        tasks=sorted(all_assignments, key=lambda a: (a.start, a.department)),
        phases_summary=phases_summary,
        hours_by_dept={k: round(v, 2) for k, v in hours_by_dept.items()},
        hours_by_element={k: round(v, 2) for k, v in hours_by_element.items()},
        warnings=warnings,
        feature=input_data.get("feature", ""),
    )
