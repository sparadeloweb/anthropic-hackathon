"""Carga y valida los YAMLs del catálogo (tareas atómicas, páginas, features, integraciones)
y los archivos de configuración (config, multipliers, dependencies)."""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@dataclass
class AtomicTask:
    id: str
    nombre: str
    departamento: str
    horas_base: float


@dataclass
class CatalogItem:
    id: str
    nombre: str
    tareas: list[dict]  # [{id, cantidad}]


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
        item = CatalogItem(id=entry["id"], nombre=entry["nombre"], tareas=entry["tareas"])
        if item.id in items:
            raise ValueError(f"ID duplicado en {path.name}: {item.id}")
        items[item.id] = item
    return items


def load_catalog(data_dir: Path = DATA_DIR) -> Catalog:
    atomic_raw = _load_yaml(data_dir / "atomic-tasks.yaml") or []
    atomic: dict[str, AtomicTask] = {}
    for entry in atomic_raw:
        t = AtomicTask(**entry)
        if t.id in atomic:
            raise ValueError(f"Tarea atómica duplicada: {t.id}")
        atomic[t.id] = t

    pages = _load_catalog_file(data_dir / "pages.yaml")
    features = _load_catalog_file(data_dir / "features.yaml")
    integrations = _load_catalog_file(data_dir / "integrations.yaml")

    multipliers = _load_yaml(data_dir / "multipliers.yaml")
    config = _load_yaml(data_dir / "config.yaml")
    dependencies = _load_yaml(data_dir / "dependencies.yaml")["fases"]

    cat = Catalog(atomic, pages, features, integrations, multipliers, config, dependencies)
    _validate(cat)
    return cat


def _validate(cat: Catalog) -> None:
    errors: list[str] = []
    for coll_name, coll in [("pages", cat.pages), ("features", cat.features), ("integrations", cat.integrations)]:
        for item in coll.values():
            for t in item.tareas:
                if t["id"] not in cat.atomic:
                    errors.append(f"{coll_name}/{item.id}: referencia tarea inexistente '{t['id']}'")
                if t.get("cantidad", 1) <= 0:
                    errors.append(f"{coll_name}/{item.id}: cantidad inválida en {t['id']}")

    for k in ("dificultad", "seniority"):
        if k not in cat.multipliers:
            errors.append(f"multipliers.yaml: falta clave '{k}'")

    for k in ("horas_por_dia", "productividad", "dias_laborables", "pais_feriados"):
        if k not in cat.config:
            errors.append(f"config.yaml: falta clave '{k}'")

    if errors:
        raise ValueError("Errores en catálogo:\n  - " + "\n  - ".join(errors))


def main() -> int:
    if "--validate" in sys.argv:
        try:
            cat = load_catalog()
        except Exception as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            return 1
        print(
            f"[OK] Catálogo válido: "
            f"{len(cat.atomic)} atómicas, {len(cat.pages)} páginas, "
            f"{len(cat.features)} features, {len(cat.integrations)} integraciones."
        )
        return 0
    print("Uso: python catalog.py --validate")
    return 2


if __name__ == "__main__":
    sys.exit(main())
