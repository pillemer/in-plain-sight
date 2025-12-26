# Development Plan: In Plain Sight

## Current Status: Phase 1 Complete ✓

**What exists:**
- Backend runs (FastAPI + Uvicorn)
- GraphQL endpoint at `/graphql` with playground
- Basic schema with `Artwork`, `Collection`, `Query`
- Hardcoded data (2 artworks, 1 collection)
- No persistence, tests, or frontend yet

## High-Level Roadmap

Following [project_process.md](project_process.md) milestone structure:

### ✓ Phase 1: Backend Infrastructure & Skeleton [COMPLETE]
- Backend runs
- GraphQL endpoint exists
- Minimal domain logic

### → Phase 2: Domain & API Shape (Schema-first) [NEXT]
**Ends when:**
- GraphQL schema is stable and complete
- Queries return meaningful domain data
- Still no UI

**Major items:**
1. Add missing domain types (`Artist`, `AI_Interpretation`, `Engineering_Note`)
2. Extend `Artwork` with technical metadata
3. Implement data layer (SQLite initially)
4. Populate with real/realistic sample data
5. Add remaining GraphQL queries

### Phase 3: AI Integration as a System Actor
**Ends when:**
- AI-generated interpretations available via API
- Prompts respect hard boundaries
- No UI polish yet

**Major items:**
1. Choose and integrate AI API (Claude API likely)
2. Design prompts for artwork/collection descriptions
3. Add GraphQL field for dynamic AI interpretations
4. Implement attribution and constraints

### Phase 4: Frontend Foundation (Structure, not beauty)
**Ends when:**
- One page renders real data
- Looks unfinished but coherent

**Major items:**
1. Choose React framework (Next.js, Vite, etc.)
2. Set up SCSS/Sass
3. Wire up GraphQL client
4. Build collection page skeleton
5. Render artworks from API

### Phase 5: Curtain Mode (Differentiator)
**Ends when:**
- Curtain can be toggled
- Reveals something meaningful
- Doesn't break art experience

**Major items:**
1. Design trigger mechanism
2. Create overlay/augmentation system
3. Surface engineering notes and decisions
4. Add AI attribution layer

### Phase 6: Visual Refinement & Taste
**Ends when:**
- Page feels "finished"
- No new features added

**Major items:**
1. Typography system
2. Spacing and rhythm
3. Subtle motion/transitions
4. Final mood calibration

---

## Phase 2 Detailed Breakdown

### Step 2.1: Set Up Testing & Linting Infrastructure
**Why first**: Easier to add tooling before writing complex code

**Deliverable**: Can run `poetry run pytest` and `poetry run ruff check`

**Tasks:**
1. Add pytest and ruff to `pyproject.toml` dependencies
2. Configure ruff in `pyproject.toml` (or `ruff.toml`)
3. Add Poetry scripts for common commands
4. Create `backend/tests/` directory structure
5. Write one simple health check test to verify pytest works
6. Update CLAUDE.md with exact commands

**Files:**
- `backend/pyproject.toml`
- `backend/tests/test_health.py` (new)
- `CLAUDE.md` (update tooling section)

**Exit criteria:**
- Tests run and pass
- Linter runs without errors
- Commands documented

---

### Step 2.2: Complete GraphQL Schema Design
**Why before persistence**: Design the API surface first, then implement storage

**Deliverable**: Full GraphQL schema with all types, still using in-memory data

**Tasks:**
1. Add `Artist` type with appropriate fields
2. Extend `Artwork` with technical metadata (medium, dimensions, year, etc.)
3. Add `Engineering_Note` type for curtain layer
4. Add placeholder for `AI_Interpretation` (will fully implement in Phase 3)
5. Update `Collection` to include artist reference
6. Add query for single artwork by ID
7. Write tests for schema types and queries

**Files:**
- `backend/app/schema.py` (major expansion)
- `backend/tests/test_schema.py` (new)

**Exit criteria:**
- GraphQL playground shows complete schema
- All types queryable with hardcoded data
- Tests pass for all queries

---

### Step 2.3: Design Data Models & Repository Pattern
**Why separate**: Keep GraphQL schema (API) separate from data storage (implementation)

**Deliverable**: Data models and data access layer, not yet wired to GraphQL

**Tasks:**
1. Create `backend/app/models.py` with dataclasses or Pydantic models
2. Create `backend/app/database.py` for SQLite connection and setup
3. Create `backend/app/repositories/` for data access
4. Implement schema creation (SQL or ORM)
5. Add repository methods (get_artworks, get_collection, etc.)
6. Write tests for repositories with test database

**Files:**
- `backend/app/models.py` (new)
- `backend/app/database.py` (new)
- `backend/app/repositories/artwork_repository.py` (new)
- `backend/app/repositories/collection_repository.py` (new)
- `backend/tests/test_repositories.py` (new)

**Exit criteria:**
- Can create SQLite database
- Can insert and query data via repositories
- Tests pass with in-memory test DB

---

### Step 2.4: Populate Database with Real Artwork Data
**Why separate**: Data entry is distinct from code implementation

**Deliverable**: SQLite database with your actual artwork data

**Tasks:**
1. Create data seeding script or migration
2. Add your artwork images to appropriate directory (e.g., `backend/static/images/`)
3. Populate database with real artwork metadata
4. Add artist information
5. Create initial collection(s)
6. Document data update process

**Files:**
- `backend/scripts/seed_data.py` (new) or similar
- `backend/data/gallery.db` (new - the SQLite file)
- `backend/static/images/` (new - artwork images)
- `backend/app/main.py` (add static file serving if needed)

**Exit criteria:**
- Database contains real artwork data
- Images accessible via backend
- Can query data via repositories

---

### Step 2.5: Wire GraphQL Schema to Data Layer
**Why last**: Connect the API surface to real persistence

**Deliverable**: GraphQL queries return real data from SQLite

**Tasks:**
1. Update GraphQL resolvers to use repositories instead of hardcoded data
2. Add database connection to GraphQL context
3. Handle query errors gracefully
4. Add integration tests for full GraphQL→DB flow
5. Test via playground with real data

**Files:**
- `backend/app/schema.py` (update resolvers)
- `backend/app/main.py` (add DB context)
- `backend/tests/test_integration.py` (new)

**Exit criteria:**
- GraphQL playground queries return real artwork data
- All tests pass (unit + integration)
- No hardcoded data remains in schema.py

---

## Key Design Decisions for Phase 2

### Artist Modeling
**Single artist (user's father)** - will never be multiple artists.

**Approach**: Model as singleton entity:
- Create `Artist` type in GraphQL schema
- One artist record in database (fixed data, not user-managed)
- Artworks reference the artist (proper relational model)
- Future-proof but acknowledges single-artist reality

### Image Storage
**Current state**: Some local files, primary storage is Google Photos

**Phase 2 approach**: Use local files for now
- Store images in `backend/static/images/`
- Serve via FastAPI static files
- Image URLs in database point to local paths
- **Defer Google Photos integration** to avoid complexity
- Can migrate to cloud storage later without schema changes

### Repository Pattern
Separation of concerns:
- GraphQL schema = API contract (what clients see)
- Models = Data structures (internal representation)
- Repositories = Data access layer (how we get data)

This keeps SQLite as an implementation detail that can be swapped later.

---

## Working Forward

Each step above is a clear milestone with a working system at the end.
Natural stopping points for dip-in/dip-out workflow.

**Next**: Step 2.1 - Set Up Testing & Linting Infrastructure
