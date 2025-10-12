from fastapi import Depends, FastAPI
from strawberry.fastapi import GraphQLRouter

from src.database import get_async_session

from .graphql.schema import schema

app = FastAPI()


async def get_context(session=Depends(get_async_session)):
    return {"session": session}


graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")
