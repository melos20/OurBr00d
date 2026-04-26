---
description: "Task list template for feature implementation"
---

# Tasks: TTS Benchmark Tool

**Input**: Design documents from `/specs/001-tts-benchmark-tool/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure for `services/tts_benchmark/` per implementation plan
- [x] T002 Initialize `services/tts_benchmark/requirements.txt` with FastAPI, Gradio, SQLAlchemy, Transformers, PyTorch
- [x] T003 Create `services/tts_benchmark/main.py` entrypoint skeleton
- [x] T004 [P] Setup testing configuration in `services/tts_benchmark/tests/conftest.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create `services/tts_benchmark/src/core/config.py` for environment variables and model paths configuration
- [x] T006 Create `services/tts_benchmark/src/core/database.py` for SQLite connection and sessions setup
- [x] T007 Create `Evaluation` entity in `services/tts_benchmark/src/models/evaluation.py` to persist scores
- [x] T008 [P] Create `TTSModelAdapter` base class interface in `services/tts_benchmark/src/inference/base.py`

**Checkpoint**: Foundation ready - user story implementation can now begin sequence or parallel where possible.

---

## Phase 3: User Story 1 - Benchmark predefined texts across models (Priority P1) 🎯 MVP

**Goal**: Users need to quickly compare how different TTS models handle standard sentences to establish a baseline of quality.

**Independent Test**: Can be fully tested by selecting one of the 5 predefined phrases, running it through a single local model, and playing back the result.

### Implementation for User Story 1

- [x] T009 [P] [US1] Implement Kokoro adapter in `services/tts_benchmark/src/inference/adapters/kokoro.py` using `TTSModelAdapter`
- [x] T010 [P] [US1] Implement alternative model adapter (e.g., OpenMoss/OmniVoice) in `services/tts_benchmark/src/inference/adapters/openmoss.py`
- [x] T011 [US1] Create core generation service function in `services/tts_benchmark/src/inference` to route requests to appropriate adapter
- [x] T012 [US1] Implement UI component for predefined text selection (5 hardcoded options) in `services/tts_benchmark/src/ui/app.py`
- [x] T013 [US1] Implement UI component for model selection dropdown in `services/tts_benchmark/src/ui/app.py`
- [x] T014 [US1] Implement "Generate" button and audio playback component in `services/tts_benchmark/src/ui/app.py` linking to generation service
- [x] T015 [US1] Implement 1-5 scale evaluation form capturing speed, human-like quality, warmth, and hiccups in `services/tts_benchmark/src/ui/app.py`
- [x] T016 [US1] Connect evaluation form submission to insert into SQLite via `services/tts_benchmark/src/models/evaluation.py`
- [x] T017 [US1] Mount Gradio app in `services/tts_benchmark/main.py` within the FastAPI application

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. MVP is achieved!

---

## Phase 4: User Story 2 - Benchmark custom text (Priority P1)

**Goal**: Users need to test models on domain-specific or challenging text that isn't in the predefined list.

**Independent Test**: Can be tested by pasting a custom paragraph into a text area, choosing a model, and verifying that the generated audio correctly matches the custom input.

### Implementation for User Story 2

- [x] T018 [US2] Update `services/tts_benchmark/src/ui/app.py` to add a custom free-form text input area
- [x] T019 [US2] Implement Tabs/Toggles in `services/tts_benchmark/src/ui/app.py` to seamlessly switch between predefined texts and custom input mode
- [x] T020 [US2] Verify inference adapters handle arbitrary custom strings without failures (add length safety bounds if necessary)

**Checkpoint**: Users can now benchmark both predefined and custom texts.

---

## Phase 5: User Story 3 - API Integration (Priority P2)

**Goal**: Other parts of the system (the main architecture pipeline) need to programmatically request TTS generation without using the UI.

**Independent Test**: Can be fully tested by sending an HTTP request (via curl/Postman) with a text payload and receiving a valid audio file response.

### Implementation for User Story 3

- [x] T021 [P] [US3] Define `GenerationRequest` and `GenerationResponse` Pydantic schemas in `services/tts_benchmark/src/api/routes.py` based on `contracts/openapi.yml`
- [x] T022 [P] [US3] Implement `POST /api/v1/generate` endpoint in `services/tts_benchmark/src/api/routes.py` returning synthetic audio
- [x] T023 [P] [US3] Implement `POST /api/v1/evaluations` endpoint in `services/tts_benchmark/src/api/routes.py` 
- [x] T024 [P] [US3] Implement `GET /api/v1/evaluations` endpoint in `services/tts_benchmark/src/api/routes.py`
- [x] T025 [US3] Include the API router into the main FastAPI application in `services/tts_benchmark/main.py`
- [x] T026 [US3] Add API integration tests utilizing TestClient in `services/tts_benchmark/tests/test_api.py`

**Checkpoint**: All user stories should now be independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T027 [P] Implement error catching and UI toast notifications for failed audio generations in `services/tts_benchmark/src/ui/app.py`
- [x] T028 [P] Ensure audio `outputs/` directory logic is configured properly (handling optional persistence configurations)
- [x] T029 Code cleanup and ensuring type hints pass across all modules in `services/tts_benchmark/`
- [x] T030 Validate `services/tts_benchmark` manually works via instructions detailed in `quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2)
- **User Story 2 (P1)**: Can start after US1 is fundamentally working as it builds on the same UI components.
- **User Story 3 (P2)**: Can start right after US1/Foundational, decoupled from US2 since it deals purely with API.

### Parallel Opportunities

- Model Adapters `T009` and `T010` in US1 can be developed simultaneously.
- API endpoints `T021-T024` in US3 can be built independently of US2.
