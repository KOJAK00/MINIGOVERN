from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config import Config
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.pool import NullPool
engine =create_async_engine(
        url = Config.DATABASE_URL, 
        poolclass=NullPool,
    )
async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False,
)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session()-> AsyncSession:
     async_session =sessionmaker(
         bind=engine,
         class_= AsyncSession,
         expire_on_commit=False
     )
     async with async_session() as session:
         yield session