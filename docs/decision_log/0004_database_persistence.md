# Decision 0004: Database persistence with SQLAlchemy

## Context
Phase 2 (Domain & API Shape) had completed with a working GraphQL schema using hardcoded data. The next step required actual database persistence. The choice of database technology, ORM approach, and data access patterns would establish foundational patterns for the entire backend.

## Decision
Use SQLite for initial persistence with SQLAlchemy 2.0 as the ORM, implementing a repository pattern for data access. Database sessions will be managed per-request via Strawberry GraphQL context.

### Key implementation choices:
- SQLite file-based database (not Postgres yet)
- SQLAlchemy 2.0 with modern `Mapped[]` type annotations
- Repository pattern to separate GraphQL from database concerns
- Session-per-request lifecycle via context injection
- Separate test database (`test_gallery.db`) from development database

## Alternatives considered
1. **Direct Postgres from start** - Rejected as over-engineering for MVP. SQLite is sufficient for development and early deployment, with clear migration path to Postgres documented.

2. **Direct SQLAlchemy queries in GraphQL resolvers** - Rejected in favor of repository pattern for cleaner separation, testability, and explainability.

3. **Async SQLAlchemy** - Considered but rejected for MVP. The overhead of async/await everywhere outweighs benefits for current small dataset. Synchronous SQLAlchemy in async FastAPI is acceptable per 2025 best practices when done correctly.

4. **Strawberry-SQLAlchemy auto-mapping** - Rejected in favor of manual `from_model()` class methods. Manual mapping provides more control over GraphQL schema shape and clearer type boundaries.

## Consequences
- Development remains simple with file-based database requiring no external services
- Repository pattern provides clean abstraction that can evolve (e.g., add caching, switch databases)
- Session-per-request prevents multiple session creation within single GraphQL query
- Test isolation protects development data from being wiped during test runs
- Migration to Postgres will require minimal code changes (mostly connection string and deployment config)
- N+1 query issues may emerge at scale but are not premature to optimize for current dataset size