"""AI Service for generating artwork interpretations using Google Gemini API.

This service encapsulates all AI interaction logic, providing curator-style
interpretations of artworks with strict boundaries on what the AI can say.
"""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.models import Artwork

# Load environment variables
load_dotenv()


class AIService:
    """Service for generating AI interpretations of artworks using Google Gemini.

    The AI acts as a curator providing observational notes about artworks,
    focusing on visual elements (color, composition, mood, texture) without
    inventing facts or claiming authority.

    Attributes:
        client: Initialized Google Gemini API client
    """

    def __init__(self):
        """Initialize the AI service with Gemini API client.

        Raises:
            ValueError: If GEMINI_API_KEY environment variable is not set
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable not set. "
                "Please add your API key to the .env file."
            )
        self.client = genai.Client(api_key=api_key)

    async def interpret_artwork(self, artwork: Artwork) -> str:
        """Generate an AI interpretation for an artwork.

        Creates a curator's note focusing on observable visual elements:
        colors, composition, mood, and texture. The interpretation is
        third-person, poetic but not overwrought, and strictly avoids
        inventing facts about the artwork.

        Args:
            artwork: The Artwork model instance to interpret

        Returns:
            A string containing the AI-generated interpretation (1-2 paragraphs)

        Raises:
            Exception: If the API call fails (network error, rate limit, etc.)
        """
        prompt = self._build_prompt(artwork)

        try:
            response = await self.client.aio.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,  # Creative but not random
                    max_output_tokens=200,  # Keep responses concise (1-2 paragraphs)
                ),
            )

            # Ensure we have text content in the response
            if not response.text:
                raise Exception("AI service returned empty response")

            return response.text

        except Exception as e:
            # Re-raise with more context for debugging
            raise Exception(f"Failed to generate AI interpretation: {str(e)}") from e

    def _build_prompt(self, artwork: Artwork) -> str:
        """Construct the prompt for the AI interpretation.

        The prompt includes:
        - Role setting (curator writing a gallery note)
        - Artwork metadata (title, artist)
        - Focus areas (color, composition, mood, texture)
        - Hard boundaries (no invented facts, interpretation only)
        - Tone guidance (third person, poetic but restrained)

        Args:
            artwork: The Artwork model instance with metadata

        Returns:
            Formatted prompt string for the AI
        """
        # Note: This is the initial prompt design. It will likely be refined
        # based on user feedback during Step 4 (Manual Testing & Calibration).
        #
        # Prompt engineering considerations:
        # - Third person is enforced to avoid conversational tone
        # - "Observed, not factual" guides AI away from claiming material knowledge
        # - "Poetic language sparingly" prevents overwrought prose
        # - Explicit length constraint (1-2 paragraphs)

        return f"""You are writing a curator's note for an art gallery visitor.
Write a brief, observational interpretation of this artwork.

Artwork: "{artwork.title}" by {artwork.artist.name}

Focus on:
- Colors and palette
- Composition and structure
- Mood and emotional tone
- Texture and technique (observed, not factual)

Constraints:
- Write in third person
- 1-2 paragraphs maximum
- Do not invent facts (dates, materials, provenance, artist intent)
- Offer interpretation only, not assertions
- Use poetic language sparingly - avoid overwrought or gushy prose
- Avoid art world jargon unless essential

Write the curator's note:"""
