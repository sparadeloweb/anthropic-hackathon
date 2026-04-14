---
name: dev-review-pr
description: Reviews pull requests for code quality, performance, security, and best practices. Writes review comments via gh CLI. Use when the user wants a PR reviewed, code checked, or quality assessment.
model: opus
allowed-tools: Bash(gh *) Bash(git *) Bash(npx *) Read Glob Grep
---

# Review Pull Request

Reviews a PR for code quality, performance, security, and adherence to best practices. Posts review comments directly on GitHub.

## Prerequisites

- GitHub CLI (`gh`) installed and authenticated
- Access to the repository

## Workflow

```
Review Progress:
- [ ] Step 1: Load PR context
- [ ] Step 2: Analyze changes
- [ ] Step 3: Check against rules
- [ ] Step 4: Write review
```

### Step 1: Load PR context

Get PR details:
```bash
# Get PR info
gh pr view PR_NUMBER

# Get the diff
gh pr diff PR_NUMBER

# Get changed files list
gh pr diff PR_NUMBER --name-only

# Get PR comments/discussion
gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments
```

If the user provides a PR URL, extract owner/repo/number from it.

### Step 2: Analyze changes

Read every changed file in full context (not just the diff). Understand:
- What the PR intends to do
- Which components/modules are affected
- What tests were added or modified

### Step 3: Check against rules

Review using checklists from [REACT-CHECKLIST.md](REACT-CHECKLIST.md) and [LARAVEL-CHECKLIST.md](LARAVEL-CHECKLIST.md) based on file types in the PR.

**For ALL code:**
- [ ] No security vulnerabilities (XSS, SQL injection, command injection)
- [ ] No hardcoded secrets or API keys
- [ ] No console.log / dd() / dump() left in code
- [ ] Error handling is appropriate
- [ ] Changes match PR description

**For React/Next.js files (.tsx, .ts):**
- See [REACT-CHECKLIST.md](REACT-CHECKLIST.md)

**For Laravel files (.php):**
- See [LARAVEL-CHECKLIST.md](LARAVEL-CHECKLIST.md)

**For tests:**
- [ ] Tests cover the happy path
- [ ] Tests cover error cases
- [ ] Tests are not flaky (no timing dependencies)
- [ ] Test descriptions are clear

### Step 4: Write review

Submit review via `gh`:

**If changes are good:**
```bash
gh pr review PR_NUMBER --approve --body "LGTM. Clean implementation, tests cover the key flows."
```

**If changes need work:**
```bash
gh pr review PR_NUMBER --request-changes --body "$(cat <<'EOF'
## Review Summary

Good progress, but a few things to address before merging:

### Must fix
- Description of critical issue

### Suggestions
- Description of improvement

### Nitpicks
- Minor style/preference items
EOF
)"
```

**Post inline comments on specific lines:**
```bash
gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments \
  -f body="Consider using \`Promise.all()\` here to parallelize these independent fetches." \
  -f path="src/app/page.tsx" \
  -f line=42 \
  -f side="RIGHT" \
  -f commit_id="COMMIT_SHA"
```

### Review severity levels

| Level | When to use | Action |
|---|---|---|
| **Must fix** | Security issues, bugs, data loss risks, broken tests | Request changes |
| **Should fix** | Performance issues, missing error handling, N+1 queries | Request changes |
| **Suggestion** | Better patterns, cleaner code, opportunities | Comment only |
| **Nitpick** | Style, naming, minor preferences | Comment with "nit:" prefix |

### Review tone

- Be specific: "This fetch could be parallelized with the one on line 38 using Promise.all()" not "improve performance"
- Suggest code: show the fix, don't just describe it
- Acknowledge good work: "Nice use of Server Components here"
- Ask questions when intent is unclear: "Is this intentionally sequential?"
