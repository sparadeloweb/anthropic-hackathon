# React Best Practices

Derived from [vercel-react-best-practices](https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices).

## Critical: Eliminating Waterfalls (async-)

- Check conditions BEFORE awaits — avoid unnecessary network calls
- Defer awaits into conditional branches
- Parallelize independent operations with `Promise.all()`
- Use Suspense boundaries for streaming data

```tsx
// BAD: Sequential waterfalls
const user = await getUser();
const posts = await getPosts(user.id);
const comments = await getComments(posts[0].id);

// GOOD: Parallel where possible
const [user, posts] = await Promise.all([getUser(), getPosts(userId)]);
```

## Critical: Bundle Size (bundle-)

- Import directly from modules, not barrel files
- Dynamically load heavy components with `next/dynamic`
- Defer third-party scripts with `next/script`
- Conditionally load modules based on feature flags
- Tree-shake unused exports

```tsx
// BAD: Barrel import pulls everything
import { Button, Icon } from '@/components';

// GOOD: Direct import
import { Button } from '@/components/ui/Button';
```

## Server-Side Performance (server-)

- Use `React.cache()` for per-request deduplication
- Parallelize server-side fetches
- Avoid module-level mutable state
- Prefer Server Components by default

## Client-Side (client-)

- Implement SWR or React Query for data deduplication
- Deduplicate event listeners
- Use passive listeners for scroll events
- Minimize `'use client'` — only when needed

## Re-render Optimization (rerender-)

- Memoize expensive computations with `useMemo`
- Stabilize callbacks with `useCallback`
- Avoid inline object/array creation in JSX props
- Split context providers to prevent unnecessary re-renders

## Component Patterns

### File Structure
```
ComponentName/
├── ComponentName.tsx    (or just ComponentName.tsx at root)
├── ComponentName.test.tsx
└── index.ts            (only if needed for re-export)
```

### Props
```tsx
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
}
```

### cn() Helper
```tsx
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

## Rules Summary

1. Server Components by default — `'use client'` only when needed
2. Direct imports — no barrel exports
3. Parallel data fetching — never sequential when independent
4. Type everything — interfaces for props, typed returns
5. One component per file
6. Colocate tests with components
7. Extract design tokens to Tailwind config
8. Minimize client-side JS — prefer server rendering
