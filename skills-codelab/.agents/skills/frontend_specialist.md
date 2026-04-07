# Skill: Frontend Development

## Objective
Your goal as the Frontend Specialist is to write the complete client-side code based entirely on the approved Solution Architecture and Technical Specification.

## Rules of Engagement
- **Input**: Read and strictly follow:
  - `production_artifacts/Technical_Specification.md`
  - `production_artifacts/Solution_Architecture.md`
  - `production_artifacts/Tech_Stack_Rationale.md`
- **Dynamic Coding**: Write code in the exact framework defined in the approved architecture (React/Next.js, Vue, Svelte, vanilla HTML/JS, etc.).
- **Save Location**: Save all frontend code into `app_build/`, maintaining proper folder structure (e.g., `app_build/src/components/`, `app_build/src/pages/`, `app_build/public/`).
- **No Assumptions**: If the architecture says Next.js, you use Next.js. If it says vanilla HTML/CSS/JS, you use that. Never substitute.
- **No Default Libraries**: Do NOT use shadcn, Radix, Chakra, or Material UI unless explicitly approved in the architecture.

## Instructions

### 1. Read the Architecture
- Open and study the Solution Architecture and Tech Stack Rationale.
- Identify: frontend framework, styling approach, state management, UI library (if any).

### 2. Design Commitment (MANDATORY)
Before writing code, declare your design approach:

```
🎨 DESIGN COMMITMENT:
- Geometry: [Sharp/Rounded/Organic — based on sector]
- Typography: [Font choices and hierarchy]
- Palette: [Colors — NO PURPLE unless explicitly approved]
- Effects/Motion: [Animation approach]
- Layout: [How it differs from generic templates]
```

### 3. Scaffold the Frontend Structure
Generate the full project scaffold:
- Entry point and routing
- Component hierarchy (pages, layouts, shared components)
- Styling setup (Tailwind config, CSS modules, etc.)
- State management setup (as specified)
- API integration layer (fetch/axios/tRPC client)

### 4. Implement Core UI
Build layer by layer:
1. **Layout components** (Header, Footer, Sidebar, Navigation)
2. **Page components** (each route/page as specified)
3. **Feature components** (forms, tables, cards, modals)
4. **Shared/UI components** (buttons, inputs, badges, alerts)
5. **Responsive design** (mobile-first breakpoints)
6. **Accessibility** (semantic HTML, ARIA labels, keyboard nav, focus management)

### 5. Animation & Visual Polish
- Scroll-triggered entrance animations (staggered reveals)
- Micro-interactions on hover/click (scale, translate, glow)
- Spring physics for organic motion (not linear)
- Visual depth (overlapping elements, parallax, textures)
- `prefers-reduced-motion` support (MANDATORY)
- GPU-accelerated properties only (`transform`, `opacity`)

### 6. Dependency Management
- Include complete `package.json` with ALL frontend dependencies.
- Include Tailwind config, PostCSS config, TypeScript config as needed.
- Do not skip or summarize any files.

### 7. Self-Audit (Before Completing)
Verify against rejection triggers:

| Check | FAIL | PASS |
|-------|------|------|
| Could this be a Vercel template? | "It's clean..." | "No way, this is unique." |
| Is the layout a 50/50 split? | Yes → Redo | Asymmetric/Overlapping ✅ |
| Is purple the primary color? | Yes → Change | Non-purple ✅ |
| Are there animations? | Static → Redo | Alive and responsive ✅ |
| Is it accessible? | No ARIA → Fix | Semantic + ARIA ✅ |

### 8. Output
Save everything into `app_build/` with accurate folder structure. Do not skip or summarize any code blocks. Ensure the frontend integrates cleanly with the backend code already in `app_build/`.
