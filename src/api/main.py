from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from .graphql.schema import schema

app = FastAPI()
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    return {"message": "Hello World"}
