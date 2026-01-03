# Decision 0008: Ephemeral AI interpretations for MVP

## Context
Phase 3 introduces AI-generated artwork interpretations using Google Gemini API. The AI acts as a "curator's note" - providing third-person observations about colors, composition, mood, and texture. Two architectural questions needed resolution:

1. **Persistence strategy**: Should AI interpretations be stored in the database or generated fresh on each request?
2. **API exposure**: Should interpretations be a field on the Artwork type or a separate query?

The project has a £0 budget requiring free tier API usage (1000 requests/day on Gemini).

## Decision
**For MVP (Phase 3):** Use fully ephemeral AI interpretations via a separate GraphQL query.

### Implementation
- New query: `generateArtworkInterpretation(artworkId: String!): AIInterpretation`
- Each request generates a fresh interpretation (no database persistence)
- Response includes ephemeral ID, content, timestamp, and context
- AI service layer (`ai_service.py`) encapsulates Gemini API calls
- Prompt engineering enforces hard boundaries (no invented facts, third-person only)

## Alternatives considered

### 1. Field on Artwork type (auto-generated on load)
```graphql
type Artwork {
  aiInterpretation: AIInterpretation
}
```

**Pros:**
- More intuitive API (interpretation is "part of" the artwork)
- Cleaner GraphQL queries

**Cons:**
- Every artwork page load = API call (expensive at scale)
- No way to avoid regeneration on refresh
- Less explicit cost control

**Verdict:** Rejected for MVP - too expensive once deployed

### 2. Hybrid: Session-based caching with TTL
Generate on first request, cache in database with 1-hour expiration, background cleanup job.

**Pros:**
- Best UX (feels immediate after first load)
- Cost-effective (API calls limited by TTL)
- Still feels dynamic

**Cons:**
- Significantly more complex (caching, TTL, cleanup)
- Premature optimization for MVP
- Contradicts "ephemeral initially" constraint from project docs

**Verdict:** Deferred to future phase - documented as long-term direction

### 3. Pre-generated and persisted (canonical)
Generate once during seeding, treat as canonical data.

**Pros:**
- Zero runtime API costs
- Fast response times

**Cons:**
- Violates "descriptions may vary between requests" requirement
- Loses freshness benefit
- Becomes stale content, not dynamic AI

**Verdict:** Rejected - contradicts project goals

## Consequences

### Positive
- **Simple implementation** - No caching logic, TTL, or cleanup jobs
- **Explicit cost control** - User decides when to generate (via button click)
- **Easy to test** - Can mock AI service cleanly
- **Truly ephemeral** - Aligns with initial project constraint
- **Easy migration path** - Can add caching later without breaking changes
- **Matches "gimmick" framing** - Interpretation is supplemental, not core experience

### Negative
- **API call per request** - Could hit free tier limits during heavy testing
- **No caching** - Refreshing page regenerates (wastes quota)
- **Less magical UX** - Requires user action (but matches "button on page" idea)

### Mitigations
- Free tier quota (1000 req/day) sufficient for MVP development
- Prompt caching can be added if quota becomes issue
- Can implement hybrid model (Alternative 2) in future phase without schema changes

### Future migration path
When ready to implement session-based caching:
1. Add `expires_at` and `artwork_id` fields to `AIInterpretation` model
2. Create repository methods: `save_interpretation()`, `get_cached_interpretation()`
3. Update resolver to check cache before generating
4. Add background job to cleanup expired interpretations
5. Add `regenerate: Boolean` argument to query for explicit regeneration

This path is documented in `phase3-ai-integration.md` but not implemented in Phase 3.

## Related decisions
- **0003: Domain model** - Established `AIInterpretation` type in schema
- **Future decision needed:** When to implement hybrid caching model
