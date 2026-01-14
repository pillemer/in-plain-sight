# In Plain Sight — Project Specification (v1)

## 1. Purpose

In Plain Sight is an art gallery website for a single artist.
Its primary goal is to present artwork beautifully and credibly to a general audience.

Secondarily, it contains a deliberately hidden layer that exposes the technical architecture, development process, and AI collaboration for technically literate visitors and potential employers.

**If the art experience fails, the project fails.**

## 2. Core Concept

The site operates on two concurrent layers:

### 2.1 Surface Layer (Default)

- Public-facing art gallery
- No developer framing
- No visible technical language
- Calm, restrained, art-first design

This is the site the artist shares.

### 2.2 Curtain Layer (Hidden)

- Exists within the same pages and domain
- Intentionally discoverable, not obvious
- When activated, the site visually and informationally transforms

**Exposes:**
- architectural decisions
- tradeoffs
- AI usage
- development process and evolution

This layer is for technically minded visitors only.

## 3. Scope (Strict)

### Initial Deliverable

- One collection landing page
- Small gallery of artworks (10-20 initially, may grow to 50+)
- Fully real backend + frontend
- Production-quality design and structure

> **Metaphor:**
> A finished room in a castle, even if no other doors exist yet.

**Explicitly out of scope (for now):**
- multiple collections
- search
- purchasing
- user accounts
- CMS
- saved AI output

### Performance & Scale Considerations

**Future optimization ( Virtual Scrolling):**
When gallery grows beyond **50 artworks**, consider implementing DOM windowing:
- Only render visible + buffer artworks
- Recycle DOM nodes during scroll
- Libraries: React Window or React Virtuoso
- Signal: DOM node count > 1000 or scrolling jank appears


## 4. Domain Model

### Artwork

- Single artist
- Can belong to multiple collections
- **Has:**
  - technical metadata (e.g. medium, dimensions)
  - image(s)
  - AI-generated curator-style description

### Collection

- Curated grouping of artworks
- Non-exclusive
- Conceptual, not hierarchical

This is a domain-driven model, not an image gallery.

## 5. AI as a System Actor

AI is a tool with boundaries, not a feature gimmick.

### AI Responsibilities

Generate dynamic, interpretive descriptions for:
- artworks
- collections

- Reduce manual curation effort
- Keep language fresh without manual rewriting

Descriptions may vary between requests.

### Hard Boundaries (Non-Negotiable)

**AI must:**

- **Not invent facts**
  - no dates, provenance, intent, biography, or materials unless explicitly provided
- **Not claim authority**
  - interpretation only, no assertions
- **Not modify structure**
  - cannot create, alter, group, or reorder artworks or collections
- **Not persist output (initially)**
  - AI text is ephemeral, not canonical
- **Stay stylistically constrained**
  - controlled tone and length
  - no jargon or art-world grandstanding
- **Be attributable**
  - it must be knowable that text is AI-generated (even if only behind the curtain)

AI is a guest voice, not a curator.

## 6. Technical Stack (Current)

### Backend

- Python 3.13
- FastAPI
- Strawberry GraphQL
- Poetry for dependency and environment management

**Purpose:**
- typed API
- clear domain modelling
- demonstrable backend competence
- minimal but extensible

### Frontend

- Modern React-based stack (framework choice intentionally deferred)
- No Tailwind
- Styling via SCSS/Sass or equivalent

**Goals:**
- visual restraint
- typographic confidence
- art-first composition

## 7. Documentation as Part of the System

Documentation is a first-class artifact.

### Decision Records

Stored in `docs/decisions/`

Only for decisions that:
- meaningfully constrain future work
- affect architecture or intent

### Process Documentation

- Development process
- AI collaboration
- Iterations over time

This documentation feeds directly into the curtain layer.

## 8. AI-Assisted Development Model

AI tools are explicitly part of the workflow.

**AI acts as:**
- junior developer
- reviewer
- summariser
- decision-log generator

**Reusable AI prompts / command files may be used to:**
- review recent work
- extract decisions
- update documentation

This is intentional and demonstrable.

## 9. Explicitly Deferred Decisions

The following are intentionally unresolved and will be decided later, in context:

- How the curtain layer is triggered
- Final tone calibration for AI-generated descriptions
- Final frontend framework choice

These are not gaps; they are staged decisions.

## 10. Non-Goals

This project is not:
- a generic developer portfolio
- a tech demo disguised as art
- a startup MVP
- a CMS
- growth- or monetisation-optimised (yet)

This document is the source of truth for intent, scope, and constraints.
All future work should align with it unless a documented decision explicitly changes it.