# anthropic-hackathon

## Setup

```bash
bash setup.sh
```

Esto va a:
1. Verificar Python 3 (instalarlo si no esta, via apt/brew)
2. Crear un entorno virtual (`venv/`)
3. Instalar dependencias de `requirements.txt`
4. Crear `.env` desde `.env.example` si no existe

Luego editar `.env` y agregar las API keys:

```bash
GOOGLE_PLACES_API_KEY=tu-api-key-aqui
```

## Skills

Este proyecto utiliza [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) para extender las capacidades de Claude Code.

### `/creating-skills`

Skill base del proyecto para crear nuevas skills siguiendo las [mejores practicas oficiales](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

**Uso:**

```
/creating-skills nombre-de-skill "descripcion de lo que hace"
```

Incluye:
- Workflow guiado paso a paso con checklist de progreso
- Templates listos para distintos tipos de skill (minimal, subagent, user-only, background knowledge, dynamic context)
- Checklist de validacion de calidad
- Referencia completa de campos frontmatter

**Estructura:**
```
.claude/skills/creating-skills/
├── SKILL.md                  # Instrucciones principales
├── TEMPLATE.md               # Templates reutilizables
├── CHECKLIST.md              # Checklist de calidad
└── FRONTMATTER-REFERENCE.md  # Referencia de frontmatter
```

### `/sales-finding-leads`

Busca leads de negocios usando Google Places API (New) con busqueda profunda basada en grilla que supera el limite de 60 resultados de la API subdividiendo el area geografica.

**Funcionalidades:**
- Busqueda por grilla (5x5 = 25 celdas por defecto) para maximizar resultados
- Filtro opcional: todos los resultados o solo negocios sin sitio web
- Deduplicacion por place ID entre celdas de la grilla
- Datos completos: fotos, reviews, horarios, resumenes editoriales, opciones de pago
- Reporte HTML interactivo (estilo shadcn): tabla compacta con vista detalle al click (fotos, reviews, horarios), busqueda, ordenamiento, filtros y exportacion CSV
- Output organizado: `./leads/YYYY-MM-DD/query-slug/`
- Salida JSON cruda para analisis con IA o procesamiento adicional

**Uso:**
```
/sales-finding-leads
```

Claude preguntara por la consulta de busqueda, preferencia de filtro y profundidad antes de ejecutar.

**Estructura:**
```
.claude/skills/sales-finding-leads/
├── SKILL.md                  # Instrucciones principales
├── SETUP.md                  # Configuracion de API key
├── scripts/
│   └── find_leads.py         # Script de busqueda y generacion de reporte
└── templates/
    └── report_template.html  # Template del reporte HTML
```

**Requiere:** Variable de entorno `GOOGLE_PLACES_API_KEY`. Ver `SETUP.md` para detalles.

### `/design-generating-websites`

Genera un diseno de sitio web en [Google Stitch](https://stitch.withgoogle.com) para **un lead a la vez**. Pregunta preferencias de diseno interactivamente antes de generar, descarga screenshots localmente.

**Funcionalidades:**
- Un lead por ejecucion (invocar de nuevo para otro lead)
- Preferencias interactivas antes de generar: tipo de proyecto, plataforma, colores, modo de color, tono, pedidos especiales
- Tipos de proyecto: **Single Page** (landing), **Multi Page** (sitio con navegacion), o **App** (pantallas mobile)
- Plataformas: Desktop, Mobile-first, App (iOS/Android)
- Analiza fotos, reviews, horarios y tipo de negocio para sugerir paleta y tipografia
- Descarga todas las screenshots a `./stitch_designs/lead-name-slug/`
- Sigue principios de UI/UX premium de [ui-ux-pro-max](https://skills.sh/kimny1143/claude-code-template/ui-ux-pro-max) y [frontend-design](https://skills.sh/anthropics/skills/frontend-design)

**Uso:**
```
/design-generating-websites
```

**Estructura:**
```
.claude/skills/design-generating-websites/
├── SKILL.md                  # Instrucciones principales
├── SETUP-STITCH.md           # Configuracion de Stitch MCP
├── DESIGN-PRINCIPLES.md      # Guia de principios de diseno UI/UX
└── SCREEN-PROMPTS.md         # Templates de prompts por tipo de pantalla
```

**Requiere:** Stitch MCP configurado con API key. Ver `SETUP-STITCH.md` para detalles.

### `/dev-from-design-to-code`

Convierte disenos de Stitch en codigo de produccion: frontend Next.js (React) con backend Laravel API opcional. Pregunta si necesita backend, scaffoldea el proyecto, divide disenos en componentes minimos, escribe tests (Playwright + Pest), instala dependencias, levanta dev server con tunnel publico opcional, y documenta todo en Notion.

### `/dev-deploy`

Despliega frontend a Vercel y/o backend a Laravel Cloud. Ejecuta checks pre-deploy (build, lint, tests), despliega via MCP o CLI, verifica produccion, y genera documentacion de deploy en Notion si no existe.

### `/dev-add-feature`

Agrega features o corrige bugs en codigo existente. Verifica GitHub CLI, crea branches con naming convencional, implementa cambios siguiendo patrones del proyecto, corre tests, crea PRs via `gh`, y actualiza documentacion en Notion.

### `/dev-review-pr`

Revisa pull requests por calidad de codigo, performance, seguridad y mejores practicas. Lee el diff completo, chequea contra checklists de React y Laravel, y postea comentarios de review directamente en GitHub via `gh` CLI.

### `/dev-tunnels`

Gestiona tunnels publicos para servidores de desarrollo local. Crea, lista y cierra tunnels. Soporta Cloudflare (gratis, sin cuenta), Vercel Dev, ngrok y localtunnel.
