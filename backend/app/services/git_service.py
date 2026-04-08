"""Git service — wraps all filesystem and Git operations.

The Git repository is the database for `.feature` files.
"""
import os
from pathlib import Path

from git import Repo

from app.core.config import get_settings


def get_repo_tree() -> dict:
    """Return a nested dict representing the `.feature` file tree.

    Only `.feature` files are included. Non-feature files are ignored.
    Leaf values are the relative path strings; intermediate nodes are dicts.

    Example::

        {
            "initiatives": {
                "npp": {
                    "accounts": {
                        "activate_account.feature": "initiatives/npp/accounts/activate_account.feature"
                    }
                }
            }
        }
    """
    settings = get_settings()
    root = Path(settings.repo_path)

    if settings.git_remote_url and root.exists():
        try:
            repo = Repo(str(root))
            repo.remote("origin").pull()
        except Exception:
            pass

    tree: dict = {}

    for dirpath, _dirnames, filenames in os.walk(root):
        feature_files = [f for f in filenames if f.endswith(".feature")]
        if not feature_files:
            continue

        rel_dir = Path(dirpath).relative_to(root)
        parts = rel_dir.parts

        for filename in feature_files:
            node = tree
            for part in parts:
                node = node.setdefault(part, {})
            rel_file_path = str(rel_dir / filename)
            node[filename] = rel_file_path

    return tree


def commit_file(relative_path: str, content: str, author: str) -> None:
    """Write *content* to *relative_path* inside the repo, then commit and push.

    Args:
        relative_path: Path relative to the repo root (e.g. ``initiatives/npp/x.feature``).
        content: Full text content to write.
        author: Display name included in the commit message.
    """
    settings = get_settings()
    repo = Repo(settings.repo_path)

    abs_path = Path(repo.working_tree_dir) / relative_path
    abs_path.parent.mkdir(parents=True, exist_ok=True)
    abs_path.write_text(content, encoding="utf-8")

    repo.index.add([str(abs_path)])
    repo.index.commit(f"Updated by {author}")

    if settings.git_remote_url:
        remote = repo.remote("origin")
        remote.push()
