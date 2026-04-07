---
applyTo: "frontend/**"
---

# Frontend Coding Instructions

## Tech Stack

- React 19 (TypeScript) + Vite
- Tailwind CSS 4
- TanStack React Query 5 (server state)
- React Router 7 (routing)

## Project Structure

```
src/
├── pages/
│   ├── HomePage.tsx              # File tree browser
│   └── EditorPage.tsx            # Kitchen Sink structured editor
├── components/
│   ├── ui/
│   │   └── Button.tsx            # Reusable button component
│   └── features/
│       └── FileTree/
│           └── FileTree.tsx      # Recursive folder/file tree from /api/v1/features/tree
├── services/
│   ├── api.ts                    # Base fetch client — all HTTP calls go here
│   └── featureApi.ts             # useFeatureTree, useFeatureDetail, useSaveFeature
├── types/
│   └── index.ts                  # TreeNode, FeatureDetail, ScenarioStep, etc.
├── lib/
│   └── utils.ts                  # cn() — conditional class helper
├── App.tsx                       # Router setup, QueryClientProvider
├── main.tsx                      # React root + StrictMode
└── index.css                     # Tailwind directives
```

## Architecture Rules

- **API layer is the boundary.** All HTTP calls go through `services/api.ts`. Never use `fetch` directly in components.
- **Server state via React Query.** Use `useQuery` for reads (`tree`, `detail`), `useMutation` for writes (`save`). Invalidate the tree query on successful save.
- **Last-Write-Wins save strategy.** On save, send the entire form state as JSON to `POST /api/v1/features/save`. No partial updates.
- **Path alias:** `@` maps to `./src` (configured in `vite.config.ts` and `tsconfig`).
- **API base URL:** Set via `VITE_API_URL` env var (defaults to `http://localhost:8000`).

## Adding a New Feature

1. Add TypeScript types in `src/types/index.ts`
2. Create API service functions in `src/services/yourApi.ts` using `apiFetch`
3. Create React Query hooks (useQuery/useMutation) in the same service file
4. Create page component in `src/pages/YourPage.tsx`
5. Add route in `src/App.tsx`
6. For reusable UI, add components to `src/components/ui/`
7. For feature-specific components, create `src/components/features/YourFeature/`

## Coding Conventions

- Pages are named exports (`export function EditorPage()`).
- Components are in `components/features/` (feature-specific) or `components/ui/` (generic).
- Types live in `types/` and mirror backend Pydantic schemas.
- API services are thin wrappers: one function per endpoint, typed return values.
- Tailwind classes directly in JSX. Use `cn()` for conditional classes.
- The Kitchen Sink editor form is split into three sections: **Header** (Feature name, description, `@entry`/`@usecase` tags), **Background** (dynamic Given/And step list), and **Scenarios** (array of Scenario cards with Given/When/Then steps).
- `@entry` and `@usecase` tags are required; the form must default them and prevent saving without them.
