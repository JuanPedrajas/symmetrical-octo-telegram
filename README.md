# Full-Stack App Template

A reusable full-stack template for AI-assisted development with Docker, FastAPI, React, Poetry, and Vite.

## Tech Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Backend  | Python 3.12+, FastAPI, SQLAlchemy 2 |
| Frontend | React 19, TypeScript, Vite, Tailwind CSS 4 |
| Database | SQLite (async via aiosqlite)        |
| State    | TanStack React Query 5             |
| Routing  | React Router 7                      |
| Tooling  | Docker Compose, Poetry, npm        |

## Quick Start

```bash
# Build the Docker image
make build

# Start the app (backend on :8000, frontend on :5173)
make server

# Check health
curl http://localhost:8000/health

# View logs
make logs

# Run tests
make test

# Stop
make clean
```

## Project Structure

```
├── .github/
│   ├── copilot-instructions.md          # Repo-wide Copilot instructions
│   ├── copilot-setup-steps.yml          # Copilot coding agent setup
│   └── instructions/
│       ├── backend.instructions.md      # Backend-specific instructions
│       └── frontend.instructions.md     # Frontend-specific instructions
├── backend/
│   ├── app/
│   │   ├── api/v1/items.py       # REST endpoints
│   │   ├── models/item.py        # SQLAlchemy ORM model
│   │   ├── schemas/item.py       # Pydantic request/response schemas
│   │   ├── services/item_service.py  # Business logic (CRUD)
│   │   └── core/                 # Config, database setup
│   ├── tests/                    # pytest + httpx async tests
│   └── main.py                   # FastAPI app entry point
├── frontend/
│   ├── src/
│   │   ├── pages/HomePage.tsx    # Landing page
│   │   ├── services/itemApi.ts   # API client + React Query hooks
│   │   ├── types/index.ts        # TypeScript interfaces
│   │   └── components/ui/        # Reusable UI components
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── start.sh
└── Makefile                      # Build, run, test commands
```

## Architecture Overview

**Backend** follows a three-layer architecture:
- **Router** (`api/v1/`) — HTTP endpoints, input validation
- **Service** (`services/`) — business logic, database queries
- **Model** (`models/`) — SQLAlchemy ORM definitions

**Frontend** separates concerns:
- **Pages** — route-level components
- **Services** — API calls via `apiFetch` + React Query hooks
- **Types** — TypeScript interfaces mirroring backend schemas

## Adding a New Feature

### Backend
1. Create ORM model in `app/models/`
2. Create Pydantic schemas in `app/schemas/` (Create, Update, Response)
3. Create async service functions in `app/services/`
4. Create router with endpoints in `app/api/v1/`
5. Register router in `main.py`
6. Add tests in `tests/`

### Frontend
1. Add TypeScript types in `src/types/index.ts`
2. Create API service + React Query hooks in `src/services/`
3. Create page component in `src/pages/`
4. Add route in `src/App.tsx`

## Environment Variables

| Variable         | Default                             | Description       |
|------------------|-------------------------------------|-------------------|
| `APP_DATABASE_URL` | `sqlite+aiosqlite:///./app.db`    | Database URL      |
| `VITE_API_URL`   | `http://localhost:8000`             | Backend API URL   |

## AI-Assisted Development

This template includes GitHub Copilot coding agent configuration files under `.github/`:

- **`.github/copilot-instructions.md`** — repo-wide instructions (tech stack, commands, architecture overview, adding a new feature)
- **`.github/instructions/backend.instructions.md`** — backend-specific rules and conventions (scoped to `backend/**`)
- **`.github/instructions/frontend.instructions.md`** — frontend-specific rules and conventions (scoped to `frontend/**`)
- **`.github/copilot-setup-steps.yml`** — environment setup for the Copilot coding agent VM
