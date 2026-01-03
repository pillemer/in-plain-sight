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

        # Create artworks with verified public domain images from Met Museum
        # These are real, working image URLs from the Met's Open Access collection
        # All images verified as isPublicDomain:true via Met API
        artwork1 = Artwork(
            title="Self-Portrait with a Straw Hat",
            image_url="https://images.metmuseum.org/CRDImages/ep/original/DT1502_cropped2.jpg",
            artist_id=artist.id,
            collection_id=collection.id,
        )
        artwork2 = Artwork(
            title="Under the Wave off Kanagawa (The Great Wave)",
            image_url="https://images.metmuseum.org/CRDImages/as/original/DP130155.jpg",
            artist_id=artist.id,
            collection_id=collection.id,
        )
        artwork3 = Artwork(
            title="Irises",
            image_url="https://images.metmuseum.org/CRDImages/ep/original/DP346474.jpg",
            artist_id=artist.id,
            collection_id=collection.id,
        )
        artwork4 = Artwork(
            title="The Dance Class",
            image_url="https://images.metmuseum.org/CRDImages/ep/original/DP-20101-001.jpg",
            artist_id=artist.id,
            collection_id=collection.id,
        )
        artwork5 = Artwork(
            title="Erasmus of Rotterdam",
            image_url="https://images.metmuseum.org/CRDImages/rl/original/DP164857.jpg",
            artist_id=artist.id,
            collection_id=collection.id,
        )

        db.add(artwork1)
        db.add(artwork2)
        db.add(artwork3)
        db.add(artwork4)
        db.add(artwork5)

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
