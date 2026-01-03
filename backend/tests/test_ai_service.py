"""Unit tests for AI service with mocked Gemini API calls."""

from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.ai_service import AIService
from app.models import Artist, Artwork


class TestAIServiceInitialization:
    """Test AI service initialization and configuration."""

    def test_initialization_with_valid_api_key(self, monkeypatch):
        """AIService initializes successfully with valid API key."""
        monkeypatch.setenv("GEMINI_API_KEY", "test_api_key_123")

        with patch("app.ai_service.genai.Client") as mock_client:
            service = AIService()
            mock_client.assert_called_once_with(api_key="test_api_key_123")
            assert service.client is not None

    def test_initialization_fails_without_api_key(self, monkeypatch):
        """AIService raises ValueError when API key is missing."""
        monkeypatch.delenv("GEMINI_API_KEY", raising=False)

        with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable not set"):
            AIService()


class TestPromptConstruction:
    """Test prompt building logic."""

    def test_prompt_includes_artwork_metadata(self, monkeypatch):
        """Prompt includes artwork title and artist name."""
        monkeypatch.setenv("GEMINI_API_KEY", "test_key")

        with patch("app.ai_service.genai.Client"):
            service = AIService()

            # Create test artwork with artist
            artist = Artist(id=1, name="Vincent van Gogh")
            artwork = Artwork(
                id=1,
                title="Starry Night",
                image_url="https://example.com/starry.jpg",
                artist_id=1,
            )
            artwork.artist = artist

            prompt = service._build_prompt(artwork)

            # Verify prompt contains key metadata
            assert "Starry Night" in prompt
            assert "Vincent van Gogh" in prompt

    def test_prompt_enforces_hard_boundaries(self, monkeypatch):
        """Prompt includes all hard boundary constraints."""
        monkeypatch.setenv("GEMINI_API_KEY", "test_key")

        with patch("app.ai_service.genai.Client"):
            service = AIService()

            artist = Artist(id=1, name="Test Artist")
            artwork = Artwork(
                id=1,
                title="Test Artwork",
                image_url="https://example.com/test.jpg",
                artist_id=1,
            )
            artwork.artist = artist

            prompt = service._build_prompt(artwork)

            # Verify hard boundary language is present
            assert "third person" in prompt.lower()
            assert "do not invent facts" in prompt.lower()
            assert "interpretation only" in prompt.lower()
            assert "1-2 paragraphs" in prompt.lower()
            assert "based on what you see" in prompt.lower()


class TestImageFetching:
    """Test image fetching from URLs."""

    @pytest.mark.asyncio
    async def test_successful_image_fetch(self, monkeypatch):
        """Successfully fetches image from URL."""
        monkeypatch.setenv("GEMINI_API_KEY", "test_key")

        # Mock image data
        mock_image_bytes = b"fake_image_data"
        mock_response = MagicMock()
        mock_response.content = mock_image_bytes
        mock_response.headers = {"content-type": "image/jpeg"}

        # Mock httpx client
        mock_http_client = AsyncMock()
        mock_http_client.get.return_value = mock_response

        # Mock Gemini client
        mock_genai_response = MagicMock()
        mock_genai_response.text = "A beautiful interpretation of the artwork."
        mock_genai_client = MagicMock()
        mock_genai_client.aio.models.generate_content = AsyncMock(return_value=mock_genai_response)

        with patch("app.ai_service.genai.Client", return_value=mock_genai_client):
            with patch("app.ai_service.httpx.AsyncClient") as mock_async_client:
                mock_async_client.return_value.__aenter__.return_value = mock_http_client

                service = AIService()
                artist = Artist(id=1, name="Test Artist")
                artwork = Artwork(
                    id=1,
                    title="Test",
                    image_url="https://example.com/image.jpg",
                    artist_id=1,
                )
                artwork.artist = artist

                result = await service.interpret_artwork(artwork)

                # Verify image was fetched
                mock_http_client.get.assert_called_once_with(
                    "https://example.com/image.jpg", timeout=10.0
                )
                assert result == "A beautiful interpretation of the artwork."

    @pytest.mark.asyncio
    async def test_image_fetch_failure_raises_exception(self, monkeypatch):
        """Raises exception when image fetch fails."""
        monkeypatch.setenv("GEMINI_API_KEY", "test_key")

        # Mock httpx client that raises HTTPError
        mock_http_client = AsyncMock()
        mock_http_client.get.side_effect = httpx.HTTPError("Network error")

        with patch("app.ai_service.genai.Client"):
            with patch("app.ai_service.httpx.AsyncClient") as mock_async_client:
                mock_async_client.return_value.__aenter__.return_value = mock_http_client

                service = AIService()
                artist = Artist(id=1, name="Test Artist")
                artwork = Artwork(
                    id=1,
                    title="Test",
                    image_url="https://invalid.com/image.jpg",
                    artist_id=1,
                )
                artwork.artist = artist

                with pytest.raises(Exception, match="Failed to fetch artwork image from"):
                    await service.interpret_artwork(artwork)

    @pytest.mark.asyncio
    async def test_mime_type_detection(self, monkeypatch):
        """Detects MIME type from Content-Type header."""
        monkeypatch.setenv("GEMINI_API_KEY", "test_key")

        mock_image_bytes = b"fake_png_data"
        mock_response = MagicMock()
        mock_response.content = mock_image_bytes
        mock_response.headers = {"content-type": "image/png"}

        mock_http_client = AsyncMock()
        mock_http_client.get.return_value = mock_response

        mock_genai_response = MagicMock()
        mock_genai_response.text = "Interpretation"
        mock_genai_client = MagicMock()
        mock_genai_client.aio.models.generate_content = AsyncMock(return_value=mock_genai_response)

        with patch("app.ai_service.genai.Client", return_value=mock_genai_client):
            with patch("app.ai_service.httpx.AsyncClient") as mock_async_client:
                mock_async_client.return_value.__aenter__.return_value = mock_http_client
                with patch("app.ai_service.types.Part.from_bytes") as mock_from_bytes:
                    mock_from_bytes.return_value = MagicMock()

                    service = AIService()
                    artist = Artist(id=1, name="Test Artist")
                    artwork = Artwork(
                        id=1,
                        title="Test",
                        image_url="https://example.com/image.png",
                        artist_id=1,
                    )
                    artwork.artist = artist

                    await service.interpret_artwork(artwork)

                    # Verify Part.from_bytes was called with correct MIME type
                    mock_from_bytes.assert_called_once()
                    call_kwargs = mock_from_bytes.call_args[1]
                    assert call_kwargs["mime_type"] == "image/png"


class TestGeminiAPIIntegration:
    """Test Gemini API call integration."""

    @pytest.mark.asyncio
    async def test_successful_api_call(self, monkeypatch):
        """Successfully generates interpretation via Gemini API."""
        monkeypatch.setenv("GEMINI_API_KEY", "test_key")

        # Mock HTTP image fetch
        mock_image_response = MagicMock()
        mock_image_response.content = b"fake_image"
        mock_image_response.headers = {"content-type": "image/jpeg"}
        mock_http_client = AsyncMock()
        mock_http_client.get.return_value = mock_image_response

        # Mock Gemini response
        mock_genai_response = MagicMock()
        mock_genai_response.text = "The artwork features bold brushstrokes."
        mock_genai_client = MagicMock()
        mock_genai_client.aio.models.generate_content = AsyncMock(return_value=mock_genai_response)

        with patch("app.ai_service.genai.Client", return_value=mock_genai_client):
            with patch("app.ai_service.httpx.AsyncClient") as mock_async_client:
                mock_async_client.return_value.__aenter__.return_value = mock_http_client

                service = AIService()
                artist = Artist(id=1, name="Test Artist")
                artwork = Artwork(
                    id=1,
                    title="Test",
                    image_url="https://example.com/image.jpg",
                    artist_id=1,
                )
                artwork.artist = artist

                result = await service.interpret_artwork(artwork)

                assert result == "The artwork features bold brushstrokes."
                mock_genai_client.aio.models.generate_content.assert_called_once()

    @pytest.mark.asyncio
    async def test_empty_response_raises_exception(self, monkeypatch):
        """Raises exception when AI returns empty response."""
        monkeypatch.setenv("GEMINI_API_KEY", "test_key")

        mock_image_response = MagicMock()
        mock_image_response.content = b"fake_image"
        mock_image_response.headers = {"content-type": "image/jpeg"}
        mock_http_client = AsyncMock()
        mock_http_client.get.return_value = mock_image_response

        # Mock empty Gemini response
        mock_genai_response = MagicMock()
        mock_genai_response.text = ""
        mock_genai_client = MagicMock()
        mock_genai_client.aio.models.generate_content = AsyncMock(return_value=mock_genai_response)

        with patch("app.ai_service.genai.Client", return_value=mock_genai_client):
            with patch("app.ai_service.httpx.AsyncClient") as mock_async_client:
                mock_async_client.return_value.__aenter__.return_value = mock_http_client

                service = AIService()
                artist = Artist(id=1, name="Test Artist")
                artwork = Artwork(
                    id=1,
                    title="Test",
                    image_url="https://example.com/image.jpg",
                    artist_id=1,
                )
                artwork.artist = artist

                with pytest.raises(Exception, match="AI service returned empty response"):
                    await service.interpret_artwork(artwork)
