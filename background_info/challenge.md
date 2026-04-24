CHALLENGE 1 LOCAL DEPLOYMENT > QUESTION
How do we deploy the entire agent pipeline locally, removing all cloud dependencies?
> SCOPE
Replace ElevenLabs STT with local whisper
Replace cloud LLM (llama.cpp, vLLM, Ollama) Replace cloud TTS (Coqui, XTTS, Piper, fish-speech) Maintain real-time bidirectional audio pipeline Handle hardware constraints (GPU, RAM, latency)
> SUCCESS CRITERIA
Full conversation loop on local hardware No external API calls during a session


--------

Cloud-Dependent Pipeline Architecture

1. Input Stage (Capture & Pre-processing)

MIC (Microphone): The physical point of audio entry.

RESAMPLE: Audio normalization and sample rate conversion to match the requirements of the downstream STT engine.

2. Transport Stage

WEBSOCKET: A persistent, bidirectional connection used to stream raw audio data to the cloud and receive processed text/audio back with low latency.

3. Intelligence Stage (The "Brain")

STT (Speech-to-Text): Converts the resampled audio stream into a text string (currently a cloud service like Whisper API or ElevenLabs STT).

LLM (Large Language Model): The core reasoning engine that processes the transcribed text and generates a response.

RAG (Retrieval-Augmented Generation): A bridge between the LLM and external data/installation lore, ensuring the AI has context-specific knowledge about the Our Br00d universe.

4. Synthesis & Persistence Stage

TTS (Text-to-Speech): Converts the LLM's text output into a synthetic voice (currently a cloud service like ElevenLabs).

SPEAKER: The physical point of audio output for the visitor.

CTRL (Control): The master logic gate or "kill switch" that manages the state transitions of the entire pipeline.

5. Output Stage (Playback & Control)

ECHO: Likely refers to Echo Cancellation or a feedback loop to prevent the AI from "hearing" its own voice through the microphone.

MEMORY: Stores conversation history and state, allowing the LLM to recall previous interactions within the session.

SYNC: Ensures the generated audio and any visual/robotic components are aligned in time.

CTRL (Control): The master logic gate or "kill switch" that manages the state transitions of the entire pipeline.

Current Architecture:
┌─────────────────────────────────────────────────────────────────────┐
│  mother.py                    brood.py                              │
│  ─────────────                ─────────                            │
│  • ElevenLabs TTS             • ElevenLabs TTS                      │
│  • ElevenLabs KB sync         • Stateless                            │
│  • Cloud LLM                  • Cloud LLM                           │
│  • Plaintext memory           • Session-scoped                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Cloud APIs     │
                    │  (ElevenLabs)   │
                    └─────────────────┘