from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.word import Word


async def test_get_all_words_returns_200_with_list(
    async_client: AsyncClient, db_session: AsyncSession
):
    db_session.add(Word(text="Think", ipa=["θ", "ɪ", "ŋ", "k"]))
    db_session.add(Word(text="The", ipa=["ð", "ə"]))
    await db_session.commit()

    response = await async_client.get("/api/v1/words")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


async def test_get_word_by_id_returns_200_with_correct_body(
    async_client: AsyncClient, db_session: AsyncSession
):
    word = Word(text="Think", ipa=["θ", "ɪ", "ŋ", "k"])
    db_session.add(word)
    await db_session.commit()
    await db_session.refresh(word)

    response = await async_client.get(f"/api/v1/words/{word.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["text"] == "Think"
    assert data["ipa"] == ["θ", "ɪ", "ŋ", "k"]


async def test_get_word_by_id_returns_404_for_unknown_id(async_client: AsyncClient):
    response = await async_client.get("/api/v1/words/9999")
    assert response.status_code == 404
