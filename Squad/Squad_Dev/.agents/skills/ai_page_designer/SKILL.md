---
name: ai-page-designer
description: >
  Design and build high-quality standalone pages from design references or a
  defined visual direction.
  TRIGGERS: landing page, landing, hero, microsite, prototype, standalone page,
  mockup, concept, visual direction, design reference, style tile, moodboard,
  marketing page, pricing page, product page, coming soon, splash, showcase,
  portfolio, case study, brochure site, one-pager.
---

# AI Page Designer

## Objective

Create visually distinctive pages without copying templates blindly or defaulting
to generic "AI aesthetic". Every page should feel intentional, brand-aligned,
and memorable.

**Core principle**: Reference-driven, not template-driven. Taste is built by
paying attention to what references actually do, not by mimicking surface style.

---

## 1. Project Structure Contract

| Folder | Purpose |
|---|---|
| `app_build/` | Implementation-ready page (when the user wants code) |
| `production_artifacts/pages/` | Concept pages, approved mockups |
| `references/` | Design notes, captured references, style summaries |
| `assets/` | Images, fonts, icons, auxiliary files |
| `scripts/` | Repeatable export / validation helpers |

---

## 2. Required Inputs

Before drawing anything, confirm:

- **Design direction**: reference folder path, moodboard URL, or a clear style description
- **Primary brand color** (exact, or direction like "deep teal")
- **Page goal**: conversion? brand? pricing? portfolio?
- **Audience**: who lands here and what do they need in 5 seconds?
- **Stack**: pure HTML/CSS? React? Next? Astro? Framer?

If already given in conversation, reuse. Don't re-interview unnecessarily.

---

## 3. Design Principles (Non-Negotiable)

### Restraint is Power

- 2-3 type sizes max for the hero, not 7
- Consistent spacing scale (8-pt grid)
- Limited palette: 1 brand, 2-3 neutrals, 1 accent
- White space is part of the design, not leftover

### Tension Makes Memorable

- Pair serifs with sans (contrast)
- Pair huge with tiny (scale)
- Pair dense text blocks with open space (rhythm)
- Pair one bold color with quiet neutrals

### Copy is Design

- Real words, not lorem ipsum
- Sentence case headlines (unless brand calls for all-caps)
- Verbs over nouns, concrete over abstract
- Edit your copy -- every adjective is suspect

---

## 4. Anti-Patterns (Never Default To)

| Pattern | Why It's Bad | Do Instead |
|---|---|---|
| Purple/violet primary | Over-used | Ask the user, or pick anything but purple |
| Bento grid hero | Generic AI starter kit | Asymmetric / editorial layouts |
| Split 50/50 hero | Predictable | Typographic hero, full-bleed image, narrative vertical |
| Aurora / mesh gradient background | "I gave up on design" | Flat bold color or well-composed photo |
| Glassmorphism everywhere | Dated, muddy | Flat surfaces with sharp shadows |
| Floating isolated 3D blobs | AI cliche | Custom illustration or bold type as art |
| Centered stack of 3 feature cards | Template #1 of AI | Asymmetric composition, varied card sizes |
| "Empower / Orchestrate / Unleash" copy | Reads as AI | Write like a human talking to a friend |
| Round shiny buttons with gradient | Dated | Flat, strong contrast, proper hit target |
| Emoji instead of icons on serious brands | Cheap | Iconography that matches the brand |

---

## 5. Workflow

### Phase 1: Intake

1. Run the intake from [references/design-intake.md](references/design-intake.md).
2. Look at the reference folder or URLs -- note palette, type, spacing, rhythm.
3. Summarize in a short style tile (3-5 bullet points).

### Phase 2: Composition

4. Sketch the structure (wireframe) in pseudo-markup before visuals.
5. Decide hero strategy: typographic / image-first / split / video / narrative.
6. Map the visual hierarchy: primary CTA is obvious in 1 second?

### Phase 3: Detail

7. Pick a palette grounded in the brand color (derive with OKLCH shifts).
8. Pick 2 type families or a single strong one with careful weight/size.
9. Apply the 8-pt grid. Audit every spacing decision.
10. Write the copy -- don't fill with lorem ipsum.
11. Add thoughtful motion only where it clarifies or delights.

### Phase 4: Implementation

12. Build to `app_build/` (if stack requested) or `production_artifacts/pages/`.
13. Mobile-first -- test at 360px width first.
14. Optimize images (AVIF/WebP, correct sizes).
15. Verify contrast (WCAG AA), keyboard nav, focus rings.

### Phase 5: Self-Audit

16. Squint test: is the hierarchy still clear?
17. 5-second test: does a cold visitor understand purpose?
18. Mobile test: does it hold up on a real phone?
19. Competitor compare: does it look distinctive next to peers?

---

## 6. Technical Patterns

### Pure HTML/CSS (no framework)

- Single `index.html` with inline or linked CSS
- No build step required
- Modern CSS: `clamp()`, `@container`, `:has()`, `oklch()`
- Minimum dependencies -- this is a standalone page

### React / Next

- Use `next/image`, `next/font`, `<Link>` if Next
- Server Components for content, Client only for interactions
- Tailwind v4 with `@theme` tokens for design system
- See frontend_specialist for deeper patterns

### Assets

- Favicon + OG image at minimum
- OG image 1200x630 with readable text even at small preview
- `lang`, `meta description`, `theme-color` in `<head>`

---

## 7. Hero Strategies

Pick one deliberately:

| Strategy | When |
|---|---|
| **Typographic** | Strong brand voice, no imagery budget, confident statement |
| **Full-bleed image** | Visual product, photography central to the brand |
| **Split editorial** | Story-driven, long-form content to follow |
| **Video loop** | Process or kinetic product (limit to muted, lightweight) |
| **Asymmetric overlap** | Editorial, high-design feel |
| **Data / dashboard preview** | B2B tools where the product IS the hero |

---

## 8. Palette Derivation (OKLCH)

From a primary brand color in OKLCH `oklch(L C H)`:

- Tints: increase L, decrease C -- `oklch(0.92 0.04 h)`
- Shades: decrease L, keep C -- `oklch(0.35 0.15 h)`
- Accent: shift H by 120-180 deg
- Neutrals: same H, very low C, range of L

Result: a palette that looks related but has variety, without muddy mixing.

---

## 9. Typography Pairing Recipes

| Context | Display | Body |
|---|---|---|
| Editorial / elegant | Fraunces, Playfair, GT Super | Inter, Söhne, Satoshi |
| Bold / confident | Space Grotesk, Archivo, Geist | Inter, IBM Plex Sans |
| Minimal / neutral | Inter Display, Satoshi | Inter, system-ui |
| Playful / approachable | DM Serif Display, Nunito | DM Sans, Nunito Sans |
| Tech / product | Geist, JetBrains Mono (accent) | Geist Sans |

Rules:
- Don't use more than 2 families
- Limit to 3 weights per family
- Use `font-variation-settings` for variable fonts (`opsz`, `wdth`)

---

## 10. Quality Bar

- [ ] No purple-first default
- [ ] No direct template clone
- [ ] No unnecessary framework dependency for a static page
- [ ] Works and looks intentional on desktop AND mobile
- [ ] Real copy, not lorem ipsum
- [ ] Palette derived from a named brand color
- [ ] Type pairing justified
- [ ] 8-pt grid respected
- [ ] Contrast WCAG AA
- [ ] OG image + favicon + meta present
- [ ] Loads fast (< 100KB CSS, images optimized)

---

## 11. Bundled Reference

| File | Contents |
|---|---|
| [references/design-intake.md](references/design-intake.md) | Consistent intake questions for page design |

---

## 12. Deliverables

Every page produces:

1. Page source in `app_build/` or `production_artifacts/pages/`
2. Style notes in `references/` summarizing the decisions
3. Screenshots (desktop + mobile) when requested for review
4. OG/social preview image when it's a marketing page
