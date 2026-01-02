import os

import pytest
from fastapi.testclient import TestClient

# Set test database URL before importing app modules
os.environ["DATABASE_URL"] = "sqlite:///./test_gallery.db"

from app.database import SessionLocal, init_db
from app.main import app
from app.models import Artist, Artwork, Collection

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Setup test database before each test."""
    # Initialize tables
    init_db()

    db = SessionLocal()
    try:
        # Clear existing data
        db.query(Artwork).delete()
        db.query(Collection).delete()
        db.query(Artist).delete()

        # Create test artist
        artist = Artist(name="Jack Pillemer")
        db.add(artist)
        db.flush()

        # Create test collection
        collection = Collection(title="Selected Works", description=None)
        db.add(collection)
        db.flush()

        # Create test artworks
        artwork1 = Artwork(
            title="Untitled Study I",
            image_url="https://example.com/image-1.jpg",
            artist_id=artist.id,
            collection_id=collection.id,
        )
        artwork2 = Artwork(
            title="Untitled Study II",
            image_url="https://example.com/image-2.jpg",
            artist_id=artist.id,
            collection_id=collection.id,
        )

        db.add(artwork1)
        db.add(artwork2)

        db.commit()
    finally:
        db.close()

    yield

    # Cleanup after test
    db = SessionLocal()
    try:
        db.query(Artwork).delete()
        db.query(Collection).delete()
        db.query(Artist).delete()
        db.commit()
    finally:
        db.close()


def test_collections_query_structure():
    """Test that collections query returns properly structured data."""
    query = """
        query {
            collections {
                id
                title
                description
                artworks {
                    id
                    title
                    imageUrl
                    artist {
                        id
                        name
                    }
                }
            }
        }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "data" in data
    assert "collections" in data["data"]
    assert isinstance(data["data"]["collections"], list)

    # Verify at least one collection exists
    assert len(data["data"]["collections"]) > 0

    # Verify first collection has required fields
    collection = data["data"]["collections"][0]
    assert "id" in collection
    assert "title" in collection
    assert "description" in collection  # Can be null
    assert "artworks" in collection
    assert isinstance(collection["artworks"], list)

    # Verify artworks have required fields
    if len(collection["artworks"]) > 0:
        artwork = collection["artworks"][0]
        assert "id" in artwork
        assert "title" in artwork
        assert "imageUrl" in artwork
        assert "artist" in artwork
        assert "id" in artwork["artist"]
        assert "name" in artwork["artist"]


def test_artist_query_returns_artist():
    """Test that artist query returns an artist object."""
    query = """
        query {
            artist {
                id
                name
            }
        }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = response.json()

    assert "data" in data
    assert "artist" in data["data"]
    assert data["data"]["artist"] is not None
    assert "id" in data["data"]["artist"]
    assert "name" in data["data"]["artist"]
    assert isinstance(data["data"]["artist"]["name"], str)
    assert len(data["data"]["artist"]["name"]) > 0


def test_collection_by_id_with_valid_id():
    """Test fetching single collection by ID using an ID from collections query."""
    # First get a valid collection ID
    collections_query = """
        query {
            collections {
                id
            }
        }
    """
    response = client.post("/graphql", json={"query": collections_query})
    assert response.status_code == 200
    collections = response.json()["data"]["collections"]
    assert len(collections) > 0
    valid_id = collections[0]["id"]

    # Now query for that specific collection
    single_query = """
        query GetCollection($id: String!) {
            collection(id: $id) {
                id
                title
            }
        }
    """
    response = client.post("/graphql", json={"query": single_query, "variables": {"id": valid_id}})
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["collection"] is not None
    assert data["data"]["collection"]["id"] == valid_id


def test_collection_by_id_with_invalid_id():
    """Test fetching non-existent collection returns None."""
    query = """
        query GetCollection($id: String!) {
            collection(id: $id) {
                id
                title
            }
        }
    """
    response = client.post(
        "/graphql",
        json={"query": query, "variables": {"id": "this-id-definitely-does-not-exist"}},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["collection"] is None


def test_artwork_by_id_with_valid_id():
    """Test fetching single artwork by ID using an ID from collections query."""
    # First get a valid artwork ID
    collections_query = """
        query {
            collections {
                artworks {
                    id
                }
            }
        }
    """
    response = client.post("/graphql", json={"query": collections_query})
    assert response.status_code == 200
    collections = response.json()["data"]["collections"]
    assert len(collections) > 0
    assert len(collections[0]["artworks"]) > 0
    valid_id = collections[0]["artworks"][0]["id"]

    # Now query for that specific artwork
    single_query = """
        query GetArtwork($id: String!) {
            artwork(id: $id) {
                id
                title
                artist {
                    name
                }
            }
        }
    """
    response = client.post(
        "/graphql",
        json={"query": single_query, "variables": {"id": valid_id}},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["artwork"] is not None
    assert data["data"]["artwork"]["id"] == valid_id


def test_artwork_by_id_with_invalid_id():
    """Test fetching non-existent artwork returns None."""
    query = """
        query GetArtwork($id: String!) {
            artwork(id: $id) {
                id
                title
            }
        }
    """
    response = client.post(
        "/graphql",
        json={"query": query, "variables": {"id": "this-id-definitely-does-not-exist"}},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["artwork"] is None


def test_schema_has_all_required_types():
    """Test that schema includes all expected types via introspection."""
    introspection_query = """
        query {
            __schema {
                types {
                    name
                }
            }
        }
    """
    response = client.post("/graphql", json={"query": introspection_query})
    assert response.status_code == 200
    data = response.json()
    type_names = [t["name"] for t in data["data"]["__schema"]["types"]]

    # Verify all our custom types are in the schema
    required_types = ["Artist", "Artwork", "Collection"]
    for required_type in required_types:
        assert required_type in type_names, f"Type {required_type} not found in schema"
