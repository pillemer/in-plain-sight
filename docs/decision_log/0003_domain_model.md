# Decision 0003: Domain-driven API model

## Context
Initial GraphQL experimentation used a simple “Image” model. As the project intent clarified, it became clear this did not accurately reflect the real-world concepts being represented.

## Decision
The API will be structured around the domain concepts of Artwork and Collection. Artworks are the primary entity, and collections represent curated groupings. Other concepts such as artist metadata, descriptions, and AI-generated content are explicitly deferred.

## Alternatives considered
- Keeping a generic Image model, which would limit future evolution.
- Fully modelling all anticipated concepts upfront, which would overcomplicate early development.

## Consequences
The API now aligns with real-world meaning and can support frontend development confidently. Some future features will require schema extension, but the core model is stable and intentionally minimal.
