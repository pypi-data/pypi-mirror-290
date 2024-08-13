from contextlib import asynccontextmanager
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    List,
    Optional,
    Type,
)

import beanie
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClientSession
from pydantic import BaseModel

from keystone_database import db_settings


class ConnectionOptions(BaseModel):
    document_models: List[Type[beanie.Document]]
    recreate_views: Optional[bool] = None
    allow_index_dropping: Optional[bool] = None


async def init_connection(
        options: ConnectionOptions,
):
    settings = db_settings.get_settings()

    await beanie.init_beanie(
            database=settings.get_db(), document_models=options.document_models, recreate_views=options.recreate_views,
            allow_index_dropping=options.allow_index_dropping,
    )
    logger.success("database initialized")


@asynccontextmanager
async def get_transaction() -> AsyncIOMotorClientSession:
    settings = db_settings.get_settings()
    async with await settings.get_client().start_session() as session:
        async with session.start_transaction(max_commit_time_ms=1000 * 60 * 60):
            try:
                logger.info(session.session_id)
                yield session
            finally:
                logger.info("session ended")


# TODO: figure out why fastapi Depends pattern doesn't allow for a context manager
def get_transaction_dep() -> Callable[[], AsyncGenerator[AsyncIOMotorClientSession, Any]]:
    settings = db_settings.get_settings()

    async def func():
        async with await settings.get_client().start_session() as session:
            async with session.start_transaction():
                try:
                    logger.info(session.session_id)
                    yield session
                    await session.commit_transaction()
                except Exception as e:
                    await session.abort_transaction()
                    raise e
                finally:
                    logger.info("session ended")

    return func
