# Decision 0007: Separate test database

## Context
Initial test setup used the same `gallery.db` file as development. This created a critical issue: running tests would wipe development data during test setup/teardown. This violated test isolation principles and made development workflow fragile.

## Decision
Use a separate SQLite database file for tests (`test_gallery.db`) by setting the `DATABASE_URL` environment variable before importing application modules.

### Implementation
- `database.py` reads `DATABASE_URL` from environment with fallback to `gallery.db`
- Test files set `os.environ["DATABASE_URL"] = "sqlite:///./test_gallery.db"` before any app imports
- Environment variable must be set early to ensure all modules use test database during import

## Alternatives considered
1. **Shared database with careful cleanup** - Rejected as too fragile; any test failure could corrupt dev data.

2. **In-memory SQLite (`:memory:`)** - Considered but rejected because:
   - Cannot inspect database state after test failure for debugging
   - Slower test startup (recreates schema every run)
   - Cannot run tests against persistent state to debug intermittent issues

3. **Separate test configuration file** - More complex than environment variable; over-engineered for this use case.

4. **Mock database layer** - Would not actually test database integration, defeating purpose of integration tests.

## Consequences
### Positive
- Development database safe from test runs
- Can inspect `test_gallery.db` after test failures for debugging
- Tests can run in parallel with development server
- Standard pattern (environment-based config) that scales to staging/production
- Test database persists between runs, allowing investigation of failures

### Negative
- Two database files to manage (minor; can add to `.gitignore`)
- Must remember to set environment variable early in test files
- Test database grows over time (can be deleted and recreated anytime)

### Future considerations
When deploying to staging/production:
- Use same environment variable pattern for Postgres connection strings
- Consider separate databases per environment (dev, test, staging, prod)
- Test database should be ephemeral in CI/CD (can use `:memory:` there)
