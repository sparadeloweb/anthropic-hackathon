# Frontmatter Reference

Complete reference for all YAML frontmatter fields available in SKILL.md.

## Fields

| Field | Required | Description |
|---|---|---|
| `name` | No | Display name and `/slash-command`. Lowercase, numbers, hyphens. Max 64 chars. Defaults to directory name. |
| `description` | Recommended | What the skill does and when to use it. Third person. Max 1024 chars. |
| `when_to_use` | No | Additional trigger context. Appended to `description`. Combined text capped at 1536 chars. |
| `argument-hint` | No | Hint shown during autocomplete. Example: `[issue-number]` or `[filename] [format]`. |
| `disable-model-invocation` | No | `true` prevents Claude from auto-loading. User must invoke with `/name`. Default: `false`. |
| `user-invocable` | No | `false` hides from `/` menu. Use for background knowledge. Default: `true`. |
| `allowed-tools` | No | Tools Claude can use without approval when skill is active. Space-separated or YAML list. |
| `model` | No | Model override when skill is active. |
| `effort` | No | Effort level: `low`, `medium`, `high`, `max` (Opus only). |
| `context` | No | `fork` runs in isolated subagent context. |
| `agent` | No | Subagent type when `context: fork`. Options: `Explore`, `Plan`, `general-purpose`, or custom from `.claude/agents/`. |
| `hooks` | No | Hooks scoped to skill lifecycle. |
| `paths` | No | Glob patterns limiting when skill activates. Comma-separated or YAML list. |
| `shell` | No | Shell for inline commands: `bash` (default) or `powershell`. |

## Invocation control matrix

| Configuration | User can invoke | Claude can invoke |
|---|---|---|
| (default) | Yes | Yes |
| `disable-model-invocation: true` | Yes | No |
| `user-invocable: false` | No | Yes |

## allowed-tools examples

```yaml
# Single tool
allowed-tools: Read

# Multiple tools
allowed-tools: Read Write Edit Bash(git *)

# Bash with specific commands
allowed-tools: Bash(npm test *) Bash(npm run build *)

# YAML list form
allowed-tools:
  - Read
  - Write
  - Bash(git *)
```
