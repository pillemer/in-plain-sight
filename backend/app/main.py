from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.schema import schema

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
