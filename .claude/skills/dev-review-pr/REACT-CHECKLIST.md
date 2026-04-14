# React / Next.js PR Review Checklist

Check every item for React/Next.js files in the PR.

## Performance (Critical)

- [ ] No request waterfalls — independent fetches are parallelized
- [ ] No barrel imports — imports are direct from component files
- [ ] Heavy components use `next/dynamic` for code splitting
- [ ] Third-party scripts use `next/script` with appropriate strategy
- [ ] No unnecessary `'use client'` — Server Components where possible
- [ ] Images use `next/image` with `priority` on LCP images
- [ ] Fonts loaded via `next/font` (no external CSS imports)

## Architecture

- [ ] Server Components by default — `'use client'` only when needed
- [ ] One component per file
- [ ] Props are typed with TypeScript interfaces
- [ ] No business logic in components — extracted to utilities or server functions
- [ ] Consistent file naming (PascalCase for components, kebab-case for routes)

## Data Fetching

- [ ] Data fetched in Server Components, not client
- [ ] `fetch()` uses appropriate caching strategy
- [ ] Forms use Server Actions (`'use server'`)
- [ ] Loading states handled (`loading.tsx` or Suspense)
- [ ] Error states handled (`error.tsx` or error boundaries)

## Security

- [ ] No `dangerouslySetInnerHTML` without sanitization
- [ ] No user input rendered without escaping
- [ ] Environment variables use `NEXT_PUBLIC_` prefix only when needed client-side
- [ ] API keys are server-side only

## Bundle Size

- [ ] No large libraries imported that could be tree-shaken
- [ ] Conditional imports for feature-flagged code
- [ ] No duplicate dependencies

## Accessibility

- [ ] Interactive elements have accessible labels
- [ ] Color contrast meets WCAG 2.1 AA (4.5:1 for text)
- [ ] Focus management for modals/dialogs
- [ ] Alt text on images

## Testing

- [ ] New components have Playwright tests
- [ ] Tests cover user-visible behavior, not implementation
- [ ] No snapshot tests (they're brittle)
- [ ] Tests don't depend on timing or network
