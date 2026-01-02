from typing import AsyncIterator

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.ai_service import AIService
from app.database import SessionLocal
from app.schema import schema

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


async def get_context() -> AsyncIterator[dict]:
    """Provide database session and AI service in GraphQL context."""
    db = SessionLocal()
    ai_service = AIService()
    try:
        yield {"db": db, "ai_service": ai_service}
    finally:
        db.close()


graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")
