from app import config
from typing import AsyncGenerator
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.ext.declarative import declarative_base

from app.models import User, OAuthAccount

engine = create_async_engine(config.settings.db_connection_async)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
# class Base(DeclarativeBase):
#     __allow_unmapped__ = True


# class User(SQLAlchemyBaseUserTableUUID, Base):
#     pass


# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User, OAuthAccount)
