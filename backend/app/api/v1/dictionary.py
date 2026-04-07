from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.word import WordResponse
from app.services.dictionary_service import get_all_words, get_word_by_id

router = APIRouter(prefix="/words", tags=["dictionary"])

DbSession = Annotated[AsyncSession, Depends(get_session)]


@router.get("", response_model=list[WordResponse])
async def list_words(db: DbSession):
    return await get_all_words(db)


@router.get("/{word_id}", response_model=WordResponse)
async def get_word(word_id: int, db: DbSession):
    return await get_word_by_id(word_id, db)
