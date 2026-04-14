---
name: creating-skills
description: Creates new Claude Code skills following Agent Skills best practices. Use when the user wants to create a new skill, custom command, slash command, or extend Claude's capabilities with reusable instructions.
allowed-tools: Bash(mkdir *) Read Write Edit Glob Grep
---

# Creating Skills

Create a new skill by following this workflow. Each step validates before proceeding.

## Workflow

Copy this checklist and track progress:

```
Skill Creation Progress:
- [ ] Step 1: Gather requirements
- [ ] Step 2: Design skill structure
- [ ] Step 3: Write SKILL.md with frontmatter
- [ ] Step 4: Create supporting files (if needed)
- [ ] Step 5: Validate the skill
- [ ] Step 6: Test the skill
```

### Step 1: Gather requirements

Determine from the user or context:

1. **What does the skill do?** One clear purpose.
2. **Who invokes it?** User-only (`disable-model-invocation: true`), Claude-only (`user-invocable: false`), or both (default).
3. **Scope:** Personal (`~/.claude/skills/`) or project (`.claude/skills/`)?
4. **Does it need supporting files?** Scripts, templates, reference docs?
5. **Does it need dynamic context?** Use `` !`command` `` syntax for shell injection.
6. **Should it run in a subagent?** Use `context: fork` for isolated tasks.

### Step 2: Design skill structure

**Simple skill** (instructions only):
```
skill-name/
└── SKILL.md
```

**Complex skill** (with supporting files):
```
skill-name/
├── SKILL.md              # Main instructions (under 500 lines)
├── reference.md          # Detailed docs (loaded as needed)
├── examples.md           # Usage examples
└── scripts/
    └── helper.py         # Utility scripts (executed, not loaded)
```

Rules:
- Keep references **one level deep** from SKILL.md
- Name files descriptively: `form_validation_rules.md`, not `doc2.md`
- Use forward slashes in all paths, never backslashes
- Reference supporting files from SKILL.md so Claude knows when to load them

### Step 3: Write SKILL.md

Use the template in [TEMPLATE.md](TEMPLATE.md) as a starting point. Key rules:

**Frontmatter:**
- `name`: lowercase letters, numbers, hyphens only. Max 64 chars. Use gerund form (`processing-pdfs`) or action form (`process-pdfs`). Never use "anthropic" or "claude" in the name.
- `description`: Write in **third person**. Include what AND when. Max 1024 chars. Front-load the key use case.
- Add `disable-model-invocation: true` for skills with side effects (deploy, send messages).
- Add `context: fork` and optionally `agent: Explore|Plan` for isolated execution.
- Add `allowed-tools` to pre-approve tools the skill needs.

**Body content:**
- Be concise. Claude is smart -- only add context it doesn't already have.
- Use consistent terminology throughout.
- Provide a default approach, not multiple options.
- For complex tasks, include a checklist workflow with feedback loops.
- No time-sensitive information.
- Include concrete examples, not abstract descriptions.
- Reference supporting files with links: `See [reference.md](reference.md) for details`

For the full frontmatter reference, see [FRONTMATTER-REFERENCE.md](FRONTMATTER-REFERENCE.md).

### Step 4: Create supporting files (if needed)

Split content when SKILL.md approaches 500 lines. Organize by domain:

- **Reference docs**: API schemas, conventions, domain knowledge
- **Templates**: Output formats for Claude to fill in
- **Scripts**: Deterministic operations Claude should execute, not generate
- **Examples**: Input/output pairs showing expected behavior

Scripts should handle errors explicitly and document any "magic" constants.

### Step 5: Validate the skill

Run through this checklist. See [CHECKLIST.md](CHECKLIST.md) for the full version.

Critical checks:
1. `name` follows naming rules (lowercase, hyphens, no reserved words)
2. `description` is third-person, specific, includes when to use
3. SKILL.md body is under 500 lines
4. All file references are one level deep
5. No Windows-style backslash paths
6. No vague names (`helper`, `utils`, `tools`)

### Step 6: Test the skill

1. **Direct invocation**: Type `/skill-name` and verify it loads
2. **Auto-discovery** (if not `disable-model-invocation`): Ask something matching the description
3. **Check available skills**: Ask "What skills are available?" and confirm it appears
4. **Test with arguments**: If the skill uses `$ARGUMENTS`, test with sample input
5. **Edge cases**: Test with missing arguments, unusual input

If the skill doesn't trigger, strengthen the description keywords.

## Scope decision guide

| Scenario | Location | Why |
|---|---|---|
| Personal workflow (deploy, commit) | `~/.claude/skills/` | Available in all projects |
| Project convention (testing, linting) | `.claude/skills/` | Shared via version control |
| Team/org standard | Managed settings or plugin | Centrally managed |
| Monorepo package-specific | `packages/x/.claude/skills/` | Auto-discovered from subdirs |

## Quick reference: string substitutions

| Variable | Description |
|---|---|
| `$ARGUMENTS` | All arguments passed to the skill |
| `$ARGUMENTS[N]` or `$N` | Specific argument by 0-based index |
| `${CLAUDE_SESSION_ID}` | Current session ID |
| `${CLAUDE_SKILL_DIR}` | Directory containing this SKILL.md |
