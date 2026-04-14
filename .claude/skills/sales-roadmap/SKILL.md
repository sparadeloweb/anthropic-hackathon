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
- "Agregale una feature al roadmap de este cliente"

## Cómo funciona

1. **Source of truth** — los tiempos base están en `data/` (atomic-tasks, pages, features, integrations) y el equipo en `roster/` (employees, allocations).
2. **Input del usuario** — JSON con páginas, features, integraciones (con dificultad `baja`/`media`/`alta` y cantidad) y `fecha_inicio_deseada`.
3. **Scheduler** — expande elementos a tareas atómicas, asigna personas según disponibilidad real, corre la fecha si el equipo está saturado.
4. **Output** — un Markdown con resumen, horas por depto, asignaciones nominales, Gantt Mermaid y detalle de tareas. Se guarda en `<repo_root>/roadmaps/<cliente_slug>/` (misma convención que `stitch_designs/`).

## Workflow

Cuando el usuario invoque esta skill, **siempre empezar preguntando el modo**:

> ¿Querés crear un **roadmap para un proyecto nuevo** (desde un diseño de Stitch existente) o agregar una **feature nueva a un proyecto existente**?

---

### Modo A — Proyecto nuevo (desde Stitch)

Usar cuando se va a estimar un proyecto completo por primera vez, típicamente a partir de un diseño ya generado en Stitch.

1. **Detectar diseños disponibles** — listar las carpetas dentro de `<repo_root>/stitch_designs/` y mostrarle al usuario los leads disponibles (leer el campo `leadName` de cada `stitch_project.json`).

2. **El usuario elige un lead** — con el `stitch_project.json` seleccionado, extraer:
   - `leadName` → campo `cliente` del input
   - Nombre de la carpeta de `stitch_designs/` → campo `cliente_slug` del input (para que la carpeta de `roadmaps/` coincida exactamente)
   - `screens[]` → mapear **cada pantalla del diseño** a un `page.*` del catálogo (`data/pages.yaml`). El roadmap debe reflejar **únicamente** lo que existe en el diseño de Stitch — no agregar páginas, features ni integraciones que no estén en el mockup. Usar este mapeo orientativo:
     - home / landing → `page.landing`
     - login → `page.login`
     - register → `page.register`
     - dashboard → `page.dashboard_simple` o `page.dashboard_advanced`
     - listado / list → `page.list_view`
     - detalle / detail → `page.detail_view`
     - perfil / profile → `page.profile`
     - settings / configuración → `page.settings`
     - contacto → `page.landing` (variante sencilla)
     - nosotros / about → `page.landing` (variante sencilla)
     - servicios → `page.list_view` (variante)
     - opiniones / reviews → `page.detail_view` (variante)
   - Si una pantalla no encaja en ningún `page.*`, preguntar al usuario.

3. **Mostrar el mapeo y confirmar** con el usuario antes de seguir:
   - Presentar la tabla de pantallas del diseño → pages del catálogo
   - Preguntar nombre del proyecto (campo `proyecto`)
   - Preguntar fecha deseada de inicio (formato `YYYY-MM-DD`)
   - Confirmar/ajustar las dificultades de cada página
   - **Solo si el usuario lo pide**, agregar features (`data/features.yaml`) o integraciones (`data/integrations.yaml`) extras que no estén en el diseño
   - (Opcional) `empleados_id` si se quiere restringir el equipo

4. **Guardar el input** como `examples/<slug-del-proyecto>.json`.

5. **Correr**:
   ```bash
   cd .claude/skills/sales-roadmap
   uv run --with pyyaml --with markdown-pdf python scripts/estimate.py examples/<archivo>.json
   ```
   Genera: `roadmaps/<cliente_slug>/<proyecto_slug>.{md,pdf}`.

6. **Mostrar el resultado** al usuario: indicarle la ruta del PDF generado y pegar el contenido del Markdown (con el Gantt Mermaid).

7. **Revisar supuestos** — señalar corrimiento de fecha si lo hubo, advertencias, horas totales por departamento.

---

### Modo B — Feature nueva para proyecto existente

Usar cuando el cliente ya tiene un proyecto estimado y se quiere agregar una funcionalidad nueva. Genera un roadmap separado enfocado solo en la feature, archivado en la misma carpeta del cliente.

1. **Identificar el lead/cliente** — listar las carpetas existentes en `roadmaps/` y/o `stitch_designs/` para que el usuario elija el cliente. Si el usuario ya lo mencionó, usar ese. Usar el nombre de la carpeta existente como campo `cliente_slug` del input para mantener la misma carpeta.

2. **Recolectar los datos de la feature** conversando con el usuario:
   - Nombre de la feature (campo `feature`) — define el prefijo del archivo de salida
   - Nombre del proyecto original (campo `proyecto`) — se muestra en el título
   - Fecha deseada de inicio (formato `YYYY-MM-DD`)
   - Páginas nuevas que requiere la feature (`data/pages.yaml`)
   - Features del catálogo que apliquen (`data/features.yaml`)
   - Integraciones nuevas que requiera (`data/integrations.yaml`)
   - Dificultad y cantidad para cada elemento
   - (Opcional) `empleados_id` si se quiere restringir el equipo

3. **Guardar el input** como `examples/<slug-cliente>-<slug-feature>.json`. El JSON debe incluir el campo `feature`:
   ```json
   {
     "cliente": "Nombre del cliente",
     "cliente_slug": "nombre-carpeta-existente",
     "proyecto": "Nombre del proyecto original",
     "feature": "Nombre de la feature nueva",
     "fecha_inicio_deseada": "YYYY-MM-DD",
     "paginas": [...],
     "features": [...],
     "integraciones": [...]
   }
   ```

4. **Correr** igual que el modo A:
   ```bash
   cd .claude/skills/sales-roadmap
   uv run --with pyyaml --with markdown-pdf python scripts/estimate.py examples/<archivo>.json
   ```
   Genera: `roadmaps/<cliente_slug>/<feature_slug>.{md,pdf}` (nótese que usa el nombre de la feature como prefijo, no el del proyecto).

5. **Mostrar el resultado** al usuario y revisar supuestos.

---

### Notas comunes a ambos modos

- Los IDs válidos están en:
  - `data/pages.yaml` (ej: `page.login`, `page.dashboard_simple`)
  - `data/features.yaml` (ej: `feature.notifications`, `feature.roles_permissions`)
  - `data/integrations.yaml` (ej: `integration.stripe`, `integration.sendgrid`)
- Si el usuario menciona algo que no está en el catálogo, **preguntale** si podés agregarlo a los YAMLs antes de seguir.

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
