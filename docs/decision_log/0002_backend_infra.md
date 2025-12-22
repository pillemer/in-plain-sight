# Decision 0002: Backend stack and infrastructure

## Context
The project required a backend that could support a modern frontend, evolve incrementally, and clearly demonstrate full-stack engineering skills without unnecessary complexity.

## Decision
The backend will use Python 3.13, FastAPI, and Strawberry GraphQL, managed with Poetry. Infrastructure will be set up in a dedicated phase before any domain or UI work begins.

## Alternatives considered
- A Node.js-based stack, which would overlap heavily with prior experience and reduce learning value.
- REST-only APIs, which would limit expressiveness and schema clarity for the frontend.
- Introducing a database early, which would add complexity without immediate benefit.

## Consequences
This setup provides a clean, typed API surface and clear separation of concerns. It postpones persistence and deployment decisions, keeping the system lightweight while remaining extensible.
