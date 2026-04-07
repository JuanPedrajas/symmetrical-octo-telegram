# Template Guide

## Overview

This is a full-stack application template designed for AI-assisted development. It provides a working Docker + FastAPI + React setup with a simple `Item` CRUD domain as a reference implementation.

### Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend   | FastAPI + SQLAlchemy 2 (async) | REST API with 3-layer architecture |
| Frontend  | React 19 + TypeScript + Vite | SPA with React Query for server state |
| Database  | SQLite (aiosqlite) | Lightweight async database |
| Styling   | Tailwind CSS 4 | Utility-first CSS |
| Deps      | Poetry (backend), npm (frontend) | Dependency management |
| Deploy    | Docker Compose | Single-command build & run |

## Getting Started

```bash
# 1. Build the Docker image
make build

# 2. Start the application
make server
# Backend: http://localhost:8000
# Frontend: http://localhost:5173

# 3. Verify it works
curl http://localhost:8000/health          # {"status": "ok"}
curl http://localhost:8000/api/v1/items/   # []

# 4. Run tests
make test

# 5. Stop everything
make clean
```

## Architecture

### Backend (3-Layer)

```
Request → Router → Service → ORM Model → Database
                                ↓
Response ← Router ← Service ← Pydantic Schema
```

- **Router** (`app/api/v1/`): Defines HTTP endpoints, validates input via Pydantic, calls service functions
- **Service** (`app/services/`): Contains business logic, executes database queries via SQLAlchemy
- **Model** (`app/models/`): SQLAlchemy ORM classes defining database tables
- **Schema** (`app/schemas/`): Pydantic models for request/response serialization

### Frontend

```
User → Page Component → React Query Hook → API Service → fetch(backend)
                              ↓
UI Update ← React Query Cache ← JSON Response
```

- **Pages** (`src/pages/`): Route-level components
- **Services** (`src/services/`): API client functions + React Query hooks
- **Types** (`src/types/`): TypeScript interfaces mirroring backend schemas
- **Components** (`src/components/`): Reusable UI (`ui/`) and feature-specific (`features/`)

## Adding a New Feature End-to-End

Example: Adding a `Task` resource with `title` and `done` fields.

### Step 1: Backend Model

Create `backend/app/models/task.py`:

```python
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
```

### Step 2: Backend Schema

Create `backend/app/schemas/task.py`:

```python
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    done: bool = False

class TaskResponse(BaseModel):
    id: int
    title: str
    done: bool
    model_config = {"from_attributes": True}
```

### Step 3: Backend Service

Create `backend/app/services/task_service.py`:

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse

async def get_all_tasks(db: AsyncSession) -> list[TaskResponse]:
    result = await db.execute(select(Task))
    return [TaskResponse.model_validate(t) for t in result.scalars().all()]

async def create_task(data: TaskCreate, db: AsyncSession) -> TaskResponse:
    task = Task(title=data.title, done=data.done)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return TaskResponse.model_validate(task)
```

### Step 4: Backend Router

Create `backend/app/api/v1/tasks.py`:

```python
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.task import TaskCreate, TaskResponse
from app.services.task_service import get_all_tasks, create_task

router = APIRouter(prefix="/tasks", tags=["tasks"])
DbSession = Annotated[AsyncSession, Depends(get_session)]

@router.get("/", response_model=list[TaskResponse])
async def list_tasks(db: DbSession):
    return await get_all_tasks(db)

@router.post("/", response_model=TaskResponse, status_code=201)
async def create_task_endpoint(data: TaskCreate, db: DbSession):
    return await create_task(data, db)
```

### Step 5: Register in main.py

```python
from app.api.v1.tasks import router as tasks_router
import app.models.task  # noqa: F401

app.include_router(tasks_router, prefix="/api/v1")
```

### Step 6: Frontend Types

Add to `frontend/src/types/index.ts`:

```typescript
export interface TaskResponse {
  id: number;
  title: string;
  done: boolean;
}
```

### Step 7: Frontend API Service

Create `frontend/src/services/taskApi.ts`:

```typescript
import { useQuery } from "@tanstack/react-query";
import { apiFetch } from "@/services/api";
import type { TaskResponse } from "@/types";

export function getTasks(): Promise<TaskResponse[]> {
  return apiFetch<TaskResponse[]>("/api/v1/tasks/");
}

export function useTasks() {
  return useQuery({ queryKey: ["tasks"], queryFn: getTasks });
}
```

### Step 8: Frontend Page

Create `frontend/src/pages/TasksPage.tsx` and add a route in `App.tsx`.

### Step 9: Tests

Add `backend/tests/test_tasks_router.py` with async test cases using the `async_client` fixture.

## Docker Workflow

| Command | Description |
|---------|-------------|
| `make build` | Build Docker image |
| `make server` | Start containers (detached) |
| `make clean` | Stop and remove containers |
| `make restart` | Stop then start |
| `make logs` | Tail container logs |
| `make test` | Run pytest in container |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_DATABASE_URL` | `sqlite+aiosqlite:///./app.db` | Backend database connection string |
| `VITE_API_URL` | `http://localhost:8000` | Frontend API base URL |

## AI-Assisted Development

Both `backend/CLAUDE.md` and `frontend/CLAUDE.md` contain architecture rules and coding conventions. Point your AI coding assistant at these files to generate code that follows the project's patterns.
