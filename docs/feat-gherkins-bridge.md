## Phase 1: Git Service & Repository Plumbing
We need to treat the Git repository as our primary database. We will use `GitPython` to interact with the repo locally within the Docker container.

### [Task 1] Environment Setup
* **1.1:** Add `GitPython` and `gherkin-official` (parser) to `backend/pyproject.toml`.
* **1.2:** Update `backend/app/core/config.py` to include `REPO_PATH` and `GIT_REMOTE_URL`.

### [Task 2] Git Service (TDD)
* **2.1 [Red]:** Create `backend/tests/test_git_service.py`. Write a test for `get_repo_tree()` that mocks a filesystem and asserts a nested dictionary structure is returned.
* **2.2 [Green]:** Implement `backend/app/services/git_service.py`. Use `os.walk` or `git ls-tree` to generate the file tree for the `initiatives/` folder.
* **2.3 [Red]:** Write a test for `commit_file(path, content, author)`.
* **2.4 [Green]:** Implement `commit_file`. It must:
    1. Write content to disk.
    2. `git add`.
    3. `git commit -m "Updated by [Author]"` using the Service Account.
    4. `git push origin main`.

---

## Phase 2: Gherkin Parsing Engine
The "Kitchen Sink" editor requires converting raw `.feature` text into a structured JSON object for the frontend and back again.

### [Task 3] Serialization Logic (TDD)
* **3.1 [Red]:** Create `backend/tests/test_gherkin_utils.py`. Write a test that takes the content of `template.feature` (from the provided repo) and asserts the parser returns a JSON object with `feature`, `tags`, `background`, and `scenarios`.
* **3.2 [Green]:** Implement `backend/app/utils/gherkin_parser.py` using the `gherkin-official` library.
* **3.3 [Red]:** Write a test for the "Compiler" that takes a JSON object and produces a valid `.feature` string.
* **3.4 [Green]:** Implement the compiler logic. Ensure it handles the Ebury-specific tagging convention (`@entry:`, `@usecase:`) as defined in `CONTRIBUTING.md`.

---

## Phase 3: Backend API Endpoints
We will adapt the template's 3-layer architecture (Router $\rightarrow$ Service $\rightarrow$ Git).

### [Task 4] CRUD API (TDD)
* **4.1 [Red]:** Create `backend/tests/test_features_router.py`. Test `GET /api/v1/features/tree`.
* **4.2 [Green]:** Create `backend/app/api/v1/features.py` and register in `main.py`.
* **4.3 [Red]:** Test `GET /api/v1/features/detail?path=initiatives/npp/accounts/activate_asl_account.feature`.
* **4.4 [Green]:** Implement detail endpoint. It should read the file and return the **Parsed JSON** (not raw text).
* **4.5 [Red]:** Test `POST /api/v1/features/save` which accepts the "Kitchen Sink" JSON and triggers a Git commit.
* **4.6 [Green]:** Implement save endpoint.

---

## Phase 4: Frontend Development
Based on the provided React template.

### [Task 5] Navigation & File Tree
* **5.1:** Create `frontend/src/components/features/FileTree.tsx`. It should recursively render folders and files from the `tree` API.
* **5.2:** Use `TanStack Query` in `frontend/src/services/featureApi.ts` to fetch and cache the tree structure.

### [Task 6] The "Kitchen Sink" Editor
* **6.1:** Create `frontend/src/pages/EditorPage.tsx`.
* **6.2:** Build the **Structured Form**:
    * **Header Section:** Inputs for Feature Name, Description, and a tag-manager for `@entry` and `@usecase`.
    * **Background Section:** A dynamic list of Given/And steps.
    * **Scenarios Section:** An array of Scenario cards. Each card contains its own list of Given/When/Then steps.
* **6.3:** Implement **Last-Write-Wins** Save: On click, send the entire form state as JSON to the `save` endpoint.

---

## Phase 5: File Operations & Safety

### [Task 7] Full File Management
* **7.1:** Add "New File" and "Delete" buttons to the `FileTree`.
* **7.2:** Implement a confirmation modal for deletions to mitigate the risk of direct-to-main data loss.

### [Task 8] Final Integration & Docker
* **8.1:** Update `docker/start.sh` to ensure the container clones the `gherkins-repo` into a known volume on startup.
* **8.2:** Run `make test` to ensure both the dictionary implementation from the template and the new Gherkin logic are green.

---

### Key Rules from `gherkins-repo` to Enforce:
1.  **Tagging:** The editor must default to or require `@entry` and `@usecase` tags.
2.  **Glossary Check:** (Optional V2) Add a link in the UI to the `glossary.md` of the current initiative to help PMs follow the rule: *"All domain objects must start with a capital letter and be defined in glossary.md"*.
