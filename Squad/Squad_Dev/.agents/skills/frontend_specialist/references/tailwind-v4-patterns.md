# Tailwind CSS v4 Patterns

Quick reference for Tailwind 4.x. The major shift: config is now CSS-first via
the `@theme` directive instead of a JS `tailwind.config.js`.

---

## 1. Installation & Entry

```css
/* app/globals.css */
@import "tailwindcss";

@theme {
  /* tokens go here */
}
```

No more `content` array, no more `@tailwind base/components/utilities`. The
single `@import` does it all.

---

## 2. Design Tokens with `@theme`

```css
@theme {
  /* Colors -- use OKLCH for perceptual uniformity */
  --color-brand-50:  oklch(0.98 0.02 255);
  --color-brand-500: oklch(0.62 0.18 255);
  --color-brand-900: oklch(0.22 0.08 255);

  /* Semantic colors */
  --color-surface: var(--color-neutral-50);
  --color-text:    var(--color-neutral-900);

  /* Typography */
  --font-sans:    "Inter", system-ui, sans-serif;
  --font-display: "Fraunces", serif;

  /* Spacing scale (extends default) */
  --spacing-18: 4.5rem;
  --spacing-22: 5.5rem;

  /* Radius */
  --radius-card: 0.75rem;

  /* Shadows */
  --shadow-card: 0 1px 3px oklch(0 0 0 / 0.08), 0 4px 12px oklch(0 0 0 / 0.06);
}
```

Tokens automatically become utilities: `bg-brand-500`, `text-display`,
`shadow-card`, `p-18`, `rounded-card`.

---

## 3. Dark Mode (CSS-first)

```css
@theme {
  --color-surface: oklch(1 0 0);
  --color-text:    oklch(0.2 0 0);
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-surface: oklch(0.15 0 0);
    --color-text:    oklch(0.95 0 0);
  }
}
```

Or class-based:

```css
.dark {
  --color-surface: oklch(0.15 0 0);
  --color-text:    oklch(0.95 0 0);
}
```

---

## 4. Container Queries (First-Class)

v4 ships native `@container` variants:

```html
<div class="@container">
  <div class="grid grid-cols-1 @md:grid-cols-2 @xl:grid-cols-3">
    ...
  </div>
</div>
```

Use container queries for **components**, media queries only for **page layout**.

---

## 5. Arbitrary Values

```html
<div class="grid grid-cols-[200px_1fr_auto]">
<div class="w-[calc(100%-4rem)]">
<div class="bg-[oklch(0.72_0.15_255)]">
```

Use sparingly. If you use the same arbitrary value twice, promote it to a token.

---

## 6. Layered Architecture

Tailwind v4 uses native CSS cascade layers:

```css
@layer base {
  body { font-family: var(--font-sans); }
  h1 { font-family: var(--font-display); }
}

@layer components {
  .btn-primary {
    @apply rounded-card px-4 py-2 bg-brand-500 text-white;
  }
}
```

Use `@layer components` sparingly -- prefer composing utilities in JSX.

---

## 7. Variants Cheat Sheet

| Variant | Use |
|---|---|
| `hover:`, `focus:`, `active:` | Interaction states |
| `focus-visible:` | Keyboard-only focus |
| `disabled:`, `aria-disabled:` | Disabled state |
| `group-*:`, `peer-*:` | Parent/sibling state |
| `data-[state=open]:` | Radix/HeadlessUI state |
| `has-[:checked]:` | CSS `:has()` |
| `motion-safe:`, `motion-reduce:` | Respects `prefers-reduced-motion` |
| `supports-[grid-template-columns:subgrid]:` | Feature queries |

---

## 8. Responsive Patterns

### Fluid type

```html
<h1 class="text-[clamp(2rem,5vw,4rem)]">Fluid heading</h1>
```

### Container-driven layout

```html
<section class="@container">
  <article class="
    grid gap-4
    @md:grid-cols-2
    @xl:grid-cols-3
    @3xl:grid-cols-4
  ">
    ...
  </article>
</section>
```

---

## 9. Animations

v4 includes motion primitives. For custom:

```css
@theme {
  --animate-pulse-slow: pulse 4s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
```

Usage: `class="animate-pulse-slow"`.

Respect reduced motion:

```html
<div class="motion-safe:animate-pulse-slow">
```

---

## 10. Component Recipes

### Button with variants (via cva)

```typescript
import { cva } from 'class-variance-authority';

export const button = cva(
  'inline-flex items-center justify-center rounded-card font-medium transition',
  {
    variants: {
      variant: {
        primary: 'bg-brand-500 text-white hover:bg-brand-600',
        ghost:   'bg-transparent text-brand-500 hover:bg-brand-50',
        danger:  'bg-red-600 text-white hover:bg-red-700',
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4 text-base',
        lg: 'h-12 px-6 text-lg',
      },
    },
    defaultVariants: { variant: 'primary', size: 'md' },
  }
);
```

### Card

```html
<article class="
  rounded-card bg-surface shadow-card
  p-6
  hover:shadow-lg transition
">
  <h2 class="font-display text-2xl mb-2">Title</h2>
  <p class="text-text/80 leading-relaxed">Body</p>
</article>
```

Note `text-text/80` -- token with opacity modifier.

---

## 11. Accessibility Helpers

- `sr-only` for screen-reader-only text
- `focus-visible:outline` ring patterns instead of removing default outline
- `aria-*` attributes drive visual state via `aria-[expanded=true]:`

---

## 12. Do / Don't

| Do | Don't |
|---|---|
| Compose utilities in JSX | Wrap every element in a custom `.btn-x` class |
| Use `@theme` tokens | Hard-code hex values |
| Container queries for components | Media queries for every breakpoint |
| OKLCH for gradients | HSL (bands) or RGB |
| Responsive via mobile-first | Desktop-first |
| `cva` for component variants | `clsx` spaghetti inside JSX |
| `@apply` in `@layer components` sparingly | `@apply` everywhere (defeats utility-first) |

---

## 13. Migration Note (v3 -> v4)

- `tailwind.config.js` becomes optional -- move tokens to `@theme`.
- `content` scan is automatic (no config needed for standard setups).
- `@tailwind base/components/utilities` -> single `@import "tailwindcss"`.
- `darkMode: 'class'` still works; default to `prefers-color-scheme` is fine.
- Test visual regressions in a storybook before shipping the v4 upgrade.
