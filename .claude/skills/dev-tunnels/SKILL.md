---
name: dev-tunnels
description: Manages public tunnels for local development servers. Lists active tunnels, creates new ones, and closes existing ones. Use when the user wants to share a local server, create a tunnel, check active tunnels, or stop a tunnel.
model: sonnet
allowed-tools: Bash(*)
---

# Manage Development Tunnels

Creates, lists, and closes public tunnels for local development servers. Supports Cloudflare Tunnels (no account needed) and Vercel Dev.

## Commands

This skill responds to these intents:

- **"List tunnels"** / **"What tunnels are active?"** → List
- **"Create a tunnel"** / **"Share my localhost"** → Create
- **"Close tunnel"** / **"Stop tunnel"** → Close
- **"Close all tunnels"** → Close all

## List Active Tunnels

```bash
# Find all tunnel processes
echo "=== Cloudflare Tunnels ==="
ps aux | grep '[c]loudflared' | awk '{print "PID:", $2, "| Started:", $9, "| CMD:", $11, $12, $13, $14}'

echo ""
echo "=== Vercel Dev ==="
ps aux | grep '[v]ercel dev' | awk '{print "PID:", $2, "| Started:", $9, "| CMD:", $11, $12, $13}'

echo ""
echo "=== Other Tunnels (ngrok, localtunnel) ==="
ps aux | grep -E '[n]grok|[l]t ' | awk '{print "PID:", $2, "| Started:", $9, "| CMD:", $11, $12, $13}'
```

If no tunnels found, inform the user. If tunnels found, display PID, port, and provider.

## Create a Tunnel

Ask the user:

**1. Which port?** Default: 3000 (Next.js). Common: 3000, 5173 (Vite), 8000 (Laravel), 8080.

**2. Which provider?**

| Provider | Command | Requires |
|---|---|---|
| Cloudflare (Recommended) | `npx cloudflared tunnel --url http://localhost:PORT` | Nothing (no account) |
| Vercel | `vercel dev --listen PORT` | Vercel CLI + auth |
| ngrok | `ngrok http PORT` | ngrok account + auth token |
| localtunnel | `npx localtunnel --port PORT` | Nothing |

**3. Run in background:**
```bash
# Cloudflare (recommended — free, no signup)
npx cloudflared tunnel --url http://localhost:PORT &> /tmp/tunnel-PORT.log &
echo "Tunnel PID: $!"

# Wait for URL to appear in logs
sleep 3
grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' /tmp/tunnel-PORT.log
```

Present the public URL to the user. Warn that the tunnel stays active until closed or the terminal session ends.

## Close a Tunnel

**Close specific tunnel by PID:**
```bash
kill PID
echo "Tunnel PID closed"
```

**Close specific tunnel by port:**
```bash
# Find tunnel process for a specific port
PID=$(ps aux | grep -E 'cloudflared|ngrok|localtunnel|vercel dev' | grep PORT | awk '{print $2}')
if [ -n "$PID" ]; then
  kill $PID
  echo "Tunnel on port PORT closed (PID: $PID)"
else
  echo "No tunnel found on port PORT"
fi
```

**Close ALL tunnels:**
```bash
pkill -f cloudflared 2>/dev/null && echo "Cloudflare tunnels closed"
pkill -f 'vercel dev' 2>/dev/null && echo "Vercel tunnels closed"
pkill -f ngrok 2>/dev/null && echo "ngrok tunnels closed"
pkill -f localtunnel 2>/dev/null && echo "localtunnel tunnels closed"
echo "All tunnels closed"
```

## Cleanup

Clean up log files when closing tunnels:
```bash
rm -f /tmp/tunnel-*.log
```

## Setup

### Cloudflare (recommended — no signup needed)

Works immediately via npx:
```bash
npx cloudflared tunnel --url http://localhost:3000
```

### ngrok (optional)

```bash
# Install
npm i -g ngrok
# Or: brew install ngrok

# Auth (one time)
ngrok config add-authtoken YOUR_TOKEN
# Get token at: https://dashboard.ngrok.com/get-started/your-authtoken
```
