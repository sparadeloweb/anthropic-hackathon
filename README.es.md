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

**Funcionalidades:**
- Pregunta si necesita backend (Laravel API) antes de scaffoldear
- Lee el HTML de Stitch y divide en componentes atomicos (`ui/`), bloques compuestos y layout
- Server Components por defecto — `'use client'` solo cuando es necesario
- Sigue las 70 reglas de [vercel-react-best-practices](https://github.com/vercel-labs/agent-skills) (waterfalls, bundle, server-side, re-renders)
- Sigue [next-best-practices](https://github.com/vercel-labs/next-skills) (App Router, RSC, data patterns, image/font)
- Backend Laravel sigue [laravel-specialist](https://github.com/jeffallan/claude-skills) (Eloquent, API Resources, Pest, >85% coverage)
- Tests E2E con Playwright (frontend), tests de feature con Pest (backend)
- Levanta dev server y ofrece tunnel publico (Cloudflare/Vercel)
- Genera documentacion del proyecto en Notion via MCP

**Uso:**
```
/dev-from-design-to-code
```

**Estructura:**
```
.claude/skills/dev-from-design-to-code/
├── SKILL.md              # Workflow principal (8 pasos)
├── REACT-RULES.md        # 70 reglas de Vercel (8 categorias)
├── NEXTJS-RULES.md       # App Router, RSC, data patterns, image/font
└── LARAVEL-RULES.md      # laravel-specialist completo (templates, checkpoints, MCP)
```

**Requiere:** Node.js 18+, Stitch MCP, Notion MCP. Laravel: PHP 8.2+, Composer.

### `/dev-deploy`

Despliega frontend a Vercel y/o backend a Laravel Cloud. Ejecuta checks pre-deploy, despliega via MCP o CLI, verifica produccion, y genera documentacion de deploy en Notion si no existe.

**Funcionalidades:**
- Auto-detecta tipo de proyecto (Next.js, Laravel, o ambos)
- Checks pre-deploy: build, lint, tests Playwright, tests Pest
- Frontend: despliega via Vercel MCP (OAuth) o Vercel CLI
- Backend: despliega via Laravel Cloud CLI o SSH manual
- Configura variables de entorno en el target de deploy
- Verifica que la URL de produccion carga y los flujos criticos funcionan
- Genera/actualiza guia de deploy en Notion con URLs, env vars, pasos de rollback

**Uso:**
```
/dev-deploy
```

**Estructura:**
```
.claude/skills/dev-deploy/
├── SKILL.md              # Workflow principal (6 pasos)
└── SETUP-DEPLOY.md       # Setup de Vercel MCP, Vercel CLI, Laravel Cloud
```

**Requiere:** Vercel MCP o CLI. Laravel Cloud CLI para backend. Notion MCP para docs.

### `/dev-add-feature`

Agrega features o corrige bugs en codigo existente. Crea workflow de git con branches, commits y PRs via GitHub CLI. Actualiza documentacion en Notion.

**Funcionalidades:**
- Verifica que `gh` CLI este instalado y autenticado — guia el setup si no
- Pregunta: tipo de cambio (feature, bug fix, refactor, perf), descripcion, criterios de aceptacion
- Crea branch con naming convencional (`feat/`, `fix/`, `refactor/`, `perf/`)
- Implementa cambios siguiendo patrones del proyecto (reglas React, reglas Laravel)
- Corre suite completa de tests antes de commitear
- Crea PR via `gh pr create` con summary, test plan y Co-Authored-By
- Actualiza documentacion en Notion si cambio el comportamiento

**Uso:**
```
/dev-add-feature
```

**Estructura:**
```
.claude/skills/dev-add-feature/
├── SKILL.md              # Workflow principal (6 pasos)
└── SETUP-GITHUB.md       # Instalacion, auth y verificacion de gh CLI
```

**Requiere:** `gh` CLI instalado y autenticado. Git remote configurado.

### `/dev-review-pr`

Revisa pull requests por calidad de codigo, performance, seguridad y mejores practicas. Postea comentarios de review directamente en GitHub via `gh` CLI.

**Funcionalidades:**
- Carga contexto completo del PR: diff, archivos cambiados, comentarios, descripcion
- Lee cada archivo cambiado en contexto completo (no solo el diff)
- Chequea archivos React/Next.js contra REACT-CHECKLIST.md (performance, arquitectura, data fetching, seguridad, a11y, testing)
- Chequea archivos Laravel contra LARAVEL-CHECKLIST.md (seguridad, arquitectura, database, calidad, testing)
- Niveles de severidad: must fix, should fix, suggestion, nitpick
- Postea comentarios inline en lineas especificas via `gh api`
- Aprueba o pide cambios con body de review estructurado

**Uso:**
```
/dev-review-pr 123
```

**Estructura:**
```
.claude/skills/dev-review-pr/
├── SKILL.md              # Workflow principal (4 pasos)
├── REACT-CHECKLIST.md    # Checklist de review React/Next.js
├── LARAVEL-CHECKLIST.md  # Checklist de review Laravel
└── SETUP-GITHUB.md       # Setup de GitHub CLI
```

**Requiere:** `gh` CLI instalado y autenticado. Acceso al repositorio.

### `/dev-tunnels`

Gestiona tunnels publicos para servidores de desarrollo local. Crea, lista y cierra tunnels.

**Funcionalidades:**
- Lista todos los tunnels activos (Cloudflare, Vercel Dev, ngrok, localtunnel)
- Crea nuevos tunnels en cualquier puerto con eleccion de proveedor
- Cloudflare recomendado (gratis, sin cuenta, funciona via npx)
- Cierra tunnels por PID, puerto, o todos a la vez
- Limpia archivos de log de tunnels

**Uso:**
```
/dev-tunnels
```

**Estructura:**
```
.claude/skills/dev-tunnels/
└── SKILL.md              # Comandos: list, create, close
```
