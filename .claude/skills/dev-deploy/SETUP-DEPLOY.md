# Deployment Setup

## Vercel (Frontend)

### Option A: Vercel MCP (Recommended)

```bash
claude mcp add --transport http vercel https://mcp.vercel.com
```

Then authenticate in Claude Code:
```
/mcp
```

Follow the OAuth flow to connect your Vercel account.

### Option B: Vercel CLI

```bash
npm i -g vercel
vercel login
```

## Laravel Cloud (Backend)

```bash
composer global require laravel/cloud-cli
cloud login
```

## Notion MCP (Documentation)

Already configured if you have Notion MCP in your Claude Code setup. Verify:
```bash
claude mcp list
```

Look for `Notion` with status `Connected`.
