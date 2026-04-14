---
name: sales-proposal-web
model: sonnet
description: Genera un dashboard web interactivo que consolida toda la información del pipeline de ventas para un lead — datos del negocio, diseño de Stitch, propuesta comercial, presupuesto y roadmap — en un único archivo HTML con tabs. Úsala cuando el usuario quiera armar la página de presentación para enviarle al cliente.
---

# Dashboard de propuesta comercial

Esta skill genera un archivo HTML autocontenido (dashboard con tabs) que consolida todo el output del pipeline de ventas para un lead en una presentación profesional lista para compartir con el cliente.

## Cuándo usarla

- "Armame la web de propuesta para este lead"
- "Generá el dashboard para enviarle al cliente"
- "Juntame todo lo que tenemos de este lead en una página"
- "Necesito la presentación web para Fernando Bliman"

## Qué incluye el dashboard

El dashboard tiene 5 tabs:

1. **Negocio** — Datos del lead de Google Places API: nombre, tipo de negocio, rating, reseñas, dirección, horarios, fotos del local.
2. **Diseño** — Galería con los screenshots de las pantallas diseñadas en Stitch, nombre del design system, paleta de colores.
3. **Propuesta** — El texto de la propuesta comercial generada por `sales-proposal`.
4. **Presupuesto** — Tabla de inversión por rol, total, fases, condiciones (de `sales-pricing`).
5. **Roadmap** — Resumen ejecutivo, fases del proyecto, equipo asignado, duración (de `sales-roadmap`).

## Prerequisitos

Antes de correr esta skill, el lead debe tener:

- [x] Datos del lead en `leads/` (output de `/sales-finding-leads`)
- [x] Diseño en `stitch_designs/<lead>/` (output de `/design-generating-websites`)
- [x] Roadmap en `roadmaps/<lead>/` (output de `/sales-roadmap`)
- [x] Presupuesto en `budgets/<lead>/` (output de `/sales-pricing`)
- [x] Propuesta en `proposals/<lead>/propuesta.txt` (output de `/sales-proposal`)

Si falta alguno, indicarle al usuario qué skill correr primero.

## Workflow

1. **Listar leads disponibles** — buscar leads que tengan las 5 carpetas/archivos necesarios. Mostrar la lista con indicadores de completitud (check/cross por cada prerequisito).

2. **El usuario elige un lead** — o lo indica directamente.

3. **Correr el script**:
   ```bash
   cd .claude/skills/sales-proposal-web
   uv run --with pyyaml python scripts/build_dashboard.py <lead-slug>
   ```
   El script busca automáticamente todos los archivos del lead en las carpetas del repo root.

   Genera: `proposals/<lead-slug>/dashboard.html`

4. **Mostrar la ruta** al usuario e indicarle que puede abrir el HTML en el navegador. Las imágenes de Stitch se embeben en base64 dentro del HTML para que sea totalmente autocontenido y compartible.

## Output

```
proposals/<lead-slug>/
├── propuesta.txt          ← ya existía (de /sales-proposal)
└── dashboard.html         ← generado por esta skill
```

## Dependencias

- Python 3.10+
- `pyyaml` (on-demand con `uv run --with`)
