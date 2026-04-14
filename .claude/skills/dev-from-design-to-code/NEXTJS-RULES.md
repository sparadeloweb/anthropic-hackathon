# Next.js Best Practices

Derived from [next-best-practices](https://skills.sh/vercel-labs/next-skills/next-best-practices).

## App Router Conventions

### File Conventions
- `layout.tsx` — shared layout, wraps children, persists across navigation
- `page.tsx` — unique page content, makes route publicly accessible
- `loading.tsx` — Suspense fallback for the route segment
- `error.tsx` — error boundary (must be `'use client'`)
- `not-found.tsx` — 404 for the segment
- `template.tsx` — like layout but re-mounts on navigation

### Route Structure
```
app/
├── layout.tsx          (root layout — includes <html>, <body>)
├── page.tsx            (home page)
├── nosotros/
│   └── page.tsx
├── servicios/
│   └── page.tsx
├── opiniones/
│   └── page.tsx
├── contacto/
│   └── page.tsx
└── api/                (API routes if needed)
    └── contact/
        └── route.ts
```

## React Server Components (RSC)

### Default to Server Components
- Pages and layouts are Server Components by default
- They can `async/await` data directly
- Zero client JS unless `'use client'` is added

### When to use `'use client'`
- Event handlers (onClick, onChange, onSubmit)
- React hooks (useState, useEffect, useRef)
- Browser-only APIs (window, localStorage)
- Interactive UI (forms, modals, dropdowns)

### RSC Boundary Pattern
```tsx
// ServerWrapper.tsx (Server Component)
import { ClientInteractive } from './ClientInteractive';

export async function ServerWrapper() {
  const data = await fetchData(); // Server-side fetch
  return <ClientInteractive initialData={data} />;
}

// ClientInteractive.tsx
'use client';
export function ClientInteractive({ initialData }) {
  const [state, setState] = useState(initialData);
  // Interactive logic here
}
```

## Data Fetching

- Fetch in Server Components — not in client components
- Use `fetch()` with Next.js caching: `fetch(url, { next: { revalidate: 3600 } })`
- Parallel fetches with `Promise.all()` in layouts/pages
- For forms: Server Actions with `'use server'`

## Image Optimization

```tsx
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Description"
  width={1200}
  height={630}
  priority // for above-the-fold images
  className="object-cover"
/>
```

- Always use `next/image` — never raw `<img>`
- Set `priority` for LCP images
- Use `sizes` prop for responsive images
- Prefer WebP/AVIF formats

## Font Optimization

```tsx
import { Geist, Space_Grotesk } from 'next/font/google';

const geist = Geist({ subsets: ['latin'], variable: '--font-geist' });
const spaceGrotesk = Space_Grotesk({ subsets: ['latin'], variable: '--font-space' });

export default function RootLayout({ children }) {
  return (
    <html className={`${geist.variable} ${spaceGrotesk.variable}`}>
      <body>{children}</body>
    </html>
  );
}
```

## Metadata

```tsx
export const metadata: Metadata = {
  title: 'Business Name',
  description: 'Business description',
  openGraph: { title: '...', description: '...', images: ['/og.png'] },
};
```

## Performance Checklist

- [ ] Server Components by default
- [ ] `next/image` for all images with priority on LCP
- [ ] `next/font` for fonts (no FOUT)
- [ ] Parallel data fetching
- [ ] Dynamic imports for heavy client components
- [ ] Metadata on every page
- [ ] Error boundaries (`error.tsx`)
- [ ] Loading states (`loading.tsx`)
