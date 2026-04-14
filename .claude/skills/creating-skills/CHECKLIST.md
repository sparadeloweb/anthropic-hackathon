# Skill Quality Checklist

Validate every new skill against this checklist before considering it complete.

## Frontmatter

- [ ] `name` is lowercase, hyphens only, max 64 chars
- [ ] `name` uses gerund (`analyzing-data`) or action form (`analyze-data`)
- [ ] `name` does not contain "anthropic" or "claude"
- [ ] `name` is not vague (`helper`, `utils`, `tools`)
- [ ] `description` is non-empty, max 1024 chars
- [ ] `description` is written in third person
- [ ] `description` states what the skill does AND when to use it
- [ ] `description` front-loads the key use case
- [ ] `description` includes keywords users would naturally say
- [ ] `disable-model-invocation: true` set for skills with side effects
- [ ] `allowed-tools` lists tools the skill needs without prompting

## Content quality

- [ ] SKILL.md body is under 500 lines
- [ ] Only adds context Claude doesn't already have
- [ ] Uses consistent terminology (one term per concept)
- [ ] Provides one default approach, not multiple options
- [ ] Examples are concrete, not abstract
- [ ] No time-sensitive information
- [ ] No unnecessary explanations of common concepts

## Structure

- [ ] All file references are one level deep from SKILL.md
- [ ] Supporting files are named descriptively
- [ ] All paths use forward slashes
- [ ] Reference files have table of contents if over 100 lines
- [ ] Scripts handle errors explicitly (not punting to Claude)
- [ ] Scripts document any non-obvious constants

## Workflows (if applicable)

- [ ] Complex tasks have step-by-step checklists
- [ ] Feedback loops included (validate -> fix -> repeat)
- [ ] Decision points have clear conditional paths
- [ ] Critical operations have validation before execution

## Testing

- [ ] Direct invocation works (`/skill-name`)
- [ ] Auto-discovery works (if not `disable-model-invocation`)
- [ ] Arguments work correctly (if using `$ARGUMENTS`)
- [ ] Skill appears in "What skills are available?"
- [ ] Supporting files load when referenced
