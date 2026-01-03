# Decision 0010: Multimodal image input via URL fetch and binary conversion

## Context
Phase 3 AI integration initially sent only artwork metadata (title, artist name) to Gemini API. This meant the AI was generating visual descriptions without actually seeing the artwork images, leading to hallucinated content that violated the "no invented facts" boundary.

To provide visually-grounded interpretations, the AI needs access to actual artwork images. Gemini API supports multimodal input but offers multiple methods for providing images.

## Decision
**Fetch artwork images from URLs and convert to binary data** for inline transmission to Gemini API via `Part.from_bytes()`.

### Implementation
- Add `httpx` as a production dependency for async HTTP requests
- Fetch image from `artwork.image_url` on each interpretation request
- Convert HTTP response to binary bytes
- Detect MIME type from `Content-Type` header (fallback to `image/jpeg`)
- Send image + text prompt together as multimodal input to Gemini
- Timeout set to 10 seconds for image fetching

```python
async with httpx.AsyncClient() as http_client:
    image_response = await http_client.get(artwork.image_url, timeout=10.0)
    image_bytes = image_response.content
    mime_type = image_response.headers.get("content-type", "image/jpeg")

contents = [
    types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
    prompt_text,
]
```

## Alternatives considered

### 1. Direct URL reference via Google Cloud Storage
Use `Part.from_uri()` to reference images stored on GCS.

**Pros:**
- Zero latency (Gemini fetches directly from GCS)
- No bandwidth costs (Google internal network)
- Scales infinitely

**Cons:**
- Requires Google Cloud Storage (vendor lock-in)
- Cannot use public domain URLs (Met Museum, WikiArt, etc.)
- More complex deployment (need GCS bucket setup)
- Over-engineered for MVP

**Verdict:** Rejected - too much infrastructure for MVP, incompatible with public domain art sources

### 2. Gemini File API (upload and reuse)
Upload images to Gemini's File API once, then reference file ID across multiple requests.

**Pros:**
- Image uploaded once, reused across requests
- Faster subsequent requests (no re-fetch)
- Better quota management

**Cons:**
- Two-step process (upload, then generate)
- File lifecycle management complexity (when to upload? when to delete?)
- Over-engineered for MVP (we generate interpretations rarely)
- Doesn't fit ephemeral interpretation model

**Verdict:** Rejected - premature optimization, adds complexity

### 3. Public HTTP URLs without fetching
Attempt to pass public URLs directly to Gemini (some APIs support this).

**Pros:**
- Simplest implementation (no fetching logic)
- Lowest latency

**Cons:**
- Gemini API documentation doesn't indicate support for arbitrary HTTP URLs
- `Part.from_uri()` is documented for GCS URIs only (`gs://` scheme)
- Would require experimentation to verify if it works
- Uncertain reliability

**Verdict:** Rejected - not documented as supported, too risky for MVP

### 4. IIIF Image Protocol URLs
Use IIIF-compatible image servers that support on-the-fly transformations.

**Pros:**
- Industry standard for museums/galleries
- Built-in image transformations (resize, rotate, crop)
- Many public domain sources support it (Met, Smithsonian, Harvard)
- Future-proof (widely adopted)

**Cons:**
- Requires IIIF-compatible image server for own artwork
- Still need to fetch as binary to send to Gemini
- Doesn't fundamentally change architecture

**Verdict:** Interesting for future optimization, but doesn't solve the core problem

## Consequences

### Positive
- **Works with any public URL** - Met Museum, WikiArt, your own hosting, CDNs
- **Simple architecture** - Straightforward fetch → convert → send flow
- **No external dependencies** beyond HTTP client (httpx)
- **Future-proof** - Can optimize later (caching, File API) without interface changes
- **Testable** - Easy to mock httpx for unit tests
- **Visually grounded** - AI now analyzes actual artwork images

### Negative
- **Latency** - Fetches image on every request (adds ~200-500ms)
- **Bandwidth** - Downloads full image each time (no caching)
- **Could hit CDN rate limits** - Some image hosts may throttle repeated requests
- **No image reuse** - Fetches same image multiple times if interpretation regenerated

### Mitigations
- Free tier quota (1000 req/day) sufficient for MVP development
- 10-second timeout prevents hanging on slow image servers
- Can add caching layer later (in-memory, Redis, File API) without changing interface
- Public domain sources (Met Museum) have generous rate limits
- Image fetching happens server-side (not client bandwidth)

### Future optimization paths
1. **Add in-memory caching** - Cache fetched images for 1 hour
2. **Use Gemini File API** - Upload images once, reuse across sessions
3. **Add CDN/proxy** - Serve images through own CDN to control caching
4. **Implement hybrid approach** - File API for own artwork, URL fetch for public domain

None of these require changing the public API or GraphQL schema.

## HTTP Client Selection (httpx vs aiohttp)

**Chose httpx** over aiohttp for async HTTP requests.

**Rationale:**
- Supports both sync and async (flexibility for testing)
- HTTP/2 support (faster for modern servers)
- Fully type-annotated (better IDE support, catches errors early)
- Similar API to `requests` (familiar, easy to learn)
- Modern, actively maintained

**Trade-off:**
- Slightly slower than aiohttp in extreme high-concurrency scenarios
- Additional dependency (not in stdlib)

**Why not aiohttp:**
- Async-only (no sync fallback for testing)
- Less intuitive API (more verbose)
- Not fully type-annotated

**Why not urllib (stdlib):**
- No native async support
- Clunky API requiring lots of boilerplate
- No HTTP/2

**Verdict:** httpx is the best balance of clean API, type safety, and async support for this use case

## Related decisions
- **0008: Ephemeral AI interpretations** - Established separate query approach
- **0009: Google Gemini API selection** - Chose Gemini 2.0 Flash Lite for free tier

## Impact on testing
- Unit tests mock httpx requests (no real HTTP calls)
- Integration tests can use real public domain URLs or mock responses
- Test coverage ensures image fetch failures are handled gracefully

## Prompt engineering enhancement
Updated prompt to emphasize visual grounding:
- Added "based on what you see in the image"
- Changed "observed, not factual" to "visual observation only"
- Reinforced "base your interpretation only on what you can see"

This ensures AI leverages the visual input rather than relying on text-based knowledge.
