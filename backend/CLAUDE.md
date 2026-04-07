## Tech Stack

- Python 3.12+
- FastAPI
- SQLAlchemy 2.0 (async)
- Pydantic v2 for request/response models
- SQLite database (via aiosqlite)
- Poetry for dependency management

## Project Structure

```
app/
├── api/
│   └── v1/
│       └── items.py          # GET/POST/DELETE /api/v1/items
├── models/
│   ├── base.py               # DeclarativeBase for all models
│   └── item.py               # Item ORM model (id, name, description)
├── schemas/
│   └── item.py               # ItemCreate, ItemUpdate, ItemResponse
├── services/
│   └── item_service.py       # Async CRUD (get_all, get_by_id, create, delete)
├── core/
│   ├── config.py             # Settings via pydantic-settings (env prefix: APP_)
│   └── database.py           # Async engine + session factory
└── main.py                   # FastAPI app with CORS + lifespan (DB init)
tests/
├── conftest.py               # In-memory SQLite fixtures (db_session, async_client)
└── test_items_router.py      # 5 CRUD tests via HTTP
```

## Architecture Rules

- **One router per domain.** Each domain gets its own file under `api/v1/`.
- **Three-layer architecture:** Router → Service → Model. Routers validate input and call services. Services contain business logic and call the ORM. Never do ORM queries directly in router functions.
- **All route handlers are `async def`.** Use async natively with aiosqlite.
- **Dependency injection via `Depends()`.** Use `Annotated[type, Depends(...)]` for type-safe injection. See `DbSession` in routers.
- **Pydantic models are the contract.** API consumers see Pydantic schemas, never SQLAlchemy models. Map with `model_validate()`.

## Adding a New Domain

1. Create the ORM model in `app/models/your_model.py`
2. Create Pydantic schemas in `app/schemas/your_model.py` (`Create`, `Update`, `Response`)
3. Create service functions in `app/services/your_service.py` (async CRUD)
4. Create router in `app/api/v1/your_router.py` with endpoints
5. Register the router in `main.py` (`app.include_router(...)`)
6. Import the model in `main.py` so tables are created at startup
7. Add tests in `tests/test_your_router.py`

## Coding Conventions

- Pydantic schema naming: `{Entity}Create`, `{Entity}Update`, `{Entity}Response`.
- Route function naming: verb first, noun second (`get_item`, `create_item`, `list_items`).
- Error responses: raise `HTTPException` with specific status codes and detail messages.
- Environment config: use `pydantic-settings` with `Settings` class. Access via `get_settings()`. Never use `os.getenv()`.

## Testing

- Framework: `pytest` + `pytest-asyncio` (auto mode)
- HTTP client: `httpx.AsyncClient` with `ASGITransport`
- Database: in-memory SQLite per test via `conftest.py` fixtures
- Test files mirror the modules they test
- Run tests: `make test`

## NEVER DO THIS

1. **Never do ORM queries in routers.** Routers call services, services call the ORM.
2. **Never return SQLAlchemy models from endpoints.** Always map to a Pydantic Response schema.
3. **Never hardcode connection strings or secrets.** Use environment variables via `pydantic-settings`.
4. **Never use synchronous database drivers in async code.**
