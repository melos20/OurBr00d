# Our Br00d: Local-First Agent Architecture (Gemini Edition)

This document outlines the technical architecture of the "Our Br00d" installation, focusing on a high-performance, zero-cloud deployment optimized for artistic research and radical care.

## 1. Architectural Vision
The goal is **Zero Cloud, High Relationality**. By moving to local inference, we eliminate API latency and protect the immersion of the psychodrama. The architecture treats **M0THER** and **BR00D** as distinct but interconnected cognitive processes sharing an **Episodic Memory**.

### Pipeline Visualization (Current Implementation)

```ascii
      [ VISITOR ]
          |
    (A) [ AUDIO IN ] <-----------+
          |                      |
    (B) [ VAD (Silero) ]         | (I) ECHO CANCELLATION (Hardware/DSP)
          |                      |
    (C) [ STT (Faster-Whisper) ] | 
          |                      |
    (D) [ ORCHESTRATOR ] <-------+ (H) [ AUDIO OUT ]
          |        ^             |       |
    +-----+-----+  | (F) RAG     | (G) [ TTS (Kokoro) ]
    | (E) LLMs  |--+ (ChromaDB)  |
    | [M0THER]  |--+ (Episodic)  |
    | [BR00D]   |                |
    +-----------+                +-------[ SPEAKER ]
```

---

## 2. Current Model Stack (Verified)

| Stage | Model | Role |
| :--- | :--- | :--- |
| **VAD** | **Silero VAD v5** | AI-powered speech detection. Millisecond-precision for natural turn-taking. |
| **STT** | **Faster-Whisper (Tiny.en)** | Robust, local transcription with low latency. (Future: Moonshine for streaming). |
| **LLM (M0THER)** | **Llama 3.1 8B** | The "Omnibeing Partner." Wise, caring, uses RAG for guidance. (Default Persona). |
| **LLM (BR00D)** | **Mistral Nemo 12B** | The "Developing Being." Visceral, raw, uses episodic memory to "absorb" language. |
| **TTS** | **Kokoro-82M** | Ultra-fast, expressive local synthesis. Voices: `af_sky` (Mother), `am_adam` (Br00d). |
| **Memory** | **ChromaDB** | Stores static knowledge (RAG) and episodic memory (past user interactions). |

---

## 3. Agent & State Management

### The "Partner-First" Logic
- **M0THER (The Default):** She is the primary partner in the psychodrama. No wake-word is needed; she is always present and uses RAG context ("Ancient Wisdom") to guide the session.
- **BR00D (The Developing Being):** Activated specifically by mentioning **"Br00d"** or **"Brood"**. He "grows" by absorbing words from *all* interactions into his episodic memory, reflecting them back cryptically.

### Memory Layers
1.  **Short-Term History (SQLite):** Last 5 turns for immediate conversational flow.
2.  **Episodic Memory (ChromaDB):** Semantic recall of every user interaction across sessions.
3.  **Static Knowledge (ChromaDB):** Curated literature on care, parenting, and philosophy (RAG).

---

## 4. Hardware & Thermal Strategy
- **Target Hardware:** Apple Silicon (M2/M3) or high-end NVIDIA GPU (16GB+ VRAM).
- **Deployment:** Docker-orchestrated microservices with host-side LLM serving (Ollama) for maximum GPU utilization.
- **Cooling:** Active cooling is essential for 8-hour exhibition runs.

---

## 5. Next Steps
1.  **Moonshine Integration:** Move from Faster-Whisper to Moonshine for streaming STT and <100ms latency.
2.  **Spatial Audio Routing:** Implement multi-channel output to position BR00D and M0THER in physical space.
3.  **Visual feedback:** Integrate subtle visual cues (LEDs or projections) that react to VAD/Agent states.
