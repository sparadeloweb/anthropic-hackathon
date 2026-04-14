---
name: agency-demo
model: opus
description: Ejecuta el pipeline completo de agencIA como demo end-to-end. Elige un rubro y país al azar, busca leads, genera diseño, roadmap, presupuesto, propuesta y dashboard. Al finalizar, crea CLAUDE.md con la documentación del flujo. Úsala para demostrar el flujo completo de la agencia.
---

# Demo del pipeline completo de agencIA

Esta skill ejecuta todo el pipeline de ventas de principio a fin como demostración, eligiendo un rubro y país al azar.

## Cuándo usarla

- "Hacé una demo del pipeline completo"
- "Probá todo el flujo de la agencia"
- `/agency-demo`

## Pipeline completo

```
1. Lead Generation ──→ 2. Scraping ──→ 3. Report (HTML/JSON)
         │
         ▼
4. Lead Selection (manual) ──→ 5. Design (Stitch) ──→ 6. Assets
         │
         ▼
7. Roadmap ──→ 8. Budget ──→ 9. Proposal ──→ 10. Dashboard Web
```

## Workflow

### Paso 0 — Elegir rubro y país al azar

Elegir al azar uno de cada lista:

**Países** (América y Europa, solo alfabeto latino):
- Argentina, México, Colombia, Chile, Uruguay, España, Portugal, Francia, Italia, Alemania, Países Bajos, Suecia, Noruega, Dinamarca, Finlandia, Polonia, República Checa, Rumania, Hungría, Croacia, Brasil, Perú, Ecuador, Costa Rica, Panamá

**Rubros**:
- Dentistas, Veterinarias, Estudios de arquitectura, Agencias inmobiliarias, Gimnasios, Restaurantes, Peluquerías, Estudios de yoga, Talleres mecánicos, Floristas, Clínicas de fisioterapia, Estudios de fotografía, Escuelas de idiomas, Estudios de abogados, Ópticas, Cafeterías especializadas, Tiendas de bicicletas, Librerías, Estudios de tatuaje, Panaderías artesanales

Mostrar al usuario: "Demo: buscando **[rubro]** en **[ciudad], [país]**"

Usar una ciudad principal del país elegido (capital o ciudad grande).

### Paso 1 — Buscar leads

Ejecutar `/sales-finding-leads` con:
- Query: el rubro elegido + "en" + ciudad, país
- Filtro: solo sin website (para tener leads a los que ofrecerles el servicio)
- Profundidad: rápida (1x1, para no gastar mucho API)

### Paso 2 — Elegir un lead

Del resultado, elegir el primer lead que:
- Tenga al menos 10 reseñas
- Tenga rating >= 4.0
- No tenga website

Si no hay ninguno que cumpla, elegir el primero disponible.

Mostrar al usuario: "Lead seleccionado: **[nombre]** (★[rating], [reseñas] reseñas)"

### Paso 3 — Generar diseño en Stitch

Ejecutar `/design-generating-websites` para el lead seleccionado.

**IMPORTANTE**: Este paso es interactivo — la skill de diseño le va a preguntar al usuario sus preferencias (tipo de proyecto, colores, estilo, etc). Esperar las respuestas antes de continuar.

### Paso 4 — Generar roadmap

Ejecutar `/sales-roadmap` en Modo A (proyecto nuevo desde Stitch):
- Usar el diseño recién generado
- Mapear las pantallas automáticamente
- Fecha de inicio: próximo lunes hábil
- Confirmar con el usuario antes de correr

### Paso 5 — Generar presupuesto

Ejecutar `/sales-pricing`:
- Usar el roadmap recién generado
- Rates por defecto en USD:
  - Backend: $55/h
  - Frontend: $50/h
  - Architecture: $70/h
  - Design: $45/h
  - Project Management: $50/h
  - Product Owner: $60/h

### Paso 6 — Generar propuesta comercial

Ejecutar `/sales-proposal`:
- Usar el lead seleccionado
- Idioma: auto-detectar del país del lead

### Paso 7 — Generar dashboard web

Correr el script de `/sales-proposal-web`:
```bash
cd .claude/skills/sales-proposal-web
python scripts/build_dashboard.py <lead-slug>
```

### Paso 8 — Crear CLAUDE.md

Si todo el pipeline se completó exitosamente, crear un archivo `CLAUDE.md` en la raíz del proyecto con la documentación completa del flujo de agencIA.

El CLAUDE.md debe incluir:

```markdown
# agencIA — Pipeline automático de captación de leads

## Qué es

agencIA es un pipeline automatizado de captación y calificación de leads comerciales, construido como un conjunto de skills de Claude Code que se ejecutan secuencialmente. Transforma una búsqueda geográfica de negocios en una propuesta comercial completa con diseño web, roadmap, presupuesto y dashboard de presentación.

## Pipeline

### 1. `/sales-finding-leads` — Captación de leads
Busca negocios por rubro y zona geográfica usando Google Places API con búsqueda en grilla para superar el límite de 60 resultados. Genera un report HTML interactivo y un JSON con todos los datos.
- **Input**: rubro + zona geográfica
- **Output**: `leads/YYYY-MM-DD/query-slug/{leads_data.json, leads_report.html}`

### 2. `/design-generating-websites` — Diseño web
Genera un diseño web profesional en Google Stitch para un lead seleccionado. Pregunta preferencias de diseño (colores, tipografía, estilo) y descarga los screenshots.
- **Input**: lead seleccionado + preferencias de diseño
- **Output**: `stitch_designs/lead-slug/{stitch_project.json, screens/*.png, design-system/}`

### 3. `/sales-roadmap` — Estimación y roadmap
Estima tiempos de desarrollo cruzando los requerimientos contra la nómina real del equipo. Genera un cronograma Gantt con asignaciones nominales.
- **Input**: pantallas del diseño de Stitch + fecha de inicio
- **Output**: `roadmaps/lead-slug/{proyecto.md, proyecto.pdf}`

### 4. `/sales-pricing` — Presupuesto
Toma el roadmap y aplica tarifas por hora por rol para generar un presupuesto comercial.
- **Input**: roadmap + tarifas por rol
- **Output**: `budgets/lead-slug/{proyecto.md, proyecto.pdf}`

### 5. `/sales-proposal` — Propuesta comercial
Genera un mensaje de propuesta de negocio profesional combinando los datos del lead, el diseño y el roadmap. Auto-detecta el idioma del país del lead.
- **Input**: lead + diseño + roadmap
- **Output**: `proposals/lead-slug/propuesta.txt`

### 6. `/sales-proposal-web` — Dashboard de presentación
Consolida todo el pipeline en un dashboard HTML interactivo con tabs: negocio, diseño, propuesta, presupuesto y roadmap. Autocontenido (imágenes en base64).
- **Input**: todos los outputs anteriores
- **Output**: `proposals/lead-slug/dashboard.html`

## Estructura de carpetas

\```
agencIA/
├── leads/                    # Datos de leads (Google Places API)
├── stitch_designs/           # Diseños web (Stitch)
├── roadmaps/                 # Roadmaps de desarrollo
├── budgets/                  # Presupuestos comerciales
├── proposals/                # Propuestas + dashboards
└── .claude/skills/           # Skills del pipeline
    ├── sales-finding-leads/
    ├── design-generating-websites/
    ├── sales-roadmap/
    ├── sales-pricing/
    ├── sales-proposal/
    ├── sales-proposal-web/
    └── agency-demo/
\```

## Cómo ejecutar el pipeline completo

1. `/sales-finding-leads` — buscar leads
2. Elegir un lead del report HTML
3. `/design-generating-websites` — diseñar el sitio
4. `/sales-roadmap` — estimar tiempos
5. `/sales-pricing` — presupuestar
6. `/sales-proposal` — redactar propuesta
7. `/sales-proposal-web` — generar dashboard
8. Enviar al cliente

O ejecutar `/agency-demo` para una demostración end-to-end con un rubro y país al azar.
```

### Paso 9 — Mostrar resumen

Mostrar al usuario un resumen de todo lo que se generó:

```
✅ Pipeline completo para: [nombre del lead]
   País: [país] | Rubro: [rubro]

   📁 leads/...                  → [N] leads encontrados
   🎨 stitch_designs/[slug]/     → [N] pantallas diseñadas
   📊 roadmaps/[slug]/           → [duración] días laborales
   💰 budgets/[slug]/            → [total] [moneda]
   📝 proposals/[slug]/propuesta → idioma: [idioma]
   🌐 proposals/[slug]/dashboard → dashboard.html
   📖 CLAUDE.md                  → documentación del flujo
```
