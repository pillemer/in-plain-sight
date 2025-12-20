import strawberry
from typing import List


@strawberry.type
class Image:
    id: str
    title: str
    image_url: str


@strawberry.type
class Query:
    @strawberry.field
    def gallery(self) -> List[Image]:
        return [
            Image(
                id="1",
                title="Untitled Study I",
                image_url="https://example.com/image-1.jpg",
            ),
            Image(
                id="2",
                title="Untitled Study II",
                image_url="https://example.com/image-2.jpg",
            ),
        ]


schema = strawberry.Schema(query=Query)
