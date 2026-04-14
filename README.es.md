# anthropic-hackathon

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
