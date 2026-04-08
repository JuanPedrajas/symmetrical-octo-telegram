"""Integration tests for /api/v1/features/* endpoints (Phase 3 TDD)."""
import pytest
import pytest_asyncio
from unittest.mock import patch, MagicMock

from httpx import AsyncClient, ASGITransport

from main import app


SAMPLE_FEATURE_DATA = {
    "feature": "Activate Account",
    "description": "PM wants to activate an account",
    "tags": ["@entry:npp", "@usecase:activate-account"],
    "background": [{"keyword": "Given", "text": "I am authenticated"}],
    "scenarios": [
        {
            "name": "Happy path",
            "tags": [],
            "steps": [
                {"keyword": "Given", "text": "the account exists"},
                {"keyword": "When", "text": "I activate it"},
                {"keyword": "Then", "text": "it is active"},
            ],
        }
    ],
}

SAMPLE_FEATURE_TEXT = """\
@entry:npp @usecase:activate-account
Feature: Activate Account
  PM wants to activate an account

  Background:
    Given I am authenticated

  Scenario: Happy path
    Given the account exists
    When I activate it
    Then it is active
"""


@pytest_asyncio.fixture
async def features_client():
    """Async client that does NOT need a db session (features router has no DB dep)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


# ---------------------------------------------------------------------------
# GET /api/v1/features/tree
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_tree_returns_200_with_tree_key(features_client):
    mock_tree = {
        "initiatives": {
            "npp": {
                "accounts": {
                    "activate_account.feature": "initiatives/npp/accounts/activate_account.feature"
                }
            }
        }
    }
    with patch("app.api.v1.features.get_repo_tree", return_value=mock_tree):
        response = await features_client.get("/api/v1/features/tree")

    assert response.status_code == 200
    body = response.json()
    assert "tree" in body
    assert body["tree"] == mock_tree


@pytest.mark.asyncio
async def test_get_tree_returns_empty_dict_when_repo_empty(features_client):
    with patch("app.api.v1.features.get_repo_tree", return_value={}):
        response = await features_client.get("/api/v1/features/tree")

    assert response.status_code == 200
    assert response.json() == {"tree": {}}


# ---------------------------------------------------------------------------
# GET /api/v1/features/detail
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_detail_returns_parsed_feature(features_client, tmp_path):
    feature_path = tmp_path / "activate_account.feature"
    feature_path.write_text(SAMPLE_FEATURE_TEXT)

    with patch("app.api.v1.features.get_settings") as mock_settings, \
         patch("app.api.v1.features.parse_feature", return_value=SAMPLE_FEATURE_DATA):
        mock_settings.return_value.repo_path = str(tmp_path)
        response = await features_client.get(
            "/api/v1/features/detail",
            params={"path": "activate_account.feature"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["feature"] == "Activate Account"
    assert "@entry:npp" in body["tags"]
    assert "@usecase:activate-account" in body["tags"]
    assert len(body["background"]) == 1
    assert len(body["scenarios"]) == 1


@pytest.mark.asyncio
async def test_get_detail_returns_404_when_file_missing(features_client, tmp_path):
    with patch("app.api.v1.features.get_settings") as mock_settings:
        mock_settings.return_value.repo_path = str(tmp_path)
        response = await features_client.get(
            "/api/v1/features/detail",
            params={"path": "non_existent.feature"},
        )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_detail_returns_400_on_path_traversal(features_client, tmp_path):
    with patch("app.api.v1.features.get_settings") as mock_settings:
        mock_settings.return_value.repo_path = str(tmp_path)
        response = await features_client.get(
            "/api/v1/features/detail",
            params={"path": "../../etc/passwd"},
        )

    assert response.status_code == 400


# ---------------------------------------------------------------------------
# POST /api/v1/features/save
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_save_feature_returns_200_on_success(features_client):
    payload = {
        "path": "initiatives/npp/accounts/activate_account.feature",
        "author": "PM Bot",
        "data": SAMPLE_FEATURE_DATA,
    }
    with patch("app.api.v1.features.compile_feature", return_value=SAMPLE_FEATURE_TEXT), \
         patch("app.api.v1.features.commit_file") as mock_commit:
        response = await features_client.post("/api/v1/features/save", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["path"] == payload["path"]


@pytest.mark.asyncio
async def test_save_feature_calls_commit_file_with_correct_args(features_client):
    payload = {
        "path": "initiatives/npp/accounts/activate_account.feature",
        "author": "PM Bot",
        "data": SAMPLE_FEATURE_DATA,
    }
    with patch("app.api.v1.features.compile_feature", return_value=SAMPLE_FEATURE_TEXT) as mock_compile, \
         patch("app.api.v1.features.commit_file") as mock_commit:
        await features_client.post("/api/v1/features/save", json=payload)

    mock_commit.assert_called_once_with(
        payload["path"],
        SAMPLE_FEATURE_TEXT,
        author="PM Bot",
    )


@pytest.mark.asyncio
async def test_save_feature_returns_422_when_missing_required_tags(features_client):
    invalid_data = {**SAMPLE_FEATURE_DATA, "tags": ["@entry:npp"]}  # missing @usecase
    payload = {
        "path": "initiatives/npp/accounts/activate_account.feature",
        "author": "PM Bot",
        "data": invalid_data,
    }
    with patch("app.api.v1.features.compile_feature", side_effect=ValueError("Missing @usecase tag")):
        response = await features_client.post("/api/v1/features/save", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_save_feature_returns_400_on_path_traversal(features_client):
    payload = {
        "path": "../../etc/cron.d/evil",
        "author": "Attacker",
        "data": SAMPLE_FEATURE_DATA,
    }
    response = await features_client.post("/api/v1/features/save", json=payload)
    assert response.status_code == 400
