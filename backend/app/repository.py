from sqlalchemy.orm import Session

from app import models


class ArtistRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_artist(self) -> models.Artist | None:
        """Get the single artist. Returns first artist found."""
        return self.db.query(models.Artist).first()


class CollectionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[models.Collection]:
        """Get all collections."""
        return list(self.db.query(models.Collection).all())

    def get_by_id(self, collection_id: int) -> models.Collection | None:
        """Get a collection by ID."""
        return self.db.query(models.Collection).filter_by(id=collection_id).first()


class ArtworkRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, artwork_id: int) -> models.Artwork | None:
        """Get an artwork by ID."""
        return self.db.query(models.Artwork).filter_by(id=artwork_id).first()
