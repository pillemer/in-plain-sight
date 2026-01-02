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

**Verbosity**: Balanced
- Brief status updates for routine work
- Explain "why" for non-obvious decisions
- Skip obvious explanations of "what"

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
- Frontend planned (React + SASS, framework choice deferred)

## Backend Commands

All backend commands run from the `backend/` directory using Poetry.

### Setup
```bash
cd backend
poetry install
```

### Development server
```bash
cd backend
poetry run uvicorn app.main:app --reload
```

The GraphQL endpoint is available at `/graphql` with an interactive playground.

### Testing
```bash
cd backend
poetry install                                 # Install all dependencies (including dev)
poetry run pytest                              # Run all tests
poetry run pytest path/to/test_file.py         # Run single file
poetry run pytest path/to/test_file.py -k name # Run specific test
poetry run pytest -v                           # Verbose output
```

### Linting and formatting
```bash
cd backend
# Linting (find errors, bugs, code quality issues)
poetry run ruff check .                        # Report lint issues
poetry run ruff check --fix .                  # Auto-fix lint issues

# Formatting (code style consistency)
poetry run ruff format .                       # Format code
poetry run ruff format --check .               # Check if formatting needed (dry-run)
```

## Architecture Principles

### Backend
- Python 3.13+, FastAPI, Strawberry GraphQL, Poetry
- Domain-oriented types: `Artwork`, `Collection`, `Artist`, `AI_Interpretation`, `Engineering_Note`
- SQLite initially (Postgres later)
- Simple, explainable data access — no premature abstraction

### Frontend (planned)
- React single-page app
- SCSS/SASS styling (no Tailwind)
- Visual tone: quiet, spacious, gallery-like
- Must feel like a "finished room"

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

- Backend running with FastAPI + Strawberry GraphQL
- Complete GraphQL schema with Artist, Artwork, Collection, AIInterpretation types
- All queries functional: `artist()`, `collections()`, `collection(id)`, `artwork(id)`
- Comprehensive test suite (8 tests passing)
- Code linted and formatted with Ruff
- Data still hardcoded (persistence in next step)
- On Phase 2 of [docs/project_process.md](docs/project_process.md): "Domain & API Shape"
