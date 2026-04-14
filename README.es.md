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
