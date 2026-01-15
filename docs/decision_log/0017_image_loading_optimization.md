# Image Loading Performance Strategy

## Context

With 20+ artworks rendering in 3D space and potential growth to 50+, image loading needed optimization. Naive eager loading would waste bandwidth; pure lazy loading would cause visible pop-in during scroll. The loading strategy needed to align with the depth camera navigation pattern.

## Decision

Use browser-native lazy loading + fetch priority hints, coordinated with camera position.

**Cloudinary transformations** (applied at seed time):
- `f_auto` — Auto-format (WebP/AVIF/JPEG XL based on browser)
- `q_auto:good` — Intelligent quality compression
- `w_1200` — Max width 1200px (covers 2x retina at 60-80vw display size)
- `dpr_auto` — Automatic retina display support

**Loading strategy** (calculated per artwork):
- **Eager**: Last 2 artworks (visible at scroll=0, camera starts past them)
- **Preload**: Next 3 artworks behind camera (where user is scrolling toward)
- **Lazy**: Everything else

**Browser hints** (applied in Artwork component):
- `loading="eager"` for immediate loads
- `loading="lazy"` + `fetchPriority="high"` for preload zone
- `loading="lazy"` + `fetchPriority="auto"` for distant content

## Consequences

**Positive:**
- Smooth scrolling with no visible image pop-in
- Cloudinary handles format/compression decisions
- Browser-native (no external libraries or custom intersection observers)
- Preload aligned with navigation direction (camera moving backward = load behind)
- Scales to 50+ artworks: only 2-5 images load initially

**Trade-offs:**
- Cloudinary transformations static in URLs (can't adjust per-request)
- Loading hints are suggestions (browser may override)
- No progressive blur-up or skeleton loaders
- Preload strategy depends on scroll direction assumption (works for linear gallery)

## Follow-up

- Monitor scroll performance with 50+ artworks
- Consider dynamic Cloudinary URLs if transformation needs vary
- Test loading behavior across browsers (Safari, Firefox, Chrome)

## Related Decisions

- [0014_depth_camera_navigation.md](0014_depth_camera_navigation.md) — Gallery navigation mechanics
- [0015_cloudinary_integration.md](0015_cloudinary_integration.md) — Cloudinary setup
