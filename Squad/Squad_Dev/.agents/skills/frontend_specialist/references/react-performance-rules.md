# React / Next.js Performance Rules

Pragmatic rules for modern React (18+/19) and Next.js (14+/15). Use this as
a checklist during implementation and review.

---

## 1. Rendering Strategy

### Pick the Right Rendering Mode

| Mode | Use For |
|---|---|
| Static (SSG) | Content that changes rarely (marketing, docs, blog) |
| ISR (revalidate) | Content that changes predictably (catalog pages) |
| On-demand revalidation | Content invalidated by events (CMS updates via webhook) |
| SSR (dynamic) | Per-request data (personalized dashboards) |
| Streaming SSR | Large pages with independent sections |
| CSR (client-only) | Highly interactive apps behind auth |

**Default for Next App Router**: Server Components + selective Client Components.

### Server Components First

- Server Components by default -- smaller client bundle, fetch closer to data.
- `"use client"` only on the leaf that needs state, effect, or browser API.
- Never mark a whole tree as client just to use one interactive leaf.

### Avoid the Waterfall

Parallel data fetching beats serial:

```typescript
// Bad: serial
const user = await fetchUser(id);
const orders = await fetchOrders(user.id);

// Good: parallel when independent
const [user, orders] = await Promise.all([
  fetchUser(id),
  fetchOrdersForUser(id),
]);
```

Use `Suspense` boundaries to stream sections independently.

---

## 2. Bundle Size

- Route-level code splitting is automatic in Next. Don't fight it.
- `dynamic()` with `ssr: false` for client-only heavy libs (charts, editors).
- Tree-shake: import named exports, not whole libraries.
- Avoid `moment.js` (use `date-fns` or native `Intl.DateTimeFormat`).
- Avoid `lodash` whole import -- `import debounce from 'lodash/debounce'` or use native.
- Check bundle with `@next/bundle-analyzer` periodically.

---

## 3. Images

- `next/image` always (optimization, lazy, AVIF/WebP).
- `priority` on the single LCP image (above-the-fold hero).
- `sizes` prop on responsive images to avoid over-delivery.
- Explicit `width`/`height` to prevent CLS.
- For SVGs, inline small icons; externalize large illustrations.

---

## 4. Fonts

- `next/font/google` or `next/font/local` -- zero CLS, subsetting, preload.
- Limit to 2 families, 3 weights each max.
- Use `font-display: swap` for critical, `optional` for decorative.
- Self-host when possible (GDPR + speed).

---

## 5. Data Fetching

### Server

- Native `fetch` in Server Components, with cache tags:
  ```typescript
  const res = await fetch(url, { next: { tags: ['orders'] } });
  ```
- Revalidate with `revalidateTag('orders')` in a Server Action.

### Client

- TanStack Query or SWR. Never roll your own caching.
- Stale-while-revalidate pattern by default.
- Prefetch on hover for predictable next navigations.

### Forms

- Server Actions for mutations in Next. No more API route for every form.
- `useOptimistic` for instant UI feedback.
- `useFormStatus` for pending state without prop drilling.

---

## 6. State Management

### Hierarchy of preference

1. **URL state** (searchParams, nuqs) -- sharable, SSR-friendly
2. **Server state** (TanStack Query / SWR) -- stale-while-revalidate
3. **Component state** (useState, useReducer)
4. **Lifted state** in a common parent
5. **Zustand / Jotai** for genuinely global UI state
6. **Context** for static values (theme, auth, i18n) -- NOT for frequently changing data

Context re-renders every consumer. Don't put counters or inputs in Context.

---

## 7. Re-render Discipline

### Measure Before Memoizing

`React.memo`, `useMemo`, `useCallback` have cost. Use the Profiler first.

Cases where memo pays off:
- Expensive computation (> 1ms)
- Child tree that re-renders unnecessarily and is expensive
- Referential equality needed for a dependency array or a memoized child

Cases where memo doesn't help:
- Cheap components (text, simple divs)
- Props that change every render anyway
- Wrapping everything "just in case"

### Common Re-render Traps

| Trap | Fix |
|---|---|
| Inline object/array in JSX | Lift to `useMemo` or constant |
| Inline arrow in JSX | Same, if passed to memoized child |
| Context with frequently changing value | Split into multiple Contexts |
| State lifted too high | Colocate state to the consumer |
| Parent state change cascades | `React.memo` on heavy children |

### Derive, Don't Sync

Anti-pattern:
```typescript
const [fullName, setFullName] = useState('');
useEffect(() => {
  setFullName(`${first} ${last}`);
}, [first, last]);
```

Fix:
```typescript
const fullName = `${first} ${last}`;
```

`useEffect` is for synchronizing with external systems, not for derivation.

---

## 8. Long Lists

- Virtualize any list > 100 items: `@tanstack/react-virtual`, `react-virtuoso`.
- `key` is stable and unique per item (not index when the list mutates).
- Use `content-visibility: auto` on sections for browser-level skipping.

---

## 9. Animations

- Animate only `transform` and `opacity` (composited).
- Use CSS transitions for simple state changes.
- Framer Motion for orchestrated sequences; keep durations < 400ms.
- `prefers-reduced-motion` respected everywhere.
- Avoid layout animations on long lists.

---

## 10. Core Web Vitals Troubleshooting

### LCP (Largest Contentful Paint) > 2.5s

- Is hero image optimized + `priority`?
- Is font blocking render? Use `next/font`.
- Is there a big client component hydrating before LCP?
- Preconnect to critical origins (`<link rel="preconnect">`).

### INP (Interaction to Next Paint) > 200ms

- Break long tasks (> 50ms) with `startTransition` or `useDeferredValue`.
- Debounce expensive computations on input.
- Defer non-critical work to idle time.
- Move heavy work off the main thread (Web Worker).

### CLS (Cumulative Layout Shift) > 0.1

- Reserve space for images/iframes (width/height).
- Avoid inserting content above existing content after load.
- Use `font-display: optional` or self-host to avoid FOIT/FOUT swap jumps.

---

## 11. Next.js Specific

- `generateStaticParams` for dynamic routes that can be pre-rendered.
- `export const dynamic = 'force-static'` to pin static.
- `<Link prefetch={true}>` (default) -- opt out only for huge routes.
- Middleware for auth, redirects, A/B -- keep it thin, runs on every request.
- Edge runtime for read-heavy, low-latency endpoints; Node runtime for heavy libs.

---

## 12. Observability

Ship performance monitoring from day one:

- Vercel Analytics / Sentry / Datadog RUM
- Web Vitals reporting via `useReportWebVitals`
- Error boundaries on route level + feature level
- Sourcemaps uploaded for readable stack traces

---

## 13. Quick Wins Checklist

- [ ] LCP image has `priority`
- [ ] Fonts loaded via `next/font`
- [ ] No client component wraps the whole page
- [ ] Data fetching in parallel where possible
- [ ] No `useEffect` for pure derivation
- [ ] Long lists virtualized
- [ ] Images have width/height to prevent CLS
- [ ] Bundle analyzed in CI at least weekly
- [ ] Web Vitals reported to an analytics sink
- [ ] `prefers-reduced-motion` respected
