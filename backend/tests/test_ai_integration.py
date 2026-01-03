"""Integration tests for AI interpretation GraphQL query."""

import os
from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

# Set test database URL before importing app modules
os.environ["DATABASE_URL"] = "sqlite:///./test_gallery.db"

from app.database import SessionLocal, init_db
from app.main import app
from app.models import Artist, Artwork, Collection


@pytest.fixture(autouse=True)
def setup_database():
    """Setup test database before each test."""
    init_db()

    db = SessionLocal()
    try:
        # Clear existing data
        db.query(Artwork).delete()
        db.query(Collection).delete()
        db.query(Artist).delete()

        # Create test artist
        artist = Artist(name="Test Artist")
        db.add(artist)
        db.flush()

        # Create test collection
        collection = Collection(title="Test Collection", description=None)
        db.add(collection)
        db.flush()

        # Create test artworks
        artwork1 = Artwork(
            title="Test Artwork 1",
            image_url="https://images.metmuseum.org/CRDImages/ep/original/DT1502_cropped2.jpg",
            artist_id=artist.id,
            collection_id=collection.id,
        )
        artwork2 = Artwork(
            title="Test Artwork 2",
            image_url="https://images.metmuseum.org/CRDImages/as/original/DP130155.jpg",
            artist_id=artist.id,
            collection_id=collection.id,
        )

        db.add(artwork1)
        db.add(artwork2)
        db.commit()

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


class TestAIInterpretationQuery:
    """Test GraphQL generateArtworkInterpretation query."""

    def test_successful_interpretation_generation(self):
        """Successfully generates interpretation for valid artwork."""
        # Mock AI service at the main.py level where it's initialized
        mock_interpretation = "The artwork displays vibrant colors and dynamic composition."
        mock_ai_service = AsyncMock()
        mock_ai_service.interpret_artwork.return_value = mock_interpretation

        with patch("app.main.AIService", return_value=mock_ai_service):
            # Create new client to get fresh context with mocked AI service
            test_client = TestClient(app)

            query = """
                query {
                    generateArtworkInterpretation(artworkId: "1") {
                        id
                        content
                        generatedAt
                        context
                    }
                }
            """

            response = test_client.post("/graphql", json={"query": query})

            assert response.status_code == 200
            data = response.json()

            assert "data" in data
            assert "generateArtworkInterpretation" in data["data"]
            interpretation = data["data"]["generateArtworkInterpretation"]

            # Verify interpretation structure
            assert interpretation is not None
            assert interpretation["content"] == mock_interpretation
            assert interpretation["context"] == "artwork:1"
            assert "id" in interpretation
            assert "generatedAt" in interpretation

    def test_returns_none_for_invalid_artwork_id(self):
        """Returns None when artwork ID doesn't exist."""
        mock_ai_service = AsyncMock()

        with patch("app.main.AIService", return_value=mock_ai_service):
            test_client = TestClient(app)

            query = """
                query {
                    generateArtworkInterpretation(artworkId: "9999") {
                        id
                        content
                    }
                }
            """

            response = test_client.post("/graphql", json={"query": query})

            assert response.status_code == 200
            data = response.json()

            assert data["data"]["generateArtworkInterpretation"] is None

    def test_handles_ai_service_failure_gracefully(self):
        """Handles AI service errors gracefully by returning None."""
        mock_ai_service = AsyncMock()
        mock_ai_service.interpret_artwork.side_effect = Exception("API Error")

        with patch("app.main.AIService", return_value=mock_ai_service):
            test_client = TestClient(app)

            query = """
                query {
                    generateArtworkInterpretation(artworkId: "1") {
                        id
                        content
                    }
                }
            """

            response = test_client.post("/graphql", json={"query": query})

            # Should handle error gracefully and return None
            assert response.status_code == 200
            data = response.json()

            # Resolver catches exception and returns None
            assert data["data"]["generateArtworkInterpretation"] is None

    def test_interpretation_includes_artwork_context(self):
        """Interpretation context field references correct artwork ID."""
        mock_interpretation = "Test interpretation content."
        mock_ai_service = AsyncMock()
        mock_ai_service.interpret_artwork.return_value = mock_interpretation

        with patch("app.main.AIService", return_value=mock_ai_service):
            test_client = TestClient(app)

            query = """
                query {
                    generateArtworkInterpretation(artworkId: "2") {
                        context
                    }
                }
            """

            response = test_client.post("/graphql", json={"query": query})

            assert response.status_code == 200
            data = response.json()

            interpretation = data["data"]["generateArtworkInterpretation"]
            assert interpretation["context"] == "artwork:2"

    def test_ephemeral_id_generation(self):
        """Generated interpretation has unique ephemeral ID."""
        mock_interpretation = "Test content."
        mock_ai_service = AsyncMock()
        mock_ai_service.interpret_artwork.return_value = mock_interpretation

        with patch("app.main.AIService", return_value=mock_ai_service):
            test_client = TestClient(app)

            query = """
                query {
                    generateArtworkInterpretation(artworkId: "1") {
                        id
                    }
                }
            """

            response = test_client.post("/graphql", json={"query": query})

            assert response.status_code == 200
            data = response.json()

            interpretation_id = data["data"]["generateArtworkInterpretation"]["id"]
            # Ephemeral ID should contain artwork ID and timestamp
            assert "ephemeral-1-" in interpretation_id

    def test_generated_at_timestamp_is_recent(self):
        """generated_at timestamp is current (within last few seconds)."""
        mock_interpretation = "Test content."
        mock_ai_service = AsyncMock()
        mock_ai_service.interpret_artwork.return_value = mock_interpretation

        with patch("app.main.AIService", return_value=mock_ai_service):
            test_client = TestClient(app)

            query = """
                query {
                    generateArtworkInterpretation(artworkId: "1") {
                        generatedAt
                    }
                }
            """

            before = datetime.now(timezone.utc)
            response = test_client.post("/graphql", json={"query": query})

            assert response.status_code == 200
            data = response.json()

            generated_at_str = data["data"]["generateArtworkInterpretation"]["generatedAt"]
            # Parse ISO format datetime (with +00:00 timezone)
            generated_at = datetime.fromisoformat(generated_at_str.replace("Z", "+00:00"))

            # Timestamp should be very recent (within 5 seconds of request)
            time_diff = (generated_at - before).total_seconds()
            assert 0 <= time_diff <= 5
