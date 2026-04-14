---
name: sales-roadmap
description: Estimación de tiempos y armado de roadmap para proyectos de desarrollo de producto. Úsala cuando el usuario pida estimar un proyecto, armar un roadmap para un cliente, calcular cuánto tarda un desarrollo en base a páginas/features/integraciones, o planificar la asignación del equipo. Cruza los requerimientos contra la nómina real del estudio y las asignaciones vigentes para producir un cronograma tipo Gantt con personas asignadas por nombre.
---

# Estimador de roadmap de producto

Esta skill produce un roadmap de desarrollo tipo Gantt, con fechas, asignaciones nominales y cronograma respetando dependencias entre fases (Discovery → Diseño → Arquitectura → Backend+Frontend en paralelo).

## Cuándo usarla

- "Armame un roadmap para este proyecto"
- "¿Cuánto tarda esto?"
- "Estimemos este proyecto para pasarle al cliente"
- "¿Cuándo podemos arrancar con este proyecto dado el equipo que tenemos?"

## Cómo funciona

1. **Source of truth** — los tiempos base están en `data/` (atomic-tasks, pages, features, integrations) y el equipo en `roster/` (employees, allocations).
2. **Input del usuario** — JSON con páginas, features, integraciones (con dificultad `baja`/`media`/`alta` y cantidad) y `fecha_inicio_deseada`.
3. **Scheduler** — expande elementos a tareas atómicas, asigna personas según disponibilidad real, corre la fecha si el equipo está saturado.
4. **Output** — un Markdown con resumen, horas por depto, asignaciones nominales, Gantt Mermaid y detalle de tareas.

## Workflow

Cuando el usuario te pida estimar un proyecto:

1. **Recolectar el input** conversando con el usuario. Si falta algo, preguntá:
   - Nombre del cliente / lead (campo `cliente`) — define la carpeta de salida
   - Nombre del proyecto (campo `proyecto`)
   - Fecha deseada de inicio (formato `YYYY-MM-DD`)
   - Páginas, features, integraciones: para cada una, `id` del catálogo + dificultad + cantidad
   - (Opcional) `empleados_id` si querés restringir el equipo

   Los IDs válidos están en:
   - `data/pages.yaml` (ej: `page.login`, `page.dashboard_simple`)
   - `data/features.yaml` (ej: `feature.notifications`, `feature.roles_permissions`)
   - `data/integrations.yaml` (ej: `integration.stripe`, `integration.sendgrid`)

   Si el usuario menciona algo que no está en el catálogo, **preguntale** si podés agregarlo a los YAMLs antes de seguir.

2. **Guardar el input** como `examples/<slug-del-proyecto>.json` o usar uno existente.

3. **Correr**:
   ```bash
   cd .claude/skills/sales-roadmap
   uv run --with pyyaml --with markdown-pdf python scripts/estimate.py examples/<archivo>.json
   ```
   Esto genera dos archivos en `roadmaps/<cliente_slug>/<proyecto_slug>-<timestamp>.{md,pdf}`.

4. **Mostrar el resultado** al usuario: indicarle la ruta del PDF generado y pegar el contenido del Markdown (con el Gantt Mermaid). Los roadmaps quedan archivados por cliente en la carpeta `roadmaps/` de la skill.

5. **Revisar supuestos** — señalar corrimiento de fecha si lo hubo, advertencias, horas totales por departamento.

## Mantenimiento

- **Nuevo empleado**: agregar en `roster/employees.yaml`.
- **Empleado asignado a un proyecto**: agregar en `roster/allocations.yaml`.
- **Nueva integración/feature/página recurrente**: agregar en el catálogo correspondiente de `data/`.
- **Calibrar tiempos base**: editar `horas_base` en `data/atomic-tasks.yaml` según aprendizaje de proyectos reales.
- **Actualizar feriados**: al terminar el año, extender `data/holidays-ar.yaml`.

## Validación

Antes de correr con un input nuevo, conviene verificar:
```bash
python scripts/catalog.py --validate
python scripts/roster.py --validate
```

## Dependencias

- Python 3.10+
- `pyyaml` + `markdown-pdf` (se instalan on-demand con `uv run --with`)

## Escala de dificultad

| Nivel | Multiplicador | Cuándo usar |
|---|---|---|
| baja | x1.0 | Caso estándar, sin sorpresas |
| media | x1.8 | Validaciones custom, lógica moderada, UX no trivial |
| alta | x3.0 | Estado complejo, realtime, compliance, muchas reglas de negocio |

## Supuestos implícitos

- 5 días laborales/semana, 8h/día, 6h productivas (75%).
- Feriados AR 2026-2028 cargados.
- Seniority: Junior x1.5, Semi x1.0, Senior x0.7 sobre horas base.
- Fases secuenciales: Discovery → Diseño → Arquitectura → (Backend || Frontend). QA no está en MVP.
