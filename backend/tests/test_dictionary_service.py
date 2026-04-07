import json

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.word import Word
from app.schemas.word import WordResponse
from app.services.dictionary_service import (
    get_all_words,
    get_word_by_id,
    seed_dictionary_from_json,
)


async def test_get_all_words_returns_seeded_words(db_session: AsyncSession):
    db_session.add(Word(text="Think", ipa=["θ", "ɪ", "ŋ", "k"]))
    db_session.add(Word(text="The", ipa=["ð", "ə"]))
    await db_session.commit()

    result = await get_all_words(db_session)

    assert len(result) == 2
    assert all(isinstance(w, WordResponse) for w in result)


async def test_get_word_by_id_returns_correct_word(db_session: AsyncSession):
    word = Word(text="Think", ipa=["θ", "ɪ", "ŋ", "k"])
    db_session.add(word)
    await db_session.commit()
    await db_session.refresh(word)

    result = await get_word_by_id(word.id, db_session)

    assert isinstance(result, WordResponse)
    assert result.text == "Think"
    assert result.ipa == ["θ", "ɪ", "ŋ", "k"]


async def test_get_word_by_id_raises_404_for_missing_id(db_session: AsyncSession):
    with pytest.raises(HTTPException) as exc_info:
        await get_word_by_id(9999, db_session)
    assert exc_info.value.status_code == 404


async def test_seed_dictionary_replaces_on_second_call(db_session: AsyncSession, tmp_path):
    first_data = [
        {"text": "Think", "ipa": ["θ", "ɪ", "ŋ", "k"]},
        {"text": "The", "ipa": ["ð", "ə"]},
    ]
    second_data = [
        {"text": "Three", "ipa": ["θ", "r", "iː"]},
    ]

    first_file = tmp_path / "first.json"
    second_file = tmp_path / "second.json"
    first_file.write_text(json.dumps(first_data))
    second_file.write_text(json.dumps(second_data))

    await seed_dictionary_from_json(str(first_file), db_session)
    await seed_dictionary_from_json(str(second_file), db_session)

    result = await get_all_words(db_session)
    assert len(result) == 1
    assert result[0].text == "Three"
