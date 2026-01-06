# Depth Camera Gallery Navigation

## Context

The default gallery layout (grid/list with vertical scroll) didn't match the project's art-first vision. The goal was to create an immersive experience where viewing artwork feels like walking through a forest path — moving through depth rather than scrolling past content.

## Decision

Implement a JS-driven depth camera navigation system using CSS 3D transforms (no 3D libraries).

**Core mechanics:**
- Scrolling moves a virtual "camera" along a depth axis
- Each artwork exists at a fixed Z-position in 3D space
- Artworks approach, come into focus, then recede behind as the viewer scrolls
- Native scroll container with RAF-throttled state updates
- CSS transitions for smooth visual changes

**Architecture:**
- `GalleryView.tsx` — container, scroll handling, camera state
- `Artwork.tsx` — stateless presentation component (memoized)
- `useCamera.ts` — custom hook mapping scroll to camera position
- `calculations.ts` — pure functions for visual state

## Consequences

**Positive:**
- Creates unique, immersive gallery experience matching the vision
- No heavy 3D dependencies (CSS 3D transforms have 95%+ browser support)
- Configurable parameters allow rapid iteration on feel
- Performance optimized via culling, throttling, memoization

**Trade-offs:**
- Removed blur filter for performance
- Disabled pointer events on artworks during navigation (click-to-expand deferred)
- Title only visible when artwork is in focus

## Follow-up

- Add click-to-expand for focused artwork
- Consider thumbnail images for scroll view
- Test on mobile devices

## Related Decisions

- [0013_frontend_implementation.md](0013_frontend_implementation.md) — Frontend foundation
