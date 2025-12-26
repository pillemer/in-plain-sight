# In Plain Sight

A single-page digital art gallery that presents the work of a single artist in a calm, intentional space, with an optional "behind the curtain" layer that exposes how the system is built.

For full project intent and constraints, see `docs/project_context.md`.

## Repository layout
- `docs/` – authoritative project context and decisions
- `backend/` – Python backend package managed with Poetry

A React/SASS frontend is planned. The FastAPI + Strawberry GraphQL backend skeleton is implemented.

## Backend setup

### Prerequisites
- Python 3.13+
- [Poetry](https://python-poetry.org/) installed

### Install dependencies
```bash
cd backend
poetry install
```

Once the FastAPI/Strawberry app is implemented, the canonical commands to run the server, tests, and linting should be documented.