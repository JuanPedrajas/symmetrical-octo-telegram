from sqlalchemy.types import JSON

from app.models.word import Word


def test_word_has_required_columns():
    columns = Word.__table__.columns.keys()
    assert "id" in columns
    assert "text" in columns
    assert "ipa" in columns


def test_word_ipa_is_json_compatible():
    ipa_col = Word.__table__.c["ipa"]
    assert isinstance(ipa_col.type, JSON)
