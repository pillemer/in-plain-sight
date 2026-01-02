# Decision 0006: Session-per-request via GraphQL context

## Context
Database session lifecycle management is critical for correctness and performance. Initial implementation created a new SQLAlchemy session for each GraphQL resolver call, which meant a single GraphQL query with multiple fields would create multiple database sessions unnecessarily.

## Decision
Implement session-per-request pattern using Strawberry GraphQL's context injection. A single database session is created at the start of each GraphQL request, shared across all resolvers in that request, and properly closed afterward.

### Implementation
- `get_context()` async generator in `main.py` creates session and yields in context dict
- All resolvers accept `info: strawberry.Info` parameter and access session via `info.context["db"]`
- Session cleanup guaranteed by try/finally in context generator

## Alternatives considered
1. **New session per resolver** (original approach) - Simple but inefficient and prevents transaction spanning multiple repository calls.

2. **FastAPI Depends() in resolvers** - Standard FastAPI pattern but has known compatibility issues with Strawberry GraphQL resolvers. Would require workarounds that sacrifice type hints.

3. **Global session** - Not thread-safe; dangerous in async context.

4. **Manual session passing** - Requires explicit session parameter threading through all function calls; verbose and error-prone.

## Consequences
### Positive
- Single session per GraphQL request regardless of query complexity
- Session properly closed even if resolvers raise exceptions
- Follows 2025 best practices for FastAPI + Strawberry integration
- Enables potential future use of database transactions spanning multiple operations
- More efficient: connection reuse, prepared statement caching within request

### Negative
- Resolvers must accept `info` parameter even if only used for session access
- Slight coupling to Strawberry's `Info` type (but acceptable as we're using Strawberry)

### Related decisions
This pattern works with the repository pattern (decision 0004) because repositories accept session as constructor parameter, making them agnostic to how the session is obtained.
