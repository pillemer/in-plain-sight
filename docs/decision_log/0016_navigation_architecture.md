# Multi-Page Navigation Architecture

## Context

The initial MVP focused on a single gallery page. To support an "About" page and future galleries, the site needed proper navigation without breaking the immersive art-first experience.

## Decision

Implement React Router with a persistent Header component containing dropdown navigation.

**Structure:**
- Routes: `/` (gallery), `/about` (bio page)
- Header component shared across pages
- Galleries dropdown with active collection + disabled placeholder collections
- Nav links styled consistently with gallery aesthetics

**Dropdown behavior:**
- Shows all collections (real + placeholder)
- Only "Watercolours" clickable initially (routes to `/`)
- "Oils" and "Sketches" shown as disabled (future collections)
- Click outside or select closes dropdown

**Data flow:**
- Header receives collections from GraphQL query
- Bio page queries artist data separately
- Collections list shared between Gallery and Bio pages

## Consequences

**Positive:**
- Clear pattern for adding new collection pages
- Maintains visual restraint (no prominent nav chrome)
- Future collections visible but not functional (scope clarity)

**Trade-offs:**
- Placeholder collections hardcoded in dropdown vs hiding them entirely
- Each page fetches collections independently (acceptable duplication for simplicity)
- No active route highlighting beyond collection title matching

## Follow-up

- When adding second collection: create route, update GalleriesDropdown active logic
- Consider header visibility behavior (always visible vs hide on scroll)

## Related Decisions

- [0013_frontend_implementation.md](0013_frontend_implementation.md) — Frontend foundation
- [0014_depth_camera_navigation.md](0014_depth_camera_navigation.md) — Gallery navigation
