import pytest
from pydantic import ValidationError

from app.schemas.word import WordResponse


def test_word_response_valid():
    word = WordResponse(id=1, text="Think", ipa=["θ", "ɪ", "ŋ", "k"])
    assert word.id == 1
    assert word.text == "Think"
    assert isinstance(word.ipa, list)
    assert all(isinstance(p, str) for p in word.ipa)


def test_word_response_rejects_missing_fields():
    with pytest.raises(ValidationError):
        WordResponse(id=1, text="Think")  # missing ipa
