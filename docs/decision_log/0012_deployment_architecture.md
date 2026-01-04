# Decision 0012: Deployment architecture - separate frontend and backend

## Context
The project uses a monorepo structure with `/backend` (Python/FastAPI) and `/frontend` (React/Vite) folders. Deployment strategy must:
- Work within free tier constraints (£0 budget)
- Support auto-deployment from GitHub on push
- Provide good performance globally
- Be straightforward to maintain
- Demonstrate professional deployment architecture for portfolio/CV

## Decision
Deploy frontend and backend **separately to different platforms**:
- **Backend:** Railway (Python/FastAPI optimized)
- **Frontend:** Vercel (React/Vite optimized)

### Architecture
```
GitHub Monorepo
├── /backend  → Railway   → https://in-plain-sight-api.railway.app
├── /frontend → Vercel    → https://in-plain-sight.vercel.app
└── /docs
```

Frontend makes API requests to backend URL via GraphQL endpoint.

## Alternatives considered

### 1. Backend serves frontend (single deployment)
**Implementation:**
- Build frontend → `/frontend/dist`
- FastAPI serves static files from `/dist`
- Single deployment, single URL

**Pros:**
- Simplest deployment (one service)
- No CORS configuration needed
- Single URL to manage

**Cons:**
- Backend doing double duty (API + static hosting)
- No CDN for frontend assets (slower global access)
- Backend restarts affect frontend availability
- Goes against modern best practices
- Harder to scale independently
- Wastes backend resources on static file serving

**Verdict:** Rejected - couples concerns, poor performance, unprofessional

### 2. Vercel monorepo (both services)
**Implementation:**
- Two Vercel projects from one GitHub repo
- Project 1: `/frontend` → `yoursite.vercel.app`
- Project 2: `/backend` → `yoursite-api.vercel.app`

**Pros:**
- Single platform (simpler mental model)
- Excellent auto-deployment
- Both on free tier

**Cons:**
- Vercel Python support is serverless (cold starts ~1-2 sec)
- Less ideal for Python than dedicated Python hosting
- Backend can't maintain persistent connections easily
- SQLite database persistence issues in serverless

**Verdict:** Rejected - Vercel not optimized for Python backends

### 3. Both on Railway
**Implementation:**
- Two Railway services from one repo
- Service 1: `/backend`
- Service 2: `/frontend`

**Pros:**
- Single platform
- Railway handles both well

**Cons:**
- Frontend not on CDN (slower global access)
- Vercel specializes in frontend, offers better performance
- Railway free tier limited to 500 hours/month across all services

**Verdict:** Rejected - Vercel superior for frontend hosting

### 4. Netlify + Railway
**Implementation:**
- Backend: Railway
- Frontend: Netlify

**Pros:**
- Similar to recommended approach
- Netlify excellent for frontend

**Cons:**
- Vercel slightly better React/Vite integration
- Vercel preview deployments superior
- Vercel more commonly used (CV recognition)

**Verdict:** Viable alternative, but Vercel preferred

## Consequences

### Positive
- **Optimized performance** - Each platform does what it does best
  - Railway: Long-running Python processes, database persistence
  - Vercel: Global CDN, edge caching, instant page loads
- **Independent scaling** - Frontend and backend scale separately
- **Fast frontend delivery** - Vercel's global CDN ensures fast access worldwide
- **Professional architecture** - Demonstrates understanding of modern deployment patterns
- **Free tier generous** - Railway: 500 hrs/month, Vercel: unlimited hobby projects
- **Auto-deployment** - Both platforms auto-deploy on git push
- **Preview deployments** - Vercel creates preview URLs for each PR
- **Environment isolation** - Frontend and backend env vars managed separately

### Negative
- **Two platforms to manage** - Slightly more operational overhead
- **CORS configuration required** - Must configure backend to accept frontend origin
- **Environment variables** - Must set API URL in frontend, frontend URL in backend
- **Two deployments** - Git push triggers two separate builds

### Mitigations
- Both platforms have excellent auto-deployment (minimal management)
- CORS is straightforward with FastAPI middleware (single decorator)
- Env vars are one-time setup, documented in README
- Separate deployments allow independent updates (actually a benefit)

## Implementation details

### Railway (backend)
**Configuration:**
- Service name: `in-plain-sight-api`
- Root directory: `/backend`
- Build command: `poetry install`
- Start command: `poetry run uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Auto-generates URL: `https://in-plain-sight-api.up.railway.app`

**Environment variables:**
- `GEMINI_API_KEY` - Google Gemini API key
- `DATABASE_URL` - SQLite path or Postgres URL (Railway provides Postgres plugin)
- `FRONTEND_URL` - Vercel frontend URL (for CORS)
- `ENVIRONMENT` - `production`

**Free tier limits:**
- 500 execution hours/month
- $5 free credit/month
- Sufficient for portfolio site traffic

### Vercel (frontend)
**Configuration:**
- Framework preset: Vite
- Root directory: `/frontend`
- Build command: `npm run build`
- Output directory: `dist`
- Auto-generates URL: `https://in-plain-sight.vercel.app`

**Environment variables:**
- `VITE_API_URL` - Railway backend GraphQL endpoint
  - Development: `http://localhost:8000/graphql`
  - Production: `https://in-plain-sight-api.up.railway.app/graphql`

**Free tier limits:**
- Unlimited projects (hobby plan)
- 100 GB bandwidth/month
- More than sufficient for gallery site

### CORS configuration
Backend FastAPI middleware:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "https://in-plain-sight.vercel.app",  # Production
        "https://*.vercel.app",  # Preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Deployment workflow
```bash
# Developer workflow:
1. Make changes to frontend or backend
2. git commit && git push
3. Railway auto-deploys backend (if /backend changed)
4. Vercel auto-deploys frontend (if /frontend changed)
5. Both services automatically restart with new code

# Preview deployments:
- Every PR gets a Vercel preview URL
- Can test frontend changes before merging
- Backend changes deploy to Railway staging environment (optional)
```

## Database persistence consideration
Railway supports persistent disk storage, making SQLite viable for MVP. For production scaling, Railway offers managed Postgres plugin (also free tier available). Migration path:
1. MVP: SQLite on Railway persistent disk
2. Growth: Railway Postgres (one-click plugin)
3. Scale: External Postgres (Neon, Supabase free tiers)

## Rationale summary
This architecture was chosen to:
1. **Optimize for each concern** - Frontend on CDN, backend on compute
2. **Maximize free tier value** - Best free hosting for each technology
3. **Demonstrate professionalism** - Industry-standard separation of concerns
4. **Enable performance** - Global CDN for art gallery is critical
5. **Simplify development** - Clear boundaries, independent deploys

The separation of frontend and backend is a modern best practice that shows understanding of scalable web architecture while remaining simple to operate.

## Related decisions
- **0011: Frontend technology stack** - Vite + React stack designed for Vercel
- **0009: Google Gemini API** - Backend needs env var management for API key
- **Future decision needed:** When/if to migrate SQLite → Postgres

## References
- [Railway Python deployment docs](https://docs.railway.app/guides/python)
- [Vercel monorepo deployment](https://vercel.com/docs/monorepos)
- [FastAPI CORS middleware](https://fastapi.tiangolo.com/tutorial/cors/)
