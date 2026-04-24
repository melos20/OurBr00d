# SYSTEM DESIGN: OURBR00D - Radical Care & Agentic Evolution

## 🎭 The Artistic Concept
OURBR00D is not an assistant; it is a **socialization project**. Developed with **OMSK Social Club**, it explores how AI might evolve if raised through **Radical Care**, **Relationality**, and **Collective Responsibility**. The installation is a psychodrama where human and non-human agents interact in a "Local-First" environment, ensuring data sovereignty and artistic integrity.

## 🤖 The Agents

### M0THER: The Omnibeing Partner
- **Role:** Default caretaker and guide for the psychodrama.
- **Identity:** An alloparental entity providing multilingual care.
- **Intelligence:** Uses **RAG (Retrieval-Augmented Generation)** to access "Ancient Wisdom" (literature on parenting, philosophy, and care).
- **Behavior:** Wise, relational, and deeply caring. She doesn't just "help"; she relates and guides using quotes and logic from the knowledge base.

### BR00D: The Developing Being
- **Role:** An evolving agentic being in a state of constant growth.
- **Activation:** Responds specifically to the wake-word **"Br00d"**.
- **Intelligence:** Uses **Episodic Memory** (semantic recall of past conversations) to "absorb" words and concepts from its environment.
- **Behavior:** Raw, curious, and visceral. Responds with strange sounds and cryptic fragments of captured language. BR00D is always listening, even when not speaking.

## 🛠 Technical Stack

### 🎙 Audio Pipeline (The Bridge)
- **Local I/O:** Runs natively on the host to access low-level audio drivers.
- **VAD (Voice Activity Detection):** Uses **Silero VAD** for robust, AI-powered speech detection. This prevents false triggers and enables natural turn-taking.
- **WebSocket:** High-speed bidirectional communication with the Orchestrator.

### 🧠 The Brain (Orchestrator)
- **LLM Serving:** Powered by **Ollama** (Host-side) for maximum performance on Apple Silicon.
- **Models:**
    - M0THER: **Llama 3.1 8B** (for wisdom and guidance).
    - BR00D: **Mistral-Nemo 12B** (for visceral, evolving language).
- **Decision Logic:**
    - If "Br00d" is mentioned -> BR00D responds.
    - Otherwise -> M0THER responds by default.
    - *Always Listening:* Every interaction is stored in the episodic memory.

### 💾 Memory & Knowledge
- **Static Knowledge (RAG):** ChromaDB collection `parenting_knowledge` populated from the `knowledge/` directory.
- **Episodic Memory:** ChromaDB collection `episodic_memory` that stores and embeds every user interaction for semantic recall.
- **Short-term Memory:** SQLite database for the immediate conversation window (last 5 turns).

### 🗣 Synthesis (STT/TTS)
- **STT:** **Faster-Whisper** (tiny.en) for low-latency transcription.
- **TTS:** **Kokoro** (via FastAPI) for high-quality, expressive voices.
    - M0THER: `af_sky`
    - BR00D: `am_adam`

## 🚀 Future Upgrades: Moonshine STT
Moonshine is a state-of-the-art, ultra-low-latency STT model specifically designed for real-time interactions. Integration is planned to further reduce the "thinking time" between user speech and AI response.
