# Decision 0005: One-to-many artwork-collection relationships

## Context
The domain model from decision 0003 established that artworks can belong to multiple collections conceptually. When implementing database relationships, we had to decide between a simple one-to-many (artwork belongs to one collection) or full many-to-many (artwork in multiple collections via junction table).

## Decision
Implement simple one-to-many relationships for MVP: an artwork belongs to at most one collection. This is represented as a nullable `collection_id` foreign key on the artwork table.

## Alternatives considered
1. **Many-to-many with junction table** - More flexible and matches conceptual domain model, but adds complexity:
   - Additional table to manage
   - More complex queries and relationships
   - Additional migration work when schema evolves
   - Overkill for current single-collection use case

2. **No collection association** - Too limiting; collections are core to the domain model.

## Consequences
### Positive
- Simpler database schema and queries
- Easier to reason about and debug
- Aligns with "minimal viable, no over-engineering" project philosophy
- Current requirement (one "Selected Works" collection) fully supported
- Foreign key relationship is straightforward to query and manage

### Negative
- If requirements change to support artworks in multiple collections, migration will be required
- Less flexibility than the conceptual domain model suggests

### Migration path
When/if many-to-many is needed:
1. Create junction table `artwork_collections`
2. Migrate existing `collection_id` data to junction table
3. Remove `collection_id` column from artworks table
4. Update repository queries to use junction table
5. GraphQL schema remains unchanged (relationships abstracted by repositories)

This decision explicitly favors simplicity now over flexibility later, documented for future context.