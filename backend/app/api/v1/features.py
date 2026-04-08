"""Features router — GET /tree, GET /detail, POST /save."""
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

from app.core.config import get_settings
from app.schemas.feature import FeatureDetail, SaveRequest, SaveResponse, TreeResponse
from app.services.git_service import commit_file, get_repo_tree
from app.utils.gherkin_parser import compile_feature, parse_feature

router = APIRouter(prefix="/features", tags=["features"])


def _safe_resolve(repo_root: Path, relative_path: str) -> Path:
    """Resolve *relative_path* inside *repo_root* and raise 400 on traversal."""
    try:
        resolved = (repo_root / relative_path).resolve()
        resolved.relative_to(repo_root.resolve())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid path: directory traversal detected.")
    return resolved


@router.get("/tree", response_model=TreeResponse)
async def get_tree() -> TreeResponse:
    """Return the nested `.feature` file tree from the Git repo."""
    tree = get_repo_tree()
    return TreeResponse(tree=tree)


@router.get("/detail", response_model=FeatureDetail)
async def get_detail(path: str = Query(..., description="Relative path to the .feature file")) -> FeatureDetail:
    """Return the parsed JSON representation of a `.feature` file."""
    settings = get_settings()
    repo_root = Path(settings.repo_path)
    abs_path = _safe_resolve(repo_root, path)

    if not abs_path.exists():
        raise HTTPException(status_code=404, detail=f"Feature file not found: {path}")

    text = abs_path.read_text(encoding="utf-8")
    data = parse_feature(text)
    return FeatureDetail(**data)


@router.post("/save", response_model=SaveResponse)
async def save_feature(body: SaveRequest) -> SaveResponse:
    """Compile the Kitchen Sink JSON to `.feature` text and commit to Git."""
    settings = get_settings()
    repo_root = Path(settings.repo_path)
    _safe_resolve(repo_root, body.path)

    try:
        text = compile_feature(body.data.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    commit_file(body.path, text, author=body.author)
    return SaveResponse(status="ok", path=body.path)
