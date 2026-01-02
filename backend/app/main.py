from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.database import SessionLocal
from app.schema import schema

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


async def get_context() -> dict:
    """Provide database session in GraphQL context."""
    db = SessionLocal()
    try:
        yield {"db": db}
    finally:
        db.close()


graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")
