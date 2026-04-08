import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from app.services.git_service import get_repo_tree, commit_file


# ---------------------------------------------------------------------------
# get_repo_tree
# ---------------------------------------------------------------------------


def _create_feature_files(base: Path) -> None:
    """Helper: build a small .feature file tree inside *base*."""
    (base / "initiatives" / "npp" / "accounts").mkdir(parents=True)
    (base / "initiatives" / "npp" / "payments").mkdir(parents=True)
    (base / "initiatives" / "npp" / "accounts" / "activate_account.feature").write_text(
        "Feature: Activate account"
    )
    (base / "initiatives" / "npp" / "payments" / "make_payment.feature").write_text(
        "Feature: Make payment"
    )
    (base / "initiatives" / "npp" / "accounts" / "README.md").write_text("# readme")


def test_get_repo_tree_returns_nested_dict(tmp_path):
    _create_feature_files(tmp_path)
    with patch("app.services.git_service.get_settings") as mock_settings:
        mock_settings.return_value.repo_path = str(tmp_path)
        tree = get_repo_tree()

    assert isinstance(tree, dict)
    assert "initiatives" in tree
    assert "npp" in tree["initiatives"]
    assert "accounts" in tree["initiatives"]["npp"]
    assert "payments" in tree["initiatives"]["npp"]


def test_get_repo_tree_only_includes_feature_files(tmp_path):
    _create_feature_files(tmp_path)
    with patch("app.services.git_service.get_settings") as mock_settings:
        mock_settings.return_value.repo_path = str(tmp_path)
        tree = get_repo_tree()

    accounts = tree["initiatives"]["npp"]["accounts"]
    assert "activate_account.feature" in accounts
    assert "README.md" not in accounts


def test_get_repo_tree_empty_repo(tmp_path):
    with patch("app.services.git_service.get_settings") as mock_settings:
        mock_settings.return_value.repo_path = str(tmp_path)
        tree = get_repo_tree()

    assert tree == {}


def test_get_repo_tree_pulls_when_remote_configured(tmp_path):
    _create_feature_files(tmp_path)
    mock_repo = MagicMock()
    mock_remote = MagicMock()
    mock_repo.remote.return_value = mock_remote

    with patch("app.services.git_service.get_settings") as mock_settings, \
         patch("app.services.git_service.Repo", return_value=mock_repo):
        mock_settings.return_value.repo_path = str(tmp_path)
        mock_settings.return_value.git_remote_url = "https://example.com/repo.git"
        get_repo_tree()

    mock_remote.pull.assert_called_once()


def test_get_repo_tree_skips_pull_when_no_remote(tmp_path):
    _create_feature_files(tmp_path)
    mock_repo = MagicMock()

    with patch("app.services.git_service.get_settings") as mock_settings, \
         patch("app.services.git_service.Repo", return_value=mock_repo):
        mock_settings.return_value.repo_path = str(tmp_path)
        mock_settings.return_value.git_remote_url = ""
        get_repo_tree()

    mock_repo.remote.assert_not_called()



def test_get_repo_tree_leaf_values_are_file_paths(tmp_path):
    """Leaf nodes should be the relative file path string, not nested dicts."""
    _create_feature_files(tmp_path)
    with patch("app.services.git_service.get_settings") as mock_settings:
        mock_settings.return_value.repo_path = str(tmp_path)
        tree = get_repo_tree()

    leaf = tree["initiatives"]["npp"]["accounts"]["activate_account.feature"]
    assert isinstance(leaf, str)
    assert leaf.endswith("activate_account.feature")


# ---------------------------------------------------------------------------
# commit_file
# ---------------------------------------------------------------------------


def test_commit_file_writes_content_to_disk(tmp_path):
    mock_repo = MagicMock()
    mock_repo.working_tree_dir = str(tmp_path)

    with patch("app.services.git_service.get_settings") as mock_settings, \
         patch("app.services.git_service.Repo", return_value=mock_repo):
        mock_settings.return_value.repo_path = str(tmp_path)
        mock_settings.return_value.git_remote_url = "https://example.com/repo.git"

        relative_path = "initiatives/npp/accounts/activate_account.feature"
        content = "Feature: Activate account\n  Scenario: Happy path\n"
        commit_file(relative_path, content, author="PM Bot")

    written = (tmp_path / relative_path).read_text()
    assert written == content


def test_commit_file_calls_git_add_and_commit(tmp_path):
    mock_repo = MagicMock()
    mock_repo.working_tree_dir = str(tmp_path)

    with patch("app.services.git_service.get_settings") as mock_settings, \
         patch("app.services.git_service.Repo", return_value=mock_repo):
        mock_settings.return_value.repo_path = str(tmp_path)
        mock_settings.return_value.git_remote_url = "https://example.com/repo.git"

        relative_path = "initiatives/npp/accounts/activate_account.feature"
        commit_file(relative_path, "Feature: X", author="PM Bot")

    mock_repo.index.add.assert_called_once()
    mock_repo.index.commit.assert_called_once()
    commit_msg = mock_repo.index.commit.call_args[0][0]
    assert "PM Bot" in commit_msg


def test_commit_file_calls_git_push_when_remote_configured(tmp_path):
    mock_repo = MagicMock()
    mock_repo.working_tree_dir = str(tmp_path)
    mock_remote = MagicMock()
    mock_repo.remote.return_value = mock_remote

    with patch("app.services.git_service.get_settings") as mock_settings, \
         patch("app.services.git_service.Repo", return_value=mock_repo):
        mock_settings.return_value.repo_path = str(tmp_path)
        mock_settings.return_value.git_remote_url = "https://example.com/repo.git"

        commit_file("initiatives/test.feature", "Feature: X", author="Bot")

    mock_remote.push.assert_called_once()


def test_commit_file_skips_push_when_no_remote(tmp_path):
    mock_repo = MagicMock()
    mock_repo.working_tree_dir = str(tmp_path)

    with patch("app.services.git_service.get_settings") as mock_settings, \
         patch("app.services.git_service.Repo", return_value=mock_repo):
        mock_settings.return_value.repo_path = str(tmp_path)
        mock_settings.return_value.git_remote_url = ""

        commit_file("initiatives/test.feature", "Feature: X", author="Bot")

    mock_repo.remote.assert_not_called()
