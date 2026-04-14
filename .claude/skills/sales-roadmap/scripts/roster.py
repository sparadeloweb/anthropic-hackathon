"""Carga el roster y las asignaciones, y expone funciones de disponibilidad por persona y día."""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml

ROSTER_DIR = Path(__file__).resolve().parent.parent / "roster"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@dataclass
class Employee:
    id: str
    nombre: str
    departamento: str
    seniority: str
    dedicacion_default: float


@dataclass
class Allocation:
    empleado_id: str
    proyecto: str
    desde: date
    hasta: date
    dedicacion: float


@dataclass
class Roster:
    employees: dict[str, Employee]
    allocations: list[Allocation]
    holidays: set[date] = field(default_factory=set)
    holiday_names: dict[date, str] = field(default_factory=dict)
    config: dict = field(default_factory=dict)
    multipliers: dict = field(default_factory=dict)

    def is_working_day(self, d: date) -> bool:
        if d.isoweekday() not in self.config["dias_laborables"]:
            return False
        if d in self.holidays:
            return False
        return True

    def allocated_on(self, emp_id: str, d: date) -> float:
        total = 0.0
        for a in self.allocations:
            if a.empleado_id == emp_id and a.desde <= d <= a.hasta:
                total += a.dedicacion
        return total

    def available_hours(self, emp_id: str, d: date) -> float:
        if not self.is_working_day(d):
            return 0.0
        emp = self.employees[emp_id]
        free = emp.dedicacion_default - self.allocated_on(emp_id, d)
        free = max(0.0, min(free, 1.0))
        return free * self.config["horas_por_dia"] * self.config["productividad"]

    def effective_hours(self, emp_id: str, d: date) -> float:
        """Horas disponibles ajustadas a equivalencia Semi (útil para sumar capacidad de equipo)."""
        raw = self.available_hours(emp_id, d)
        mult = self.multipliers["seniority"][self.employees[emp_id].seniority]
        return raw / mult

    def employees_by_dept(self, dept: str) -> list[Employee]:
        return [e for e in self.employees.values() if e.departamento == dept]


def _load_yaml(path: Path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _parse_date(value) -> date:
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def load_roster(
    roster_dir: Path = ROSTER_DIR,
    data_dir: Path = DATA_DIR,
    employees_file: str = "employees.yaml",
    allocations_file: str = "allocations.yaml",
) -> Roster:
    emp_raw = _load_yaml(roster_dir / employees_file) or []
    employees: dict[str, Employee] = {}
    for e in emp_raw:
        emp = Employee(**e)
        if emp.id in employees:
            raise ValueError(f"Empleado duplicado: {emp.id}")
        if emp.seniority not in ("junior", "semi", "senior"):
            raise ValueError(f"Seniority inválido en {emp.id}: {emp.seniority}")
        if not 0 < emp.dedicacion_default <= 1.0:
            raise ValueError(f"dedicacion_default inválida en {emp.id}")
        employees[emp.id] = emp

    alloc_raw = _load_yaml(roster_dir / allocations_file) or []
    allocations: list[Allocation] = []
    for a in alloc_raw:
        alloc = Allocation(
            empleado_id=a["empleado_id"],
            proyecto=a["proyecto"],
            desde=_parse_date(a["desde"]),
            hasta=_parse_date(a["hasta"]),
            dedicacion=float(a["dedicacion"]),
        )
        if alloc.empleado_id not in employees:
            raise ValueError(f"Allocation referencia empleado inexistente: {alloc.empleado_id}")
        if alloc.hasta < alloc.desde:
            raise ValueError(f"Allocation con rango inválido: {alloc.empleado_id} {alloc.proyecto}")
        if not 0 < alloc.dedicacion <= 1.0:
            raise ValueError(f"Dedicacion inválida: {alloc.empleado_id} {alloc.proyecto}")
        allocations.append(alloc)

    config = _load_yaml(data_dir / "config.yaml")
    multipliers = _load_yaml(data_dir / "multipliers.yaml")

    holidays_raw = _load_yaml(data_dir / "holidays-ar.yaml") or {}
    holidays: set[date] = set()
    holiday_names: dict[date, str] = {}
    for year_entries in holidays_raw.values():
        for h in year_entries:
            d = _parse_date(h["fecha"])
            holidays.add(d)
            holiday_names[d] = h["nombre"]

    return Roster(
        employees=employees,
        allocations=allocations,
        holidays=holidays,
        holiday_names=holiday_names,
        config=config,
        multipliers=multipliers,
    )


def main() -> int:
    if "--validate" in sys.argv:
        try:
            r = load_roster()
        except Exception as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            return 1
        print(
            f"[OK] Roster válido: {len(r.employees)} empleados, "
            f"{len(r.allocations)} asignaciones, {len(r.holidays)} feriados."
        )
        return 0
    print("Uso: python roster.py --validate")
    return 2


if __name__ == "__main__":
    sys.exit(main())
