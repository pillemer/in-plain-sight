# Decision 0011: Frontend technology stack

## Context
Phase 4 requires implementing the frontend for the art gallery. Requirements:
- Single-page application (one collection page with artwork gallery)
- Art-first visual design (calm, spacious, gallery-like)
- GraphQL integration with existing FastAPI/Strawberry backend
- SCSS/SASS styling (no Tailwind, per project constraints)
- TypeScript for type safety
- Must complement backend stack aesthetically and technically
- Should demonstrate modern 2026 best practices for portfolio/CV value
- Minimal viable approach - avoid over-engineering

## Decision
Use **Vite + React 18 + TypeScript** with **TanStack Query + graphql-request** for data fetching and **SCSS Modules** for styling.

### Complete Stack
- **Build tool:** Vite 6.x
- **Framework:** React 18
- **Language:** TypeScript 5.x
- **Data fetching:** TanStack Query v5 + graphql-request
- **Type generation:** GraphQL Code Generator
- **Styling:** SCSS Modules (modern Sass with @use/@forward)
- **Routing:** React Router v7 (single route, but establishes pattern)
- **State:** TanStack Query for server state, React hooks for UI state

## Alternatives considered

### Framework alternatives

#### 1. Next.js 15
**Pros:**
- Industry standard, high name recognition
- Built-in SSR/SSG capabilities
- App Router with React Server Components
- Excellent Vercel deployment integration

**Cons:**
- Over-engineered for single-page app
- SSR complexity not needed for this use case
- Heavier bundle and deployment footprint
- Contradicts "minimal viable solutions" philosophy

**Verdict:** Rejected - too much framework for a SPA

#### 2. Remix
**Pros:**
- Server-first architecture, web standards focused
- Excellent for form-heavy applications
- Growing ecosystem, Shopify-backed

**Cons:**
- Also over-engineered for SPA
- Less widespread adoption than Next.js or Vite
- Server-side complexity not needed

**Verdict:** Rejected - interesting but overkill

### GraphQL Client alternatives

#### 1. Apollo Client
**Pros:**
- Industry standard, comprehensive feature set
- Built-in normalized cache
- Excellent DevTools
- High name recognition

**Cons:**
- Heavy bundle size (~30KB vs ~15KB for TanStack Query + graphql-request)
- Normalized cache complexity overkill for simple data needs
- Over-featured for this project's requirements
- Some community concerns about cache complexity

**Verdict:** Rejected - too heavy for simple use case

#### 2. urql
**Pros:**
- Lightweight (~12KB)
- Purpose-built for GraphQL
- Good documentation and defaults

**Cons:**
- Less flexible than TanStack Query for non-GraphQL needs
- Smaller ecosystem and community
- Lower name recognition on CVs
- TanStack Query is more widely used in 2026

**Verdict:** Rejected - TanStack Query is the modern standard

### Styling alternatives

#### 1. CSS-in-JS (styled-components / Emotion)
**Pros:**
- Component-scoped automatically
- Dynamic styling with JavaScript
- Popular in industry

**Cons:**
- Runtime performance cost (styles generated in browser)
- Larger bundle size
- Dynamic class names complicate debugging
- Performance-conscious developers moving away in 2026
- Not ideal for static gallery layouts

**Verdict:** Rejected - runtime overhead not justified

#### 2. Plain CSS / Utility-first (Tailwind)
**Pros:**
- Zero runtime cost
- Fast development (Tailwind)

**Cons:**
- Tailwind explicitly rejected per project constraints
- Plain CSS lacks scoping and variables

**Verdict:** N/A - Tailwind ruled out, plain CSS insufficient

## Consequences

### Positive
- **Minimal and focused** - Each tool serves a clear purpose, no bloat
- **Modern best practices** - TanStack Query is the 2026 industry standard for server state
- **Performant** - Lightweight bundle (~15KB for data layer vs ~30KB for Apollo)
- **Fast development** - Vite's instant HMR, sub-second cold starts
- **Type-safe end-to-end** - GraphQL Codegen generates types from backend schema
- **CV value** - TanStack Query + TypeScript + modern patterns demonstrate current skills
- **Flexibility** - Not locked into framework opinions, easy to modify
- **Perfect fit** - SPA architecture matches single-page gallery requirement

### Negative
- **Manual wiring** - TanStack Query + graphql-request requires setup (vs Apollo out-of-box)
- **Less name recognition** - TanStack Query less known than Apollo to non-technical recruiters
- **No SSR/SSG** - Can't pre-render content (but not needed for this project)

### Mitigations
- TanStack Query setup is straightforward (~20 lines of config)
- GraphQL Codegen automates type generation, reducing manual work
- Documentation will explain technical choices for non-technical readers
- Could add SSG later via Vite plugins if needed (unlikely)

## Technical implementation details

### GraphQL Code Generator setup
- Plugins: `@graphql-codegen/typescript`, `@graphql-codegen/typed-document-node`
- Auto-generates TypeScript types from backend Strawberry schema
- Single source of truth - schema changes propagate to frontend types
- Eliminates manual type maintenance
- Catches breaking changes at build time, not runtime

### SCSS Modules approach
- Modern Sass Modules with `@use` and `@forward` (2026 best practice)
- Scoped by default (no class name collisions)
- Build-time processing (zero runtime cost)
- Debuggable class names in development
- Performance: 50-70% smaller bundles vs legacy SCSS patterns
- Aligns with "gallery-like" design requiring custom layouts

### TanStack Query pattern
- Handles all server state (artwork data, collections, AI interpretations)
- Automatic caching, background updates, request deduplication
- Simple React hooks interface: `useQuery`, `useMutation`
- Replaces need for Redux/Zustand for server data
- Client state (curtain mode toggle, UI preferences) via React hooks or Context

## Rationale summary

This stack was chosen to:
1. **Match project philosophy** - Minimal viable, no premature optimization
2. **Complement backend** - FastAPI/GraphQL backend + modern React = full-stack competence
3. **Demonstrate expertise** - Modern patterns (TanStack Query, TypeScript, GraphQL Codegen)
4. **Optimize performance** - Lightweight, fast, appropriate for gallery with heavy images
5. **Enable rapid iteration** - Vite's dev experience allows quick visual experimentation

## Related decisions
- **0012: Deployment architecture** - Separate frontend/backend deployments
- **Future decision needed:** Whether to add Zustand if UI state becomes complex

## References
- [TanStack Query documentation](https://tanstack.com/query/latest)
- [Vite vs Next.js vs Remix comparison 2025](https://jsgurujobs.com/blog/vite-vs-next-js-vs-remix-framework-comparison-for-2025)
- [React Stack Patterns 2026](https://www.patterns.dev/react/react-2026/)
- [Sass Modules architecture 2026](https://www.johal.in/sass-modules-in-django-architecture-for-scalable-css-organization-2026/)
- [GraphQL Codegen best practices](https://the-guild.dev/blog/graphql-codegen-best-practices)
