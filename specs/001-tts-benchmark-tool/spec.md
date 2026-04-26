# Feature Specification: TTS Benchmark Tool

**Feature Branch**: `001-tts-benchmark-tool`  
**Created**: 2026-04-24  
**Status**: Draft  
**Input**: User description: "in this project the overall goal is to create an on prem pipeline, where we also tweak on things like tts or stt. To be able to "benchamark" different models against each other, i would like to buil a small tool, which might also run independently. Lets first only focus on the TTS part This means, i want an UI, where i might have a selectoin of e.g. 5 text and i can paste in something myself. Then there should be model selection a,b,c... For each model there should be an evaluation such as: Fast/Slow Response, human like, warm tone, no weird hiccups etc. I want to use models from huggingface on local hardware. would it make sense to make it accessible via api calls, so that we can include it in the architecture? But it should be able to run independentaly from the rest of the project. Models i am looking into right now are: Kokoro, OmniVoice, OpenMoss and maybe a lightweight qwen model."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Benchmark predefined texts across models (Priority: P1)

Users need to quickly compare how different TTS models handle standard sentences to establish a baseline of quality. They will select from a predefined list of texts, choose a model, generate the audio, and provide qualitative feedback.

**Why this priority**: Core functionality needed to achieve the primary goal of comparing models consistently.

**Independent Test**: Can be fully tested by selecting one of the 5 predefined phrases, running it through a single local model, and playing back the result.

**Acceptance Scenarios**:

1. **Given** the benchmarking UI is open, **When** the user selects a predefined text and a model (e.g., Kokoro) and clicks "Generate", **Then** the local model streams/returns audio playback.
2. **Given** audio generation is complete, **When** the user plays the audio, **Then** they can fill out an evaluation form scoring speed, human-likeness, warmth, and artifacts.

---

### User Story 2 - Benchmark custom text (Priority: P1)

Users need to test models on domain-specific or challenging text that isn't in the predefined list.

**Why this priority**: Essential for testing edge cases or production-like inputs that the models will face in the real pipeline.

**Independent Test**: Can be tested by pasting a custom paragraph into a text area, choosing a model, and verifying that the generated audio correctly matches the custom input.

**Acceptance Scenarios**:

1. **Given** the benchmarking UI, **When** the user pastes custom text into the input field and triggers generation, **Then** the selected model creates accurate audio for the entirety of the custom text.

---

### User Story 3 - API Integration (Priority: P2)

Other parts of the system (the main architecture pipeline) need to programmatically request TTS generation without using the UI.

**Why this priority**: Fulfills the requirement to include the benchmarking tool's capabilities in the broader architecture while maintaining its standalone nature.

**Independent Test**: Can be fully tested by sending an HTTP request (via curl/Postman) with a text payload and receiving a valid audio file response.

**Acceptance Scenarios**:

1. **Given** the tool is running in background/server mode, **When** a valid API request with text and a model identifier is received, **Then** the tool processes the text using the local model and returns an audio file.

### Edge Cases

- What happens if the local hardware lacks the VRAM/RAM to load multiple models sequentially or concurrently?
- How does the system handle extremely long custom texts that exceed the model's context window?
- What happens if the selected model has not been downloaded from HuggingFace yet?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a web-based User Interface for the benchmarking process.
- **FR-002**: System MUST provide a mechanism to select from at least 5 predefined texts.
- **FR-003**: System MUST provide a text input area for users to paste completely custom text.
- **FR-004**: System MUST allow users to select between local HuggingFace TTS models (e.g., Kokoro, OmniVoice, OpenMoss, Qwen).
- **FR-005**: System MUST present an evaluation form for generated audio, capturing scores for: Response Speed, Human-like quality, Warm Tone, and Absence of hiccups.
- **FR-006**: System MUST download and execute the selected HuggingFace models entirely on local hardware.
- **FR-007**: System MUST expose an API endpoint that accepts text and model parameters and returns generated audio.
- **FR-008**: System MUST operate independently without requiring the rest of the main project architecture to be running.
- **FR-009**: System MUST capture evaluation metrics using a 1-5 scale.
- **FR-010**: System MUST persist evaluation results for future comparison. However, generated audio MUST NOT be persisted by default (ephemeral), but the system MUST provide a configurable flag to optionally save the audio to disk if desired.

### Key Entities

- **Model**: Represents a local HuggingFace TTS model with its file paths and configuration.
- **Evaluation**: The user's subjective rating of a specific audio generation (contains scores and selected text/model).
- **Generation Request**: The payload (text + target model) for creating an audio output.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The UI loads successfully in a standard web browser within 2 seconds.
- **SC-002**: Users can toggle between predefined text and custom text seamlessly.
- **SC-003**: Models load and execute locally, producing audible speech with no external cloud dependencies (after initial model pull).
- **SC-004**: The API endpoint responds to valid text requests with corresponding audio data in a standard format (e.g., WAV/MP3).
- **SC-005**: The tool can be started via a single run command, entirely isolated from the main repository's orchestrator or knowledge\_ingest services.

## Assumptions

- Target local hardware has sufficient capacity (CPU/GPU) to run lightweight 80M-100M parameter TTS models.
- The system will use standard, open-source Python web frameworks (e.g., Gradio, Streamlit, or FastAPI/React) for the standalone UI and API, leaving actual framework choice to the implementation phase.
- Model downloads will occur automatically on first use or via a dedicated initialization script.
