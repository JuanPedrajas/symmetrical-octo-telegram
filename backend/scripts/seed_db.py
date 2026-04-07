import asyncio
import sys

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings
from app.models.base import Base
from app.services.dictionary_service import seed_dictionary_from_json


async def main(file_path: str) -> None:
    settings = get_settings()
    engine = create_async_engine(settings.database_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        await seed_dictionary_from_json(file_path, session)

    await engine.dispose()
    print(f"Seeded dictionary from {file_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/seed_db.py <path/to/words.json>")
        sys.exit(1)
    asyncio.run(main(sys.argv[1]))
