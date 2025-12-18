# Behind the Curtain – Art Gallery

## Authoritative Project Context

**Audience:** AI development agents collaborating with a human senior engineer

**Status:** Active – single‑page demo phase

This document is the **single source of truth** for the project. AI agents must treat it as binding. When ambiguities arise, default to the principles and non‑goals defined here rather than inventing new scope.

This document is intentionally opinionated. Decisions are made early to avoid drift.

---

## 1. Project Identity

This is **an art gallery first, and a technical artefact second**.

The primary purpose of the system is to present the work of a single artist in a calm, elegant, and respectful digital space. The technical sophistication exists in service of that goal, not alongside it.

The same system also acts as a **transparent demonstration of how it is built**, accessible only to visitors who deliberately look for it.

There is **one product**, viewed through two lenses:

- **The Gallery** – the default, public‑facing experience
- **Behind the Curtain** – an optional explanatory overlay revealing structure, decisions, and process

There are not two websites, two modes of navigation, or two identities.

---

## 2. Intended Visitors

### Primary visitors
- People interested in the artist’s work
- Visitors directed to “the artist’s website” by the artist himself
- Viewers with no technical background

For these visitors:
- The site must feel complete, intentional, and non‑technical
- Nothing should accidentally reveal implementation details
- The curtain layer must never interrupt or confuse the art experience

### Secondary visitors
- Technically minded visitors
- Hiring managers and engineers evaluating the developer

For these visitors:
- The system should reward curiosity
- Technical explanations should be clear, honest, and grounded in real decisions

---

## 3. Curtain Visibility Philosophy

The curtain is **hidden in plain sight**.

- It should be discoverable without instructions
- It should not be visually loud
- It should not be triggered accidentally

Think:
- a subtle icon
- a discreet text affordance
- a gesture or interaction that feels intentional

Activating the curtain should feel like *choosing* to look closer, not stumbling into a feature.

---

## 4. Position on AI

AI is treated as:

> **an assistant that offers interpretations, not authority**.

AI does not speak *for* the artist. It offers alternative lenses through which a viewer might understand the work.

AI is also part of the **development process itself**, acting as a junior developer collaborating under human supervision.

Both roles are explicit and inspectable.

---

## 5. AI in the Art Experience

### Role
- Generate textual interpretations of artworks
- Reduce the need for manual curation as new works are added
- Offer consistency without flattening meaning

### Behaviour
- AI descriptions are **generated dynamically** when a page is requested
- Output is constrained by prompt design and schema
- Variations between visits are acceptable and intentional

### Framing
- AI text must be clearly framed as *interpretation*, not fact
- Tone should be reflective and descriptive, not authoritative

AI output is ephemeral by default. Persistence, caching, or approval workflows are future considerations, not part of the initial demo.

---

## 6. AI in the Development Process

AI agents participating in development are considered **junior engineers**.

They are expected to:
- Propose solutions
- Ask clarifying questions
- Implement approved designs
- Log reasoning and trade‑offs

They are not expected to:
- Introduce scope unilaterally
- Optimise prematurely
- Override established decisions

Human decisions override AI suggestions. Rejected AI ideas are valuable and should be logged.

This collaboration model is itself part of the system’s story and may be surfaced behind the curtain.

---

## 7. Initial Scope (Strict)

This project intentionally begins with **one complete page**.

### Included
- One gallery / collection landing page
- A small set of artworks (3–8 images)
- Dynamically generated AI interpretations
- Curtain overlay explaining selected decisions
- Fully styled, finished‑feeling experience

### Explicit Non‑Goals (for this phase)
- Multiple pages or routes
- CMS or admin UI
- User accounts or authentication
- E‑commerce or payments
- SEO optimisation
- Analytics
- Social features

If something is not listed above, it is out of scope.

---

## 8. Domain Model (Initial)

### Artist
- id
- name
- bio (optional)

### Collection
- id
- title
- description (optional)
- order

### Artwork
- id
- collection_id
- title (optional)
- year (optional)
- medium (optional)
- dimensions (optional)
- image_url
- artist_notes (optional)

### AI_Interpretation
- artwork_id
- mode (e.g. FORMAL, EMOTIONAL, ACCESSIBLE)
- generated_text
- prompt_summary
- generated_at

### Engineering_Note
- scope (PAGE | COMPONENT | API | AI | PROCESS)
- title
- explanation
- trade_offs
- created_at

Engineering notes are first‑class data and may be selectively exposed in curtain mode.

---

## 9. Backend Architecture (Initial)

### Language
- Python 3.12+

### Framework
- FastAPI

### API Style
- GraphQL using Strawberry

Rationale:
- Explicit schema supports explanation
- Frontend can query only what it needs
- Clear separation between domain and presentation

### Data Storage
- SQLite (initial)

Chosen for simplicity, zero cost, and ease of explanation. Migration to Postgres is intentionally deferred.

### Image Hosting
- External image URLs (e.g. Google Photos / Drive shared links)

Images are treated as opaque resources behind URLs. No image processing pipeline exists in the demo.

---

## 10. Frontend Architecture

### Framework
- React (tooling chosen for clarity over novelty)

### Styling
- SCSS / SASS
- No utility‑class frameworks

Styling should feel authored, restrained, and durable.

### Visual Direction
- Quiet
- Spacious
- Gallery‑like
- “A finished room with no visible doors yet”

---

## 11. Curtain Mode Behaviour

When activated:
- The page does not navigate
- Content remains visible
- An overlay augments, not replaces, the experience

Curtain elements may include:
- Callouts explaining layout choices
- Notes on data flow (high‑level)
- Explanations of AI usage and constraints
- Commentary on rejected alternatives

Avoid:
- Excessive animation
- Performance metrics
- Decorative tech motifs

Words and judgement matter more than spectacle.

---

## 12. Documentation as a Feature

Every meaningful decision should produce at least one Engineering_Note.

This includes:
- Technology choices
- Rejected alternatives
- AI prompt design
- Scope decisions

Documentation is not ancillary. It is part of the system.

---

## 13. Success Criteria (Demo)

The demo is successful if:
- The page feels complete and intentional
- The art experience stands on its own
- The backend is explainable without hand‑waving
- AI usage feels thoughtful, not gimmicky
- Curtain mode rewards curiosity without demanding attention

---

## 14. Origin Statement

> This project exists because I wanted to showcase my father’s artwork and my own skills along the way.

This sentence anchors all future decisions.

---

End of authoritative project context.

