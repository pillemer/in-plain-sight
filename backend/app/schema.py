from datetime import datetime
from typing import List

import strawberry


@strawberry.type
class Artist:
    id: str
    name: str


@strawberry.type
class Artwork:
    id: str
    title: str
    image_url: str
    artist: Artist


@strawberry.type
class Collection:
    id: str
    title: str
    description: str | None
    artworks: List[Artwork]


@strawberry.type
class AIInterpretation:
    id: str
    content: str
    generated_at: datetime
    context: str


# Hardcoded artist data
ARTIST_DATA = Artist(id="artist-1", name="Jack Pillemer")


# Helper function to get all collections data
def get_all_collections() -> List[Collection]:
    artworks = [
        Artwork(
            id="1",
            title="Untitled Study I",
            image_url="https://example.com/image-1.jpg",
            artist=ARTIST_DATA,
        ),
        Artwork(
            id="2",
            title="Untitled Study II",
            image_url="https://example.com/image-2.jpg",
            artist=ARTIST_DATA,
        ),
    ]

    return [
        Collection(
            id="c1",
            title="Selected Works",
            description=None,
            artworks=artworks,
        )
    ]


@strawberry.type
class Query:
    @strawberry.field
    def artist(self) -> Artist:
        """Returns the gallery artist."""
        return ARTIST_DATA

    @strawberry.field
    def collections(self) -> List[Collection]:
        return get_all_collections()

    @strawberry.field
    def collection(self, id: str) -> Collection | None:
        """Get single collection by ID."""
        collections = get_all_collections()
        return next((c for c in collections if c.id == id), None)

    @strawberry.field
    def artwork(self, id: str) -> Artwork | None:
        """Get single artwork by ID."""
        collections = get_all_collections()
        for collection in collections:
            artwork = next((a for a in collection.artworks if a.id == id), None)
            if artwork:
                return artwork
        return None


schema = strawberry.Schema(query=Query)
