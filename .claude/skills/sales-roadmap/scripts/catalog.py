"""Loads and validates the catalog YAMLs (atomic tasks, pages, features, integrations)
and configuration files (config, multipliers, dependencies)."""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@dataclass
class AtomicTask:
    id: str
    name: str
    department: str
    base_hours: float


@dataclass
class CatalogItem:
    id: str
    name: str
    tasks: list[dict]  # [{id, quantity}]


@dataclass
class Catalog:
    atomic: dict[str, AtomicTask]
    pages: dict[str, CatalogItem]
    features: dict[str, CatalogItem]
    integrations: dict[str, CatalogItem]
    multipliers: dict
    config: dict
    dependencies: list[dict]


def _load_yaml(path: Path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_catalog_file(path: Path) -> dict[str, CatalogItem]:
    raw = _load_yaml(path) or []
    items: dict[str, CatalogItem] = {}
    for entry in raw:
        item = CatalogItem(id=entry["id"], name=entry["name"], tasks=entry["tasks"])
        if item.id in items:
            raise ValueError(f"Duplicate ID in {path.name}: {item.id}")
        items[item.id] = item
    return items


def load_catalog(data_dir: Path = DATA_DIR) -> Catalog:
    atomic_raw = _load_yaml(data_dir / "atomic-tasks.yaml") or []
    atomic: dict[str, AtomicTask] = {}
    for entry in atomic_raw:
        t = AtomicTask(**entry)
        if t.id in atomic:
            raise ValueError(f"Duplicate atomic task: {t.id}")
        atomic[t.id] = t

    pages = _load_catalog_file(data_dir / "pages.yaml")
    features = _load_catalog_file(data_dir / "features.yaml")
    integrations = _load_catalog_file(data_dir / "integrations.yaml")

    multipliers = _load_yaml(data_dir / "multipliers.yaml")
    config = _load_yaml(data_dir / "config.yaml")
    dependencies = _load_yaml(data_dir / "dependencies.yaml")["phases"]

    cat = Catalog(atomic, pages, features, integrations, multipliers, config, dependencies)
    _validate(cat)
    return cat


def _validate(cat: Catalog) -> None:
    errors: list[str] = []
    for coll_name, coll in [("pages", cat.pages), ("features", cat.features), ("integrations", cat.integrations)]:
        for item in coll.values():
            for t in item.tasks:
                if t["id"] not in cat.atomic:
                    errors.append(f"{coll_name}/{item.id}: references non-existent task '{t['id']}'")
                if t.get("quantity", 1) <= 0:
                    errors.append(f"{coll_name}/{item.id}: invalid quantity in {t['id']}")

    for k in ("difficulty", "seniority"):
        if k not in cat.multipliers:
            errors.append(f"multipliers.yaml: missing key '{k}'")

    for k in ("hours_per_day", "productivity", "working_days", "holidays_country"):
        if k not in cat.config:
            errors.append(f"config.yaml: missing key '{k}'")

    if errors:
        raise ValueError("Catalog errors:\n  - " + "\n  - ".join(errors))


def main() -> int:
    if "--validate" in sys.argv:
        try:
            cat = load_catalog()
        except Exception as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            return 1
        print(
            f"[OK] Valid catalog: "
            f"{len(cat.atomic)} atomic tasks, {len(cat.pages)} pages, "
            f"{len(cat.features)} features, {len(cat.integrations)} integrations."
        )
        return 0
    print("Usage: python catalog.py --validate")
    return 2


if __name__ == "__main__":
    sys.exit(main())
