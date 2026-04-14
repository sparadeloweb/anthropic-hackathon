---
name: dev-add-feature
description: Adds new features or fixes bugs in existing code. Creates branches, commits, and pull requests via gh CLI. Updates documentation. Use when the user wants to add a feature, fix a bug, modify code, or create a PR.
model: opus
allowed-tools: Bash(*) Read Write Edit Glob Grep mcp__claude_ai_Notion__*
---

# Add Feature / Fix Bug

Modifies existing project code, creates a proper git workflow (branch, commits, PR), and updates documentation.

## Prerequisites

- Project code exists locally with git initialized
- GitHub CLI (`gh`) installed and authenticated
- If not configured, this skill guides setup

## Workflow

```
Feature Progress:
- [ ] Step 0: Verify git + GitHub setup
- [ ] Step 1: Understand the change
- [ ] Step 2: Create branch
- [ ] Step 3: Implement changes
- [ ] Step 4: Run tests
- [ ] Step 5: Commit and create PR
- [ ] Step 6: Update documentation
```

### Step 0: Verify git + GitHub setup

Check if `gh` is installed and authenticated:
```bash
gh auth status
```

If not authenticated, instruct the user:
```
GitHub CLI is not configured. Run these commands:

1. Install gh:
   - macOS: brew install gh
   - Linux: sudo apt install gh
   - Windows: winget install GitHub.cli

2. Authenticate:
   ! gh auth login

3. Verify:
   gh auth status
```

Wait for the user to complete setup before continuing.

Also verify the remote is set:
```bash
git remote -v
```

### Step 1: Understand the change

Ask the user:

**1a. What type of change?**
- New feature
- Bug fix
- Refactor
- Performance improvement

**1b. Describe the change:**
- What should change?
- Which files/areas are affected?
- Any acceptance criteria?

**1c. Scope check:**
Read the relevant files to understand the current code before proposing changes.

### Step 2: Create branch

```bash
# Ensure we're on main and up to date
git checkout main
git pull origin main

# Create feature branch
git checkout -b TYPE/DESCRIPTION
```

Branch naming:
- `feat/add-booking-form`
- `fix/contact-form-validation`
- `refactor/extract-service-card`
- `perf/optimize-image-loading`

### Step 3: Implement changes

Follow the project's established patterns:

**Frontend (Next.js/React):**
- See `/dev-from-design-to-code` REACT-RULES.md and NEXTJS-RULES.md
- Server Components by default
- Direct imports, no barrel files
- Type all props and returns

**Backend (Laravel):**
- See `/dev-from-design-to-code` LARAVEL-RULES.md
- Business logic in services, not controllers
- Form Requests for validation
- API Resources for JSON responses
- Queue long-running tasks

**General rules:**
- Minimal changes — only modify what's necessary
- Don't refactor unrelated code
- Don't add features that weren't requested
- Match existing code style exactly

### Step 4: Run tests

```bash
# Frontend
pnpm build && pnpm lint && npx playwright test

# Backend (if exists)
php artisan test
```

If tests fail, fix before committing. If the change needs new tests, write them:
- New component → Playwright test for the page it appears on
- New API endpoint → Pest feature test
- Bug fix → regression test that would have caught the bug

### Step 5: Commit and create PR

```bash
# Stage specific files (never git add -A)
git add src/components/NewComponent.tsx src/app/page.tsx

# Commit with conventional message
git commit -m "feat: add booking form to contact page

Adds a date picker and time slot selector to the contact page.
Validates against business hours (Mon-Fri 9-18).

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"

# Push
git push -u origin feat/add-booking-form

# Create PR
gh pr create --title "feat: add booking form to contact page" --body "$(cat <<'EOF'
## Summary
- Adds booking form component with date picker and time slot selector
- Validates against business hours
- Includes Playwright test for form submission flow

## Test plan
- [ ] Form renders correctly on contact page
- [ ] Date picker shows available dates
- [ ] Time slots respect business hours
- [ ] Form submission works end-to-end
- [ ] Mobile responsive

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Present the PR URL to the user.

### Step 6: Update documentation

If the change affects documented behavior:

1. Check if Notion documentation exists for this project
2. Update relevant sections (new endpoints, new components, changed behavior)
3. If no documentation exists, suggest running `/dev-from-design-to-code` step 7

```
mcp__claude_ai_Notion__notion-update-page({
  pageId: "PAGE_ID",
  content: updated markdown
})
```
