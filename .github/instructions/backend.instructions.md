---
applyTo: "backend/**"
---

# Backend Coding Instructions

## Tech Stack

- Python 3.12+
- FastAPI
- GitPython (Git repository as the database)
- `gherkin-official` (Gherkin parser)
- Pydantic v2 for request/response models
- Poetry for dependency management

## Project Structure

```
app/
├── api/
│   └── v1/
│       └── features.py       # GET /tree, GET /detail, POST /save
├── schemas/
│   └── feature.py            # FeatureDetail, SaveRequest, TreeResponse
├── services/
│   └── git_service.py        # get_repo_tree(), commit_file(path, content, author)
├── utils/
│   └── gherkin_parser.py     # parse(text) → JSON, compile(json) → .feature text
├── core/
│   ├── config.py             # Settings (REPO_PATH, GIT_REMOTE_URL) via pydantic-settings
│   └── database.py           # (retained from template; unused by Gherkin feature)
└── main.py                   # FastAPI app with CORS + lifespan
tests/
├── conftest.py               # Shared fixtures (async_client, tmp repo)
├── test_git_service.py       # Unit tests for git_service (mocked filesystem)
├── test_gherkin_utils.py     # Unit tests for parser and compiler
└── test_features_router.py   # Integration tests for /api/v1/features/*
```

## Architecture Rules

- **Git is the database.** There is no ORM or SQL for feature files. `git_service.py` owns all filesystem and Git operations.
- **One router per domain.** Each domain gets its own file under `api/v1/`.
- **Three-layer architecture:** Router → Service → Git/Utils. Routers validate input and call services. Services call `git_service` or `gherkin_parser`. Never touch the filesystem or Git directly in routers.
- **All route handlers are `async def`.**
- **Dependency injection via `Depends()`.** Use `Annotated[type, Depends(...)]` for type-safe injection.
- **Pydantic models are the contract.** API consumers see Pydantic schemas, never raw dicts.

## Adding a New Endpoint

1. Add Pydantic schemas in `app/schemas/your_schema.py` (`Request`, `Response`)
2. Add service functions in `app/services/your_service.py`
3. Create router in `app/api/v1/your_router.py`
4. Register the router in `main.py` (`app.include_router(...)`)
5. Add TDD tests in `tests/test_your_router.py` (Red → Green)

## Coding Conventions

- Pydantic schema naming: `{Entity}Request`, `{Entity}Response`.
- Route function naming: verb first, noun second (`get_tree`, `get_detail`, `save_feature`).
- Error responses: raise `HTTPException` with specific status codes and detail messages.
- Environment config: use `pydantic-settings` with `Settings` class and `APP_` prefix. Access via `get_settings()`. Never use `os.getenv()`.
- Gherkin tagging convention: always enforce `@entry:` and `@usecase:` tags in the compiler output.

## Testing

- Framework: `pytest` + `pytest-asyncio` (auto mode)
- HTTP client: `httpx.AsyncClient` with `ASGITransport`
- Git operations: mock the filesystem with `tmp_path` or `unittest.mock`; do not rely on a real remote
- Test files mirror the modules they test
- Run tests: `make test`

## NEVER DO THIS

1. **Never do filesystem or Git operations in routers.** Routers call services, services call `git_service`.
2. **Never return raw dicts from endpoints.** Always map to a Pydantic Response schema.
3. **Never hardcode paths or remote URLs.** Use environment variables via `pydantic-settings`.
4. **Never push to the remote inside a unit test.** Mock `git push` calls.
