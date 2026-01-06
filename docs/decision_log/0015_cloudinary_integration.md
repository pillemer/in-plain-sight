# Cloudinary Integration for Artwork Assets

## Context

The gallery needed real artwork images instead of placeholder content. Initial attempts with hardcoded URLs proved brittle — any change to folder structure or filenames would break the gallery. A more sustainable approach was needed that could scale with the artwork collection.

## Decision

Integrate with the Cloudinary Admin API to dynamically fetch available artwork.

**Implementation:**
- Added `cloudinary` Python package to backend dependencies
- Seed script uses `cloudinary.api.resources()` to list uploaded images
- Image URLs constructed from public IDs returned by the API
- Credentials stored in `.env` (gitignored)

**Visual layer:**
- Added forest background image (`backgroundForest.jpg`) to reinforce the "walking through forest" navigation metaphor
- Background applied as fixed, covering image on gallery container
- Artwork titles hidden when empty (no placeholder text)

## Consequences

**Positive:**
- No hardcoded image URLs — upload to Cloudinary, re-seed, done
- Single source of truth for artwork assets
- Background image reinforces immersive gallery experience
- Clean UI with no placeholder text visible

**Trade-offs:**
- Requires Cloudinary API credentials in environment
- Seed script requires network access to Cloudinary
- No metadata (titles) for artworks currently — would need to come from Cloudinary tags or separate source

## Follow-up

- Consider storing artwork metadata (titles, dates) in Cloudinary asset context or separate data source
- Add image optimization transforms to Cloudinary URLs

## Related Decisions

- [0014_depth_camera_navigation.md](0014_depth_camera_navigation.md) — Gallery navigation implementation
