from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine

from app.api.v1.items import router as items_router
from app.api.v1.dictionary import router as dictionary_router
from app.core.config import get_settings
from app.models.base import Base
import app.models.item  # noqa: F401
import app.models.word  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_async_engine(get_settings().database_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router, prefix="/api/v1")
app.include_router(dictionary_router, prefix="/api/v1")


@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}


@app.get("/health")
async def health():
    return {"status": "ok"}
