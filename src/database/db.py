import contextlib
import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from src.config.config import config

logging.basicConfig(level=logging.INFO, format="%(levelname)s     %(module)s - %(message)s")


class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autoflush=False, autocommit=False, bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Session is not initialized")

        async with self._session_maker() as session:
            try:
                yield session
            except Exception as err:
                await session.rollback()
                logging.error(f"Database error: {err}")
                raise HTTPException(status_code=500, detail="Database error occurred")
            finally:
                await session.close()


sessionmanager = DatabaseSessionManager(config.DB_URL)


async def get_db():
    async with sessionmanager.session() as session:
        yield session
