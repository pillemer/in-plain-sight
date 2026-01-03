# Decision 0009: Google Gemini API for AI generation

## Context
Phase 3 requires an AI API to generate artwork interpretations. The AI must:
- Generate 1-2 paragraph curator-style notes
- Focus on colors, composition, mood, texture
- Respect hard boundaries (no invented facts, third-person only)
- Work within £0 budget (free tier only)

## Decision
Use **Google Gemini API** with the **`gemini-2.0-flash-lite`** model.

### Implementation
- Python SDK: `google-genai ^0.4.0`
- Model: `gemini-2.0-flash-lite` (free tier after billing setup)
- Configuration: `temperature=0.7`, `max_output_tokens=200`
- API key via environment variable: `GEMINI_API_KEY`

## Alternatives considered

### 1. Claude API (Anthropic)
**Pros:**
- Excellent at following complex instructions
- Strong at nuanced creative writing
- Project uses Claude for development assistance (familiarity)

**Cons:**
- **No free tier** - Starts at paid tier (~$3 input / $15 output per million tokens)
- ~$0.007 per interpretation = $7 per 1000 interpretations
- Requires credit card, no £0 option

**Verdict:** Rejected due to cost constraint

### 2. OpenAI GPT-4 or GPT-3.5
**Pros:**
- Strong creative writing capabilities
- Well-documented API

**Cons:**
- **No free tier** for GPT-4
- GPT-3.5 free tier severely limited
- More expensive than Gemini at scale

**Verdict:** Rejected due to cost and quota limits

### 3. Local LLM (Llama, Mistral via Ollama)
**Pros:**
- Truly free (no API costs)
- Unlimited requests
- Full control over model

**Cons:**
- Requires local GPU or slow CPU inference
- Deployment complexity (can't run on basic hosting)
- Quality inconsistent for creative tasks
- Over-engineered for MVP

**Verdict:** Rejected - too complex for MVP, revisit if scaling issues arise

## Consequences

### Positive
- **Free tier available** - 1000 requests/day on `gemini-2.0-flash-lite` (as of Jan 2026)
- **Sufficient quota for MVP** - 30-50 interpretations/day during development
- **Good quality** - Initial tests show appropriate tone and adherence to constraints
- **Simple integration** - Official Python SDK, straightforward async API
- **Future flexibility** - Service layer abstraction allows swapping to Claude/GPT later

### Negative
- **Billing setup required** - Even for free tier (credit card needed)
- **Quota limits exist** - 1000/day limit could be hit during heavy testing
- **Free tier uncertainty** - Google has reduced free quotas in past (Dec 2025)
- **Geographic restrictions** - Free tier cannot serve EU/EEA/UK/Switzerland users

### Mitigations
- Service layer (`AIService`) decouples API choice from GraphQL resolvers
- Can swap to different provider by changing only `ai_service.py`
- Quota monitoring available at https://ai.dev/usage
- Prompt caching can be added to reduce token usage if needed

## Model selection rationale
Chose `gemini-2.0-flash-lite` specifically because:
- **Free tier availability** - Confirmed quota after billing setup
- **Speed** - Fastest Gemini 2.0 variant (low latency for UX)
- **Cost efficiency** - Most cost-efficient model in Gemini family
- **Quality sufficient** - Outperforms Gemini 1.5 Flash on benchmarks
- **Large context** - 1M token context window (overkill for our use, but future-proof)

Note: Initial attempts used `gemini-2.0-flash-lite` but hit quota=0 errors until billing information was added to Google AI account, even for free tier access.

## Related decisions
- **0008: Ephemeral AI interpretations** - MVP persistence strategy
- **Future decision needed:** If/when to migrate to paid tier or alternative provider
