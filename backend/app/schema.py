from typing import List

import strawberry


@strawberry.type
class Artwork:
    id: str
    title: str
    image_url: str


@strawberry.type
class Collection:
    id: str
    title: str
    artworks: List[Artwork]


@strawberry.type
class Query:
    @strawberry.field
    def collections(self) -> List[Collection]:
        artworks = [
            Artwork(
                id="1",
                title="Untitled Study I",
                image_url="https://example.com/image-1.jpg",
            ),
            Artwork(
                id="2",
                title="Untitled Study II",
                image_url="https://example.com/image-2.jpg",
            ),
        ]

        return [
            Collection(
                id="c1",
                title="Selected Works",
                artworks=artworks,
            )
        ]


schema = strawberry.Schema(query=Query)
