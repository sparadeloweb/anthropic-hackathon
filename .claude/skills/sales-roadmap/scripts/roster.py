"""Loads the roster and allocations, and exposes availability functions per person per day."""
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
    name: str
    department: str
    seniority: str
    default_allocation: float


@dataclass
class Allocation:
    employee_id: str
    project: str
    start: date
    end: date
    allocation: float


@dataclass
class Roster:
    employees: dict[str, Employee]
    allocations: list[Allocation]
    holidays: set[date] = field(default_factory=set)
    holiday_names: dict[date, str] = field(default_factory=dict)
    config: dict = field(default_factory=dict)
    multipliers: dict = field(default_factory=dict)

    def is_working_day(self, d: date) -> bool:
        if d.isoweekday() not in self.config["working_days"]:
            return False
        if d in self.holidays:
            return False
        return True

    def allocated_on(self, emp_id: str, d: date) -> float:
        total = 0.0
        for a in self.allocations:
            if a.employee_id == emp_id and a.start <= d <= a.end:
                total += a.allocation
        return total

    def available_hours(self, emp_id: str, d: date) -> float:
        if not self.is_working_day(d):
            return 0.0
        emp = self.employees[emp_id]
        free = emp.default_allocation - self.allocated_on(emp_id, d)
        free = max(0.0, min(free, 1.0))
        return free * self.config["hours_per_day"] * self.config["productivity"]

    def effective_hours(self, emp_id: str, d: date) -> float:
        """Available hours adjusted to Semi equivalence (useful for summing team capacity)."""
        raw = self.available_hours(emp_id, d)
        mult = self.multipliers["seniority"][self.employees[emp_id].seniority]
        return raw / mult

    def employees_by_dept(self, dept: str) -> list[Employee]:
        return [e for e in self.employees.values() if e.department == dept]


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
            raise ValueError(f"Duplicate employee: {emp.id}")
        if emp.seniority not in ("junior", "semi", "senior"):
            raise ValueError(f"Invalid seniority for {emp.id}: {emp.seniority}")
        if not 0 < emp.default_allocation <= 1.0:
            raise ValueError(f"Invalid default_allocation for {emp.id}")
        employees[emp.id] = emp

    alloc_raw = _load_yaml(roster_dir / allocations_file) or []
    allocations: list[Allocation] = []
    for a in alloc_raw:
        alloc = Allocation(
            employee_id=a["employee_id"],
            project=a["project"],
            start=_parse_date(a["from"]),
            end=_parse_date(a["to"]),
            allocation=float(a["allocation"]),
        )
        if alloc.employee_id not in employees:
            raise ValueError(f"Allocation references non-existent employee: {alloc.employee_id}")
        if alloc.end < alloc.start:
            raise ValueError(f"Allocation with invalid range: {alloc.employee_id} {alloc.project}")
        if not 0 < alloc.allocation <= 1.0:
            raise ValueError(f"Invalid allocation: {alloc.employee_id} {alloc.project}")
        allocations.append(alloc)

    config = _load_yaml(data_dir / "config.yaml")
    multipliers = _load_yaml(data_dir / "multipliers.yaml")

    holidays_raw = _load_yaml(data_dir / "holidays-ar.yaml") or {}
    holidays: set[date] = set()
    holiday_names: dict[date, str] = {}
    for year_entries in holidays_raw.values():
        for h in year_entries:
            d = _parse_date(h["date"])
            holidays.add(d)
            holiday_names[d] = h["name"]

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
            f"[OK] Valid roster: {len(r.employees)} employees, "
            f"{len(r.allocations)} allocations, {len(r.holidays)} holidays."
        )
        return 0
    print("Usage: python roster.py --validate")
    return 2


if __name__ == "__main__":
    sys.exit(main())
