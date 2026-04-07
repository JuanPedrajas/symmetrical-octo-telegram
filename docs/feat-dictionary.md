## Phase 1: Test Suite
**Goal:** Write all failing tests and wire up the `make test` command. No implementation code exists yet — every test should fail with `ImportError` or `ModuleNotFoundError` by the end of this phase.

### [Task 1] Models & Schemas tests
* **ID:** 1
    - [x] 1.1: Create `backend/tests/test_models.py`. Write a test that imports `Word` from `app/models/word.py` and asserts it has `id`, `text`, and `ipa` columns. Assert that `ipa` is mapped to a JSON-compatible type.
    - [x] 1.2: Create `backend/tests/test_schemas.py`. Write a test that instantiates `WordResponse` with `{ "id": 1, "text": "Think", "ipa": ["θ", "ɪ", "ŋ", "k"] }` and asserts correct field types. Write a second test that asserts `WordResponse` rejects missing fields.

### [Task 2] Dictionary Service tests
* **ID:** 2
    - [x] 2.1: Create `backend/tests/test_dictionary_service.py`. Write a test for `get_all_words()` that seeds 2 `Word` rows via the test DB fixture and asserts the function returns a list of 2 `WordResponse` objects.
    - [x] 2.2: Write a test for `get_word_by_id(word_id)` that asserts it returns the correct `WordResponse` for a valid ID, and raises `HTTPException(404)` for a non-existent ID.
    - [x] 2.3: Write a test for `seed_dictionary_from_json(file_path)` that calls the function twice with different data and asserts the second call fully replaces the first (Clear & Reload semantics — final count matches the second file's entries, not the sum).

### [Task 3] Router tests
* **ID:** 3
    - [x] 3.1: Create `backend/tests/test_dictionary_router.py`. Using `httpx.AsyncClient` with `ASGITransport`, write a test for `GET /api/v1/words` that seeds 2 words and asserts a `200` response with a list of 2 `WordResponse` objects.
    - [x] 3.2: Write a test for `GET /api/v1/words/{id}` that asserts `200` and correct body for a valid ID, and `404` for an unknown ID.

### [Task 4] Wire up `make test`
* **ID:** 4
    - [x] 4.1: Add a `test` target to the root `Makefile` that runs `pytest tests/ -v` inside the Docker container.
    - [x] 4.2: Run `make test` and confirm all tests fail with `ImportError` / `ModuleNotFoundError` (no silent passes).

---

## Phase 2: Implementation
**Goal:** Write the minimum production code to turn every red test green.

### [Task 5] Models & Schemas
* **ID:** 5 | **Dependencies:** 1
    - [x] 5.1: Create `backend/app/models/base.py` with a shared SQLAlchemy `Base` class.
    - [x] 5.2: Implement `Word` model in `backend/app/models/word.py` with fields: `id` (PK), `text` (String), and `ipa` (JSON).
    - [x] 5.3: Define `WordResponse` Pydantic schema in `backend/app/schemas/word.py`.
    - [x] 5.4: Run `make test` — `test_models.py` and `test_schemas.py` must be green.

### [Task 6] Dictionary Service
* **ID:** 6 | **Dependencies:** 5
    - [x] 6.1: Create `backend/app/services/dictionary_service.py` and implement `get_all_words()`, `get_word_by_id()`, and `seed_dictionary_from_json()` with the minimal logic to pass all tests in `test_dictionary_service.py`.
    - [x] 6.2: Run `make test` — `test_dictionary_service.py` must be green.

### [Task 7] Router & CLI seed
* **ID:** 7 | **Dependencies:** 6
    - [x] 7.1: Create `backend/app/api/v1/dictionary.py` with `GET /words` and `GET /words/{id}` route handlers that delegate to the service layer.
    - [x] 7.2: Register the dictionary router in `backend/main.py`.
    - [x] 7.3: Create `backend/scripts/seed_db.py` to run `seed_dictionary_from_json` using a standalone async session.
    - [x] 7.4: Add a `seed` target to the root `Makefile` to run the script inside the Docker container.
    - [x] 7.5: Run `make test` — full suite must be green with no regressions.
