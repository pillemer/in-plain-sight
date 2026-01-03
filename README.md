# In Plain Sight

A single-page digital art gallery that presents the work of a single artist in a calm, intentional space, with an optional "behind the curtain" layer that exposes how the system is built.

**The concept:** Two concurrent experiences in one site—a public-facing art gallery and a hidden technical overlay that reveals architecture, AI usage, and development decisions. Art-first on the surface, radically transparent underneath.

For full project intent and constraints, see [docs/project_context.md](docs/project_context.md).

## Current Status

**Backend (Complete):**
- FastAPI + Strawberry GraphQL server
- SQLite database with SQLAlchemy ORM
- Domain model: Artist, Artwork, Collection, AI Interpretation
- AI-powered artwork interpretation via Google Gemini (multimodal vision)
- Comprehensive test suite
- Seeded sample data

**Frontend:** Planned (React + SCSS/SASS)

## Quick Start

### Prerequisites
- Python 3.13+
- [Poetry](https://python-poetry.org/) installed
- Google Gemini API key (for AI features)

### Installation

```bash
# Install dependencies
cd backend
make install

# Set up environment (create backend/.env file)
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Seed the database with sample data
make seed

# Start the development server
make dev
```

The GraphQL playground will be available at `http://localhost:8000/graphql`

Get your free Gemini API key at [Google AI Studio](https://aistudio.google.com/apikey) (1000 requests/day on free tier).

## Features

### GraphQL API

Query for artists, artworks, and collections:

```graphql
query {
  artist {
    name
    bio
  }

  collections {
    id
    title
    artworks {
      title
      image_url
    }
  }

  artwork(id: "1") {
    title
    medium
    dimensions
  }
}
```

### AI-Powered Interpretation

Generate dynamic artwork interpretations using multimodal AI:

```graphql
query {
  generateArtworkInterpretation(artworkId: "1") {
    content
    generated_at
  }
}
```

AI interpretations are ephemeral, stylistically constrained, and never invent facts. The AI acts as a guest voice, not a curator.

## Repository Structure

```
├── docs/              # Project context, decisions, and architecture
├── backend/           # Python backend (FastAPI + Strawberry GraphQL)
│   ├── app/           # Application code
│   │   ├── main.py    # FastAPI entrypoint
│   │   ├── schema.py  # GraphQL schema
│   │   ├── models.py  # SQLAlchemy models
│   │   └── ai/        # AI service integration
│   ├── tests/         # Test suite
│   └── Makefile       # Development commands
└── frontend/          # (Planned) React application
```

## Development

All commands run from the `backend/` directory:

```bash
make dev      # Start dev server with hot reload
make test     # Run test suite
make lint     # Check code with ruff
make format   # Format code with ruff
make seed     # Seed database with sample data
```

### Running Specific Tests

```bash
poetry run pytest path/to/test_file.py           # Single file
poetry run pytest path/to/test_file.py -k name   # Specific test
```

## Technology Stack

**Backend:**
- Python 3.13
- FastAPI (web framework)
- Strawberry GraphQL
- SQLAlchemy (ORM)
- SQLite (database, Postgres planned)
- Google Gemini API (AI interpretation)
- Poetry (dependency management)

**Frontend (Planned):**
- React
- SCSS/SASS styling
- Framework choice intentionally deferred

## Documentation

- [docs/project_context.md](docs/project_context.md) - Project goals, philosophy, and constraints
- [docs/DECISIONS.md](docs/DECISIONS.md) - Architectural decision log
- [CLAUDE.md](CLAUDE.md) - AI collaboration guidelines

## Project Philosophy

This is not a generic portfolio or tech demo. It's an art gallery that happens to be radically transparent about its construction.

**Core principles:**
- If the art experience fails, the project fails
- AI is a guest voice with hard boundaries (no invented facts, no claimed authority)
- Documentation is a first-class artifact
- "Finished room" quality over sprawling features
- Minimal viable solutions, no premature optimization

See [docs/project_context.md](docs/project_context.md) for the complete specification.