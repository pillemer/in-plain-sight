from datetime import datetime
from typing import List

import strawberry

from app import models
from app.repository import ArtistRepository, ArtworkRepository, CollectionRepository


@strawberry.type
class Artist:
    id: str
    name: str

    @classmethod
    def from_model(cls, model: models.Artist) -> "Artist":
        return cls(id=str(model.id), name=model.name)


@strawberry.type
class Artwork:
    id: str
    title: str
    image_url: str
    artist: Artist

    @classmethod
    def from_model(cls, model: models.Artwork) -> "Artwork":
        return cls(
            id=str(model.id),
            title=model.title,
            image_url=model.image_url,
            artist=Artist.from_model(model.artist),
        )


@strawberry.type
class Collection:
    id: str
    title: str
    description: str | None
    artworks: List[Artwork]

    @classmethod
    def from_model(cls, model: models.Collection) -> "Collection":
        return cls(
            id=str(model.id),
            title=model.title,
            description=model.description,
            artworks=[Artwork.from_model(a) for a in model.artworks],
        )


@strawberry.type
class AIInterpretation:
    id: str
    content: str
    generated_at: datetime
    context: str


@strawberry.type
class Query:
    @strawberry.field
    def artist(self, info: strawberry.Info) -> Artist | None:
        """Returns the gallery artist."""
        db = info.context["db"]
        repo = ArtistRepository(db)
        artist_model = repo.get_artist()
        return Artist.from_model(artist_model) if artist_model else None

    @strawberry.field
    def collections(self, info: strawberry.Info) -> List[Collection]:
        db = info.context["db"]
        repo = CollectionRepository(db)
        collection_models = repo.get_all()
        return [Collection.from_model(c) for c in collection_models]

    @strawberry.field
    def collection(self, id: str, info: strawberry.Info) -> Collection | None:
        """Get single collection by ID."""
        db = info.context["db"]
        repo = CollectionRepository(db)
        try:
            collection_id = int(id)
        except ValueError:
            return None
        collection_model = repo.get_by_id(collection_id)
        return Collection.from_model(collection_model) if collection_model else None

    @strawberry.field
    def artwork(self, id: str, info: strawberry.Info) -> Artwork | None:
        """Get single artwork by ID."""
        db = info.context["db"]
        repo = ArtworkRepository(db)
        try:
            artwork_id = int(id)
        except ValueError:
            return None
        artwork_model = repo.get_by_id(artwork_id)
        return Artwork.from_model(artwork_model) if artwork_model else None


schema = strawberry.Schema(query=Query)
