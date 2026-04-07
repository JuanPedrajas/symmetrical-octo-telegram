# Full-Stack App Template

## What This Repo Does

A full-stack CRUD application template with a FastAPI backend and a React frontend, deployed via Docker Compose.

## Tech Stack

| Layer    | Technology                                   |
|----------|----------------------------------------------|
| Backend  | Python 3.12+, FastAPI, SQLAlchemy 2 (async)  |
| Frontend | React 19, TypeScript, Vite, Tailwind CSS 4   |
| Database | SQLite (async via aiosqlite)                  |
| State    | TanStack React Query 5                        |
| Routing  | React Router 7                                |
| Tooling  | Docker Compose, Poetry, npm                   |

## Build / Run / Test Commands

```bash
make build     # Build Docker image
make server    # Start containers (backend :8000, frontend :5173)
make clean     # Stop and remove containers
make restart   # Stop then start
make logs      # Tail container logs
make test      # Run pytest inside container
```

## Environment Variables

| Variable           | Default                          | Description          |
|--------------------|----------------------------------|----------------------|
| `APP_DATABASE_URL` | `sqlite+aiosqlite:///./app.db`   | Database URL         |
| `VITE_API_URL`     | `http://localhost:8000`          | Backend API URL      |

## Architecture Overview

**Backend** — three-layer architecture:
- **Router** (`app/api/v1/`) — HTTP endpoints, input validation
- **Service** (`app/services/`) — business logic, database queries
- **Model** (`app/models/`) — SQLAlchemy ORM definitions

**Frontend** — separation of concerns:
- **Pages** (`src/pages/`) — route-level components
- **Services** (`src/services/`) — API calls via `apiFetch` + React Query hooks
- **Types** (`src/types/`) — TypeScript interfaces mirroring backend schemas

## Adding a New Feature (End-to-End)

### Backend
1. Create ORM model in `backend/app/models/`
2. Create Pydantic schemas in `backend/app/schemas/` (`Create`, `Update`, `Response`)
3. Create async service functions in `backend/app/services/`
4. Create router with endpoints in `backend/app/api/v1/`
5. Register router in `backend/app/main.py`
6. Import the model in `main.py` so tables are created at startup
7. Add tests in `backend/tests/`

### Frontend
1. Add TypeScript types in `frontend/src/types/index.ts`
2. Create API service + React Query hooks in `frontend/src/services/`
3. Create page component in `frontend/src/pages/`
4. Add route in `frontend/src/App.tsx`
