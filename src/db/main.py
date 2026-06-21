from sqlmodel import  create_engine ,text , SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.books.config import settings
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

engine=AsyncEngine(
    create_engine(
        url=settings.DATABASE_URL,
        echo=True
    )
)
async def init_db() -> None :
    async with engine.begin() as conn:
        from src.books.models import Book
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    session=sessionmaker(
        bind=engine,
        class_= AsyncSession,
        expire_on_commit=False
    )
    async with session() as session:
        yield session