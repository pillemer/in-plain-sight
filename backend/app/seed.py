"""Seed the database with artwork from Cloudinary."""

import os

import cloudinary
import cloudinary.api
from dotenv import load_dotenv

from app.database import SessionLocal, init_db
from app.models import Artist, Artwork, Collection

# Load environment variables
load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

# Cloudinary base URL for constructing image URLs
CLOUDINARY_BASE_URL = f"https://res.cloudinary.com/{os.getenv('CLOUDINARY_CLOUD_NAME')}/image/upload"


def fetch_cloudinary_images(max_results: int = 20) -> list[dict]:
    """Fetch image public_ids from Cloudinary."""
    try:
        # Fetch resources from Cloudinary
        result = cloudinary.api.resources(
            type="upload",
            resource_type="image",
            max_results=max_results,
        )
        return result.get("resources", [])
    except Exception as e:
        print(f"Error fetching from Cloudinary: {e}")
        return []


def seed_database(max_artworks: int = 20):
    """Populate database with artwork from Cloudinary."""
    # Initialize database tables
    init_db()

    # Fetch images from Cloudinary
    print("Fetching images from Cloudinary...")
    images = fetch_cloudinary_images(max_results=max_artworks)

    if not images:
        print("No images found in Cloudinary. Please upload some images first.")
        return

    print(f"Found {len(images)} images in Cloudinary")

    db = SessionLocal()
    try:
        # Clear existing data
        db.query(Artwork).delete()
        db.query(Collection).delete()
        db.query(Artist).delete()

        # Create artist
        artist = Artist(name="Jack Pillemer", bio="""I live in Jerusalem. I paint in Jerusalem - mostly. I enjoy the air, the color and shapes in and around Jerusalem. There must be shade, quiet and something of interest - and that's it. Most times I would be with Ben Marom - friend, colleague and often mentor. It would likely be a Friday. Find a spot, set up the easel or the folding table and begin.
I started studying with Tzahi Gil who taught me the basics. Eli Shamir gave me some direction on watercolor and Naomi at the Israel Museum insisted I look and paint what I see. Marek Yanai took me back to basics with such intensity and skill and Yael Morag helped me celebrate with watercolor. Ben and I discuss the spots, the contrasts and the geometrical shapes.""")
        db.add(artist)
        db.flush()

        # Create collection
        collection = Collection(title="Watercolours", description=None)
        db.add(collection)
        db.flush()

        # Create artworks from Cloudinary images
        for image in images:
            public_id = image["public_id"]
            # Construct the URL (format is automatically detected)
            image_url = f"{CLOUDINARY_BASE_URL}/{public_id}"

            artwork = Artwork(
                title="",  # No metadata yet
                image_url=image_url,
                artist_id=artist.id,
                collection_id=collection.id,
            )
            db.add(artwork)

        db.commit()
        print(f"Database seeded successfully with {len(images)} artworks!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
