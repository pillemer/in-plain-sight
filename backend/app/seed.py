"""Seed the database with initial data."""

from app.database import SessionLocal, init_db
from app.models import Artist, Artwork, Collection


def seed_database():
    """Populate database with initial gallery data."""
    # Initialize database tables
    init_db()

    db = SessionLocal()
    try:
        # Clear existing data
        db.query(Artwork).delete()
        db.query(Collection).delete()
        db.query(Artist).delete()

        # Create artist
        artist = Artist(name="Jack Pillemer")
        db.add(artist)
        db.flush()

        # Create collection
        collection = Collection(title="Selected Works", description=None)
        db.add(collection)
        db.flush()

        # Create artworks
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
        print("Database seeded successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
