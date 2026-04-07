# Gherkins Bridge

## What This Repo Does

A full-stack Gherkin feature-file editor that uses a Git repository as its database. Users can browse a file tree of `.feature` files, edit them through a structured "Kitchen Sink" form, and save changes back to the repo via automated Git commits. The backend parses Gherkin text into structured JSON and compiles it back, bridging a PM-friendly UI with a version-controlled source of truth.

## Tech Stack

| Layer      | Technology                                                        |
|------------|-------------------------------------------------------------------|
| Backend    | Python 3.12+, FastAPI, GitPython, gherkin-official                |
| Frontend   | React 19, TypeScript, Vite, Tailwind CSS 4                        |
| Git Store  | Git repository mounted as a volume (`REPO_PATH`)                  |
| State      | TanStack React Query 5                                            |
| Routing    | React Router 7                                                    |
| Tooling    | Docker Compose, Poetry, npm                                       |

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

| Variable            | Default                  | Description                              |
|---------------------|--------------------------|------------------------------------------|
| `APP_REPO_PATH`     | `/repo`                  | Path to the mounted gherkins Git repo    |
| `APP_GIT_REMOTE_URL`| —                        | Remote URL for `git push`                |
| `VITE_API_URL`      | `http://localhost:8000`  | Backend API URL                          |

## Architecture Overview

**Backend** — three-layer architecture where **Git is the database**:
- **Router** (`app/api/v1/`) — HTTP endpoints, input validation
- **Service** (`app/services/`) — business logic; `git_service.py` reads/writes the repo
- **Utils** (`app/utils/`) — `gherkin_parser.py` parses `.feature` text → JSON and compiles JSON → `.feature` text

**Frontend** — separation of concerns:
- **Pages** (`src/pages/`) — route-level components (e.g., `EditorPage`)
- **Components** (`src/components/features/`) — feature-specific UI (e.g., `FileTree`, Kitchen Sink form sections)
- **Services** (`src/services/`) — API calls via `apiFetch` + React Query hooks
- **Types** (`src/types/`) — TypeScript interfaces mirroring backend Pydantic schemas

## Adding a New Feature (End-to-End)

### Backend
1. Add Pydantic schemas in `backend/app/schemas/` (`Request`, `Response`)
2. Add service functions in `backend/app/services/` (interact with `git_service` or `gherkin_parser`)
3. Create router with endpoints in `backend/app/api/v1/`
4. Register router in `backend/app/main.py`
5. Add tests in `backend/tests/` (TDD: Red → Green)

### Frontend
1. Add TypeScript types in `frontend/src/types/index.ts`
2. Create API service + React Query hooks in `frontend/src/services/`
3. Create page or feature component in `frontend/src/pages/` or `frontend/src/components/features/`
4. Add route in `frontend/src/App.tsx`
