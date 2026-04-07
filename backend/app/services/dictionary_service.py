import json

from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.word import Word
from app.schemas.word import WordResponse


async def get_all_words(db: AsyncSession) -> list[WordResponse]:
    result = await db.execute(select(Word))
    return [WordResponse.model_validate(w) for w in result.scalars().all()]


async def get_word_by_id(word_id: int, db: AsyncSession) -> WordResponse:
    result = await db.execute(select(Word).where(Word.id == word_id))
    word = result.scalar_one_or_none()
    if word is None:
        raise HTTPException(status_code=404, detail=f"Word {word_id} not found")
    return WordResponse.model_validate(word)


async def seed_dictionary_from_json(file_path: str, db: AsyncSession) -> None:
    with open(file_path) as f:
        data = json.load(f)
    await db.execute(delete(Word))
    for entry in data:
        db.add(Word(text=entry["text"], ipa=entry["ipa"]))
    await db.commit()
