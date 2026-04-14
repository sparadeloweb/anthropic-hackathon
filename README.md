# anthropic-hackathon

## Skills

This project uses [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) to extend Claude Code capabilities.

### `/creating-skills`

Base skill for creating new skills following the [official best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

**Usage:**

```
/creating-skills skill-name "description of what it does"
```

Includes:
- Step-by-step guided workflow with progress checklist
- Ready-to-use templates for different skill types (minimal, subagent, user-only, background knowledge, dynamic context)
- Quality validation checklist
- Complete frontmatter field reference

**Structure:**
```
.claude/skills/creating-skills/
├── SKILL.md                  # Main instructions
├── TEMPLATE.md               # Reusable templates
├── CHECKLIST.md              # Quality checklist
└── FRONTMATTER-REFERENCE.md  # Frontmatter reference
```
