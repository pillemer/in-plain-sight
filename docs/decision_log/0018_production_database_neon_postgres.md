# Production Database: Neon Postgres

## Context

Decision 0012 planned for SQLite on Railway's persistent disk as the MVP database. During actual deployment, we discovered Railway's container storage is ephemeral - the SQLite database file would be wiped on every redeploy. This made SQLite unviable for production without additional infrastructure.

## Decision

Use Neon Postgres (free tier) as the production database, while keeping SQLite for local development and tests.

**Configuration:**
- Production: `DATABASE_URL` environment variable set in Railway, pointing to Neon
- Local dev: Falls back to `sqlite:///./gallery.db` when no `DATABASE_URL` is set
- Tests: Continue using SQLite (`test_gallery.db`)

**Code changes:**
- Added `psycopg2-binary` dependency for Postgres connectivity
- Made SQLAlchemy's `check_same_thread` conditional (SQLite-only option)
- Database seeding runs locally against Neon via `DATABASE_URL` env var

## Alternatives Considered

1. **Railway Postgres add-on** - $5/month minimum after trial. Rejected due to cost constraint (must be free).

2. **SQLite with persistent volume on Railway** - Railway doesn't support persistent disk for free tier containers. Would require paid plan.

3. **Supabase free tier** - Viable alternative with 500MB storage. Rejected as overkill (includes auth, realtime, storage we don't need). Neon is simpler for just Postgres.

4. **Manual re-seeding after each deploy** - Would work but operationally painful. Data loss on every deploy is unacceptable even for MVP.

## Consequences

**Positive:**
- Data persists across Railway deploys
- Free tier sufficient (0.5GB storage, 100 compute-hours/month)
- SQLAlchemy works identically - just a connection string change
- Local dev remains simple (no Postgres install required)
- Neon auto-sleeps when idle (preserves compute hours)

**Trade-offs:**
- External dependency (Neon account required)
- Slightly slower queries vs local SQLite (network latency)
- Free tier limits exist (adequate for portfolio site)
- Must run seed script manually against Neon when schema changes

**Operational notes:**
- Seed production: `DATABASE_URL='postgresql://...' poetry run python -m app.seed`
- Schema changes require dropping tables in Neon and re-seeding (no migrations yet)
- Neon connection string must use `postgresql://` prefix (not `postgres://`)

## Follow-up

- Consider Alembic migrations when schema changes become frequent
- Monitor Neon free tier usage as traffic grows
- Document Neon setup in README for future contributors

## Related Decisions

- [0004_database_persistence.md](0004_database_persistence.md) - Original SQLite decision
- [0012_deployment_architecture.md](0012_deployment_architecture.md) - Deployment plan that assumed SQLite would work
