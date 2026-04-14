---
name: dev-from-design-to-code
description: Converts Stitch designs into production code (Next.js frontend + optional Laravel API backend). Splits into minimum components, creates tests, installs dependencies, generates Notion documentation. Use when the user wants to build a website or app from an existing Stitch design.
model: opus
allowed-tools: Bash(*) Read Write Edit Glob Grep mcp__stitch__* mcp__claude_ai_Notion__*
---

# From Design to Code

Takes a Stitch design project and converts it into production-ready code: Next.js (React) frontend with optional Laravel API backend. Follows component-driven architecture, creates comprehensive tests, and documents everything in Notion.

## Prerequisites

- Stitch MCP configured (for reading designs)
- Node.js 18+ and npm/pnpm installed
- Notion MCP configured (for documentation)
- If backend needed: PHP 8.2+, Composer, Laravel installer

## Workflow

```
Build Progress:
- [ ] Step 1: Select Stitch project and review designs
- [ ] Step 2: Ask build preferences
- [ ] Step 3: Scaffold project and install dependencies
- [ ] Step 4: Build frontend components from design
- [ ] Step 5: Build backend API (if needed)
- [ ] Step 6: Write tests
- [ ] Step 7: Start dev server + optional tunnel
- [ ] Step 8: Generate documentation in Notion
```

### Step 1: Select Stitch project and review designs

List Stitch projects:
```
mcp__stitch__list_projects()
```

Or load from local `stitch_designs/*/stitch_project.json` if available.

For each screen, retrieve the HTML code via `get_screen` — this is the design reference for building components.

### Step 2: Ask build preferences

Ask ALL before proceeding:

**2a. Include backend?**
- Frontend only (static site / SSG)
- Frontend + Laravel API backend

**2b. Frontend framework:**
- Next.js (App Router) — recommended
- Next.js (Pages Router)

**2c. Styling:**
- Tailwind CSS (recommended)
- CSS Modules

**2d. Package manager:**
- pnpm (recommended)
- npm

**2e. Deployment target:**
- Vercel
- Self-hosted

**2f. What features need API?**
- Contact form submissions
- User authentication
- CMS / dynamic content
- Booking / appointments
- None (static only)

### Step 3: Scaffold project and install dependencies

**Frontend:**
```bash
npx create-next-app@latest PROJECT_NAME --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
cd PROJECT_NAME
pnpm add lucide-react clsx tailwind-merge
pnpm add -D @playwright/test
npx playwright install
```

**Backend (if needed):**
```bash
composer create-project laravel/laravel PROJECT_NAME-api
cd PROJECT_NAME-api
composer require laravel/sanctum laravel/mcp
php artisan install:api
php artisan vendor:publish --tag=ai-routes
```

### Step 4: Build frontend components from design

Follow rules in [REACT-RULES.md](REACT-RULES.md) and [NEXTJS-RULES.md](NEXTJS-RULES.md).

**Component splitting strategy:**
1. Read each Stitch screen HTML
2. Identify atomic UI elements → create in `src/components/ui/` (Button, Badge, Card, Input, etc.)
3. Identify composed blocks → create in `src/components/` (Hero, ServiceCard, ReviewCard, ContactForm, etc.)
4. Identify layout elements → create in `src/components/layout/` (Navbar, Footer, Section)
5. Build pages in `src/app/` using composed components

**Rules:**
- Every component in its own file
- Server Components by default — only add `'use client'` when needed (event handlers, hooks, browser APIs)
- Props typed with TypeScript interfaces
- No barrel exports — import directly from component file
- Colocate styles with components
- Extract design tokens from Stitch design system → `tailwind.config.ts`

**Page structure (multi-page site):**
```
src/
├── app/
│   ├── layout.tsx        (root layout with Navbar + Footer)
│   ├── page.tsx           (Home)
│   ├── nosotros/page.tsx
│   ├── servicios/page.tsx
│   ├── opiniones/page.tsx
│   └── contacto/page.tsx
├── components/
│   ├── layout/ (Navbar, Footer, Section)
│   ├── ui/ (Button, Badge, Card, Input, StarRating)
│   ├── Hero.tsx
│   ├── ServiceCard.tsx
│   ├── ReviewCard.tsx
│   └── ContactForm.tsx
└── lib/
    └── utils.ts (cn helper)
```

### Step 5: Build backend API (if needed)

Follow rules in [LARAVEL-RULES.md](LARAVEL-RULES.md).

**Structure:**
- Models with typed properties, relationships, scopes
- Form Requests for validation
- API Resources for JSON transformation
- Service classes for business logic — never in controllers
- Queued jobs for long-running tasks (email sending, etc.)
- Feature tests with Pest targeting >85% coverage

**API endpoints example (contact form):**
```
POST /api/contact — submit contact form
GET /api/services — list services
GET /api/reviews — list reviews
```

### Step 6: Write tests

**Frontend — Playwright E2E tests:**
```
tests/
├── home.spec.ts
├── navigation.spec.ts
├── contact-form.spec.ts
└── responsive.spec.ts
```

Test each page loads, navigation works, forms submit, responsive breakpoints render correctly.

**Frontend — Component tests (if applicable):**
Use React Testing Library for interactive components.

**Backend — Pest feature tests:**
```
tests/Feature/
├── ContactTest.php
├── ServicesTest.php
└── ReviewsTest.php
```

Test API responses, validation, error handling. Target >85% coverage.

Run all tests:
```bash
# Frontend
npx playwright test

# Backend
php artisan test --coverage
```

### Step 7: Start dev server and optional tunnel

Start the development server in background:
```bash
pnpm dev &
```

**Ask the user:** "The dev server is running at http://localhost:3000. Do you want to create a public tunnel to share it?"

If yes, create a tunnel using Cloudflare (no account needed):
```bash
npx cloudflared tunnel --url http://localhost:3000
```

Or using Vercel (if authenticated):
```bash
vercel dev --listen 3000
```

Inform the user of the public URL. They can manage active tunnels with `/dev-tunnels`.

### Step 8: Generate documentation in Notion

Use Notion MCP to create a project page:

```
mcp__claude_ai_Notion__notion-create-pages({
  title: "Project Name — Documentation",
  content: markdown with:
    - Project overview
    - Architecture diagram (text-based)
    - Component inventory
    - API endpoints (if backend)
    - Environment variables needed
    - How to run locally
    - How to deploy
    - Test coverage summary
    - Tunnel URL (if created)
})
```

Present the Notion page link to the user.
