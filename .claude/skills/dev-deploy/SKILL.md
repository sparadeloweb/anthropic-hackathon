---
name: dev-deploy
description: Deploys project code to Vercel (frontend) or Laravel Cloud (backend) using MCPs. Generates deployment documentation if missing. Use when the user wants to deploy, publish, or ship code to production.
model: opus
allowed-tools: Bash(*) Read Write Edit Glob Grep mcp__claude_ai_Notion__*
---

# Deploy to Production

Deploys frontend to Vercel and/or backend to Laravel Cloud. Generates deployment documentation if it doesn't exist.

## Prerequisites

- Project code exists locally (built by `/dev-from-design-to-code` or manually)
- Vercel MCP configured: `claude mcp add --transport http vercel https://mcp.vercel.com`
- For Laravel: Laravel Cloud account or server access
- Notion MCP configured (for documentation)

## Workflow

```
Deploy Progress:
- [ ] Step 1: Detect project type and deployment targets
- [ ] Step 2: Pre-deploy checks
- [ ] Step 3: Deploy frontend (Vercel)
- [ ] Step 4: Deploy backend (Laravel Cloud) if applicable
- [ ] Step 5: Verify deployment
- [ ] Step 6: Generate/update deploy documentation
```

### Step 1: Detect project type

Scan the project to determine what needs deploying:

- `package.json` with `next` → Next.js frontend → deploy to Vercel
- `composer.json` with `laravel/framework` → Laravel backend → deploy to Laravel Cloud
- Both → deploy both

Ask the user to confirm deployment targets.

### Step 2: Pre-deploy checks

**Frontend:**
```bash
pnpm build        # Must succeed with no errors
pnpm lint         # Must pass
npx playwright test  # E2E tests must pass
```

**Backend:**
```bash
php artisan test   # All tests must pass
php artisan config:cache
php artisan route:cache
```

If any check fails, stop and fix before deploying. Never deploy broken code.

### Step 3: Deploy frontend to Vercel

**If Vercel MCP is available**, use it to:
1. Create or link project
2. Set environment variables
3. Trigger deployment

**If Vercel MCP is not available**, use Vercel CLI:
```bash
# Install if needed
npm i -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

Set required environment variables:
```bash
vercel env add NEXT_PUBLIC_API_URL production
```

### Step 4: Deploy backend to Laravel Cloud (if applicable)

**Option A: Laravel Cloud**
```bash
# Install Cloud CLI
composer global require laravel/cloud-cli

# Deploy
cloud deploy production
```

**Option B: Manual server deploy**
```bash
ssh user@server 'cd /var/www/app && git pull origin main && composer install --no-dev && php artisan migrate --force && php artisan config:cache && php artisan route:cache && php artisan queue:restart'
```

### Step 5: Verify deployment

After deploy completes:
1. Check the production URL loads correctly
2. Test critical flows (contact form, navigation)
3. Verify API endpoints respond (if backend)
4. Check for console errors

### Step 6: Generate/update deploy documentation

If no deploy documentation exists, create it in Notion via MCP:

```
mcp__claude_ai_Notion__notion-create-pages({
  title: "Project Name — Deployment Guide",
  content: markdown with:
    - Production URLs (frontend + backend)
    - Environment variables required
    - How to deploy (step by step)
    - How to rollback
    - CI/CD setup (if any)
    - Domain configuration
    - SSL status
})
```

If documentation already exists, update it with the latest deployment info.

## Vercel MCP Setup

```bash
claude mcp add --transport http vercel https://mcp.vercel.com
```

Then authenticate: `/mcp` in Claude Code and follow the OAuth flow.

## Troubleshooting

| Issue | Solution |
|---|---|
| Build fails | Run `pnpm build` locally first, fix errors |
| Environment variables missing | Check Vercel dashboard or `vercel env ls` |
| API not connecting | Verify `NEXT_PUBLIC_API_URL` points to production backend |
| 404 on routes | Check `next.config.ts` for rewrites/redirects |
