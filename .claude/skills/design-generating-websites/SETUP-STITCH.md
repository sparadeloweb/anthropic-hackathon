# Stitch MCP Setup

## 1. Get an API Key

1. Go to [Stitch Settings](https://stitch.withgoogle.com)
2. Scroll to **API Keys** section
3. Click **Create API Key**
4. Copy and save the key securely

## 2. Add to Claude Code

```bash
claude mcp add stitch --transport http https://stitch.googleapis.com/mcp --header "X-Goog-Api-Key: YOUR-API-KEY" -s user
```

`-s user` saves globally (all projects). Use `-s project` to save only for this project.

## 3. Add key to .env

Add to your `.env` file:

```
STITCH_API_KEY=your-api-key-here
```

And add to `.env.example`:

```
STITCH_API_KEY=your-api-key-here
```

## 4. Verify

Restart Claude Code and check:

```bash
claude mcp list
```

You should see `stitch` in the list with status `Connected`.

## Stitch MCP tools available

| Tool | What it does |
|---|---|
| `create_project` | Create a new design project |
| `get_project` | Get project details + screen instances |
| `list_projects` | List all projects |
| `list_screens` | List screens in a project |
| `get_screen` | Get screen HTML, screenshot, figma export |
| `generate_screen_from_text` | Generate a screen from a text prompt |
| `edit_screens` | Edit existing screens with a prompt |
| `generate_variants` | Generate design variants |
| `create_design_system` | Create design tokens (colors, fonts, shapes) |
| `update_design_system` | Update design system |
| `list_design_systems` | List design systems |
| `apply_design_system` | Apply design system to screens |
