# In Plain Sight

A single-page digital art gallery that presents the work of a single artist in a calm, intentional space, with an optional "behind the curtain" layer that exposes how the system is built.

**The concept:** Two concurrent experiences in one site—a public-facing art gallery and a hidden technical overlay that reveals architecture, AI usage, and development decisions. Art-first on the surface, radically transparent underneath.

For full project intent and constraints, see [docs/project_context.md](docs/project_context.md).

## Current Status

**Backend:**
- FastAPI + Strawberry GraphQL server
- SQLite database with SQLAlchemy ORM
- Domain model: Artist, Artwork, Collection, AI Interpretation
- AI-powered artwork interpretation via Google Gemini (multimodal vision)
- Cloudinary integration for artwork asset management
- Comprehensive test suite
- CORS configured for frontend

**Frontend:**
- Vite + React 18 + TypeScript
- TanStack Query + GraphQL Code Generator
- SCSS Modules with modern architecture
- Immersive depth-camera gallery navigation (CSS 3D transforms)
- Full end-to-end integration with backend

## Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+
- [Poetry](https://python-poetry.org/) installed
- Google Gemini API key (for AI features)
- Cloudinary account (for artwork assets)

### Backend Setup

```bash
# Install dependencies
cd backend
make install

# Set up environment (create backend/.env file)
# Copy from .env.example and fill in your keys
cp .env.example .env

# Seed the database with artwork from Cloudinary
make seed

# Start the development server
make dev
```

Required environment variables (see `.env.example`):
- `GEMINI_API_KEY` - [Google AI Studio](https://aistudio.google.com/apikey)
- `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` - [Cloudinary Console](https://console.cloudinary.com/settings/api-keys)

The GraphQL playground will be available at `http://localhost:8000/graphql`

### Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Set up environment (create frontend/.env.local file)
echo "VITE_API_URL=http://localhost:8000/graphql" > .env.local

# Generate TypeScript types from GraphQL schema (backend must be running)
npm run codegen

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

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
│   │   ├── seed.py    # Database seeding from Cloudinary
│   │   └── ai_service.py  # AI service integration
│   ├── tests/         # Test suite
│   └── Makefile       # Development commands
└── frontend/          # React + TypeScript application
    ├── src/
    │   ├── pages/     # Page components
    │   ├── components/# React components
    │   │   └── Gallery/  # Depth-camera gallery system
    │   ├── styles/    # SCSS modules
    │   ├── queries/   # GraphQL query definitions
    │   └── lib/       # Client setup
    └── README.md      # Frontend documentation
```

## Development

### Backend Commands

From the `backend/` directory:

```bash
make dev      # Start dev server with hot reload
make test     # Run test suite
make lint     # Check code with ruff
make format   # Format code with ruff
make seed     # Seed database with sample data
```

### Frontend Commands

From the `frontend/` directory:

```bash
npm run dev           # Start dev server with HMR
npm run build         # Build for production
npm run codegen       # Generate TypeScript types from GraphQL schema
npm run codegen:watch # Watch mode for codegen
```

See [frontend/README.md](frontend/README.md) for detailed frontend documentation.

## Technology Stack

**Backend:**
- Python 3.13
- FastAPI (web framework)
- Strawberry GraphQL
- SQLAlchemy (ORM)
- SQLite (database, Postgres planned)
- Google Gemini API (AI interpretation)
- Cloudinary (artwork asset management)
- Poetry (dependency management)

**Frontend:**
- Vite (build tool)
- React 18 + TypeScript
- TanStack Query (data fetching)
- graphql-request + GraphQL Code Generator (type-safe GraphQL)
- React Router (routing)
- SCSS Modules (styling)

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