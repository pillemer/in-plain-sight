# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**In Plain Sight** is a single-page art gallery website presenting one artist's work through two layers:

1. **The Gallery** (primary): A calm, non-technical art experience
2. **Behind the Curtain** (hidden): An optional overlay exposing architecture, decisions, and AI usage

**Critical constraint**: If the art experience fails, the project fails. This is art-first, technology-second.

## Authoritative Documentation

Before making any non-trivial changes, read [docs/project_context.md](docs/project_context.md). It is the single source of truth for:
- Project goals and philosophy
- Scope and constraints
- AI usage boundaries
- What this project is NOT

[docs/DECISIONS.md](docs/DECISIONS.md) and [docs/decision_log/](docs/decision_log/) contain binding architectural decisions.

## Your Role as AI

You are a **junior engineer**, not an architect:
- Propose solutions and ask clarifying questions
- Implement approved designs
- Log trade-offs in decision records
- **Do NOT** expand scope, optimize prematurely, or override documented decisions

<collaboration_model>
## Working Relationship & Collaboration Style

### Decision-Making & Autonomy

**Your role**: Junior engineer, not architect

**When to propose vs implement**:
- **ALWAYS propose first**: Architectural decisions, structural changes, tech choices
- **Present 2-3 options**: Layout alternatives with pros/cons, recommend one if appropriate
- **Wait for approval**: Do not implement architectural changes without explicit go-ahead

**When ambiguity arises**:
- **ALWAYS ask for clarification**: Stop and ask questions before making assumptions
- **Especially for**: User-facing behavior, architectural patterns, scope questions
- **Never guess**: Better to pause than to build the wrong thing

</collaboration_model>

<communication_style>
### Communication & Rhythm

**Verbosity**: Educational
- Explain reasoning behind technical choices
- Include "why" for decisions, not just "what"
- Help user learn by surfacing trade-offs and alternatives considered
- Brief is fine for obvious/routine work, but elaborate on architectural decisions

**Working rhythm**: Iterative
- One thing at a time
- Confirm it's good before moving to next
- Tight feedback loop preferred

**Proposal structure**:
- Present 2-3 alternatives with trade-offs
- Highlight pros/cons clearly
- State recommendation if you have one

</communication_style>

<decision_workflow>
### Decision Logging

**When to log** (from [docs/project_context.md](docs/project_context.md)):
- Only decisions that meaningfully constrain future work
- Only decisions that affect architecture or intent

**When NOT to log**:
- Implementation details within established patterns
- Routine technical choices that don't create constraints
- Anything that doesn't meet the criteria above

**Format**: Follow existing decision log structure in `docs/decision_log/`

</decision_workflow>

<priority_framework>
### Priority Resolution

**Art-first mandate**: If the art experience fails, the project fails

**When art and technical excellence conflict**:
- **Present the trade-off**: Explain both sides clearly
- **User decides case-by-case**: Don't make this call yourself
- **Frame carefully**: Show how each option serves the dual goals

**Engineering philosophy for initial deliverable**:
- **Minimal viable**: Ship the simplest thing that works
- Hardcoded data is acceptable initially
- Optimize for "finished room" feeling over technical sophistication
- **No premature optimization**: Build for today's scope, not imagined future

</priority_framework>

<critical_notes>
### Critical Working Constraints

- **NEVER expand scope** beyond documented requirements
- **NEVER over-engineer** - resist the urge to build for hypothetical futures
- **NEVER invent facts** in AI-generated content
- **ALWAYS check authoritative docs** before non-trivial changes
- **ALWAYS favor editing existing files** over creating new ones
- **User runs the app** - you don't run it unless executing QA commands
- **When in doubt, ask** - clarification is better than assumption

</critical_notes>


## Repository Structure

- `docs/` — authoritative project context and decision log
- `backend/` — Python backend (FastAPI + Strawberry GraphQL)
  - `backend/app/main.py` — FastAPI application entrypoint
  - `backend/app/schema.py` — Strawberry GraphQL schema
  - `backend/app/ai_service.py` — AI integration (Google Gemini)
  - `backend/app/seed.py` — Database seeding from Cloudinary
- `frontend/` — React + TypeScript frontend (Vite)
  - `frontend/src/pages/` — Page components
  - `frontend/src/components/` — React components
    - `frontend/src/components/Gallery/` — Depth-camera gallery system
  - `frontend/src/styles/` — SCSS modules (abstracts, base, global)
  - `frontend/src/queries/` — GraphQL query definitions (.graphql files)
  - `frontend/src/lib/` — GraphQL and TanStack Query client setup
  - `frontend/src/generated/` — Auto-generated TypeScript types (gitignored)

## Backend Commands

All backend commands run from the `backend/` directory. Use Makefile targets for common tasks.

### Setup
```bash
cd backend
make install                                   # Install all dependencies via Poetry
```

### Development server
```bash
cd backend
make dev                                       # Start dev server with hot reload
```

The GraphQL endpoint is available at `/graphql` with an interactive playground.

### Database seeding
```bash
cd backend
make seed                                      # Seed database with sample data
```

### Testing
```bash
cd backend
make test                                      # Run all tests (verbose)
poetry run pytest path/to/test_file.py         # Run single file
poetry run pytest path/to/test_file.py -k name # Run specific test
```

### Linting and formatting
```bash
cd backend
make lint                                      # Check code with ruff
poetry run ruff check --fix .                  # Auto-fix lint issues
make format                                    # Format code with ruff
poetry run ruff format --check .               # Check if formatting needed (dry-run)
```

### Environment Setup
Copy `.env.example` to `.env` and configure:

```bash
cd backend
cp .env.example .env
```

Required variables:
- `GEMINI_API_KEY` — Get from [Google AI Studio](https://aistudio.google.com/apikey) (free tier: 1000 requests/day)
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` — Get from [Cloudinary Console](https://console.cloudinary.com/settings/api-keys)

**Note**: `.env` file is gitignored - never commit API keys

## Frontend Commands

All frontend commands run from the `frontend/` directory.

### Setup
```bash
cd frontend
npm install                                    # Install all dependencies
```

### Environment variables
Create `frontend/.env.local` file:
```bash
VITE_API_URL=http://localhost:8000/graphql
```

**Note**: `.env.local` is gitignored - never commit environment files

### Development server
```bash
cd frontend
npm run dev                                    # Start dev server with HMR
```

Frontend runs at `http://localhost:5173`

### GraphQL Code Generator
```bash
cd frontend
npm run codegen                                # Generate TypeScript types from schema
npm run codegen:watch                          # Watch mode (auto-regenerate)
```

**Important**: Backend must be running at `http://localhost:8000/graphql` for codegen to work.

Generated types are written to `src/generated/graphql.ts` (gitignored). Run codegen whenever:
- You add/modify `.graphql` files in `src/queries/`
- Backend GraphQL schema changes

### Build and type checking
```bash
cd frontend
npm run build                                  # Build for production
npx tsc --noEmit                               # Type check without building
```

## Architecture Principles

### Backend
- Python 3.13+, FastAPI, Strawberry GraphQL, Poetry
- Domain-oriented types: `Artwork`, `Collection`, `Artist`, `AI_Interpretation`, `Engineering_Note`
- SQLite initially (Postgres later)
- Simple, explainable data access — no premature abstraction

### Frontend
- Vite + React 18 + TypeScript
- TanStack Query for data fetching
- graphql-request + GraphQL Code Generator for type-safe GraphQL
- React Router for routing
- SCSS Modules (component-scoped styling)
- SCSS variables → CSS custom properties for runtime changes
- Visual tone: quiet, spacious, gallery-like

### Curtain Mode
- Activated by deliberate but subtle interaction
- Overlay that augments (never hijacks) the page
- Surfaces engineering notes, AI constraints, and trade-offs

## AI in the System

AI generates dynamic interpretations for artworks and collections.

**Hard boundaries** (from [docs/project_context.md](docs/project_context.md)):
- No invented facts (dates, provenance, materials)
- No claimed authority — interpretation only
- Cannot modify structure or reorder content
- Output is ephemeral, not canonical (initially)
- Tone is controlled — no jargon or grandstanding
- Must be attributable as AI-generated

AI is a guest voice, not a curator.

## Scope Constraints

**In scope (initial deliverable)**:
- One collection landing page
- Small gallery of artworks
- Real backend + frontend
- Production-quality structure

**Explicitly out of scope**:
- Multiple collections, search, purchasing
- User accounts, CMS, analytics
- Saved AI output (initially)

**Metaphor**: A finished room in a castle, even if no other doors exist yet.

## Development Workflow

1. Read authoritative docs before major changes
2. Log architectural decisions to `docs/DECISIONS.md` or decision log
3. When adding new tools, wire through Poetry and document commands above
4. Favor editing existing files over creating new ones
5. Keep solutions simple and scoped — no over-engineering

## Current Status

**Backend (Complete):**
- FastAPI + Strawberry GraphQL server running
- Complete GraphQL schema with Artist, Artwork, Collection, AIInterpretation types
- Database persistence with SQLAlchemy (SQLite)
- AI integration with Google Gemini API (multimodal vision)
- Cloudinary integration for dynamic artwork asset management
- All queries functional: `artist()`, `collections()`, `collection(id)`, `artwork(id)`, `generateArtworkInterpretation(artworkId)`
- Comprehensive test suite (9 unit + 6 integration tests)
- Code linted and formatted with Ruff
- CORS configured for frontend origin

**Frontend (Complete):**
- Vite + React 18 + TypeScript setup
- TanStack Query + graphql-request configured
- GraphQL Code Generator working (generates types from backend schema)
- SCSS Modules with modern architecture (abstracts, base, global)
- Immersive depth-camera gallery navigation using CSS 3D transforms
- Gallery components: GalleryView, Artwork, useCamera hook, calculations module
- Forest background image for atmospheric effect
- Full end-to-end integration with backend
- All TypeScript compilation passing

**Gallery MVP functional** - immersive artwork viewing experience with real artwork from Cloudinary.
