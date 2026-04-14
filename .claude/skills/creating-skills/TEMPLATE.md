# SKILL.md Template

Use this template when creating a new skill. Remove comments and unused fields.

## Minimal skill (instructions only)

```yaml
---
name: skill-name
description: Does X when Y. Use when the user asks about Z or works with W files.
---

# Skill Title

Instructions here. Be concise -- only add what Claude doesn't already know.
```

## Standard skill (with configuration)

```yaml
---
name: skill-name
description: Does X when Y. Use when the user asks about Z or works with W files.
argument-hint: [required-arg] [optional-arg]
allowed-tools: Bash(command *) Read Write
---

# Skill Title

## Quick start

Core instructions for the most common use case.

## Workflow

1. First step
2. Second step
3. Validate: run check or review output
4. If validation fails, return to step 2

## Additional resources

- For detailed reference, see [reference.md](reference.md)
- For examples, see [examples.md](examples.md)
```

## User-only skill (manual invocation)

```yaml
---
name: deploy-app
description: Deploy the application to production environment
disable-model-invocation: true
allowed-tools: Bash(npm *) Bash(git *)
---

# Deploy

Deploy $ARGUMENTS to production:

1. Run tests: `npm test`
2. Build: `npm run build`
3. Deploy: `npm run deploy -- $ARGUMENTS`
4. Verify deployment succeeded
```

## Subagent skill (isolated execution)

```yaml
---
name: research-topic
description: Research a topic thoroughly using codebase exploration
context: fork
agent: Explore
---

# Research: $ARGUMENTS

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

## Background knowledge skill (Claude-only)

```yaml
---
name: project-conventions
description: Coding conventions for this project. Use when writing or reviewing code.
user-invocable: false
---

## Conventions

- Use TypeScript strict mode
- Prefer composition over inheritance
- All public functions need JSDoc comments
- Error responses follow RFC 7807
```

## Skill with dynamic context injection

```yaml
---
name: pr-review
description: Review the current pull request
context: fork
agent: Explore
disable-model-invocation: true
allowed-tools: Bash(gh *)
---

## PR Context

- Diff: !`gh pr diff`
- Comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Task

Review this PR for:
1. Correctness
2. Security issues
3. Performance concerns
```
