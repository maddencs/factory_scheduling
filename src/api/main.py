from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter

from src.database import AsyncSession, get_async_session
from .graphql.schema import schema

app = FastAPI()


async def get_context():
    async with get_async_session() as session:
        yield {"session": session}


graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    return {"message": "Hello World"}
