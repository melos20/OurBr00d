# OURBROOD Workshop – Technical Development of Agentic AI in Artistic Research

## Workshop Overview

**Project Workshop – Session 1: Limitations & Challenges**  
**Date:** March 25-26, 2025 | **Time:** 10am-4pm

---

### Assessment
- Group technical project + colloquium
- Group documentation (max. 10 pages)

---

## Project Context: Our Br00d – AI as Social and Cultural Actor

### What is OUR BROOD?

An experimental participatory installation by **OMSK Social Club** investigating how AI might evolve if 'raised' through radical care, relationality, and collective responsibility. AI as a social and cultural actor whose behavior emerges through socialization between human and non-human agents.

### The Encounter
Guided role-play informed by psychodrama and social design. Participants take up roles to explore speculative narratives around the ideas of living with machines.

### The Agents

#### MOTHER
- Multilingual caretaking entity
- Cloud-based voice agent
- Participates in the psychodrama sessions
- Features: Persistent long-term memory, web search, echo suppression, mode switching

#### BR00D
- A developing agentic being
- Always-on, wake-word activated
- Multi-channel audio
- Remembers words from audience interactions across sessions

---

## Course Objective

### The Technical Mission
Migrate OUR BROOD from proprietary cloud services to an **open-source, locally deployable (on-premise) architecture**. Not purely technical optimization – a core artistic and ethical intervention.

### Why It Matters
- Latency, data sovereignty, transparency, scalability are inseparable from the inquiry into care and agency
- Open-source as practical strategy and political gesture

### Your Role
- Work directly with the agent architecture
- Collaborate with OMSK Social Club
- Reflect on how architectures encode social assumptions and relational models

---

## Current Architecture

### Current System Stack

#### MOTHER.PY (1271 Lines)
- ElevenLabs Conversational AI API
- WebSocket bidirectional audio
- Cloud LLM + TTS pipeline
- RAG via Knowledge Base API
- Persistent memory (plaintext + KB sync)
- Echo suppression (agent/user)
- ACTIVE/LISTENING mode (hotkeys)
- Supervisor process (auto-restart)

#### BR00D.PY (693 Lines)
- ElevenLabs Conversational AI API
- Wake-word activation ('br00d')
- 15-second speech gate
- Multi-channel audio routing
- VAD-based idle listen
- Supervisor process (auto-restart)

### Cloud Dependencies
- ElevenLabs API
- LLM reasoning (cloud-hosted)
- Text-to-speech synthesis
- Speech-to-text transcription
- Knowledge Base (RAG storage)
- Agent configuration + tools
- DuckDuckGo Search API (web search)

### Local Components
- PyAudio (mic/speaker I/O)
- pynput (hotkey listener)
- Memory file (mother_memory.txt)
- Audio config (JSON device map)
- python-dotenv (.env config)

---

## Current Limitations

### Limitations – MOTHER.PY

#### Interaction Quality
- Time lag of response
- Cloud round-trip: mic → STT → LLM → TTS → speaker
- Noticeable latency breaks conversational flow
- Manual ACTIVE/LISTENING mode switching
- Operator must toggle via hotkeys
- No automatic turn-taking or silence detection

#### Response Diversity
- Responses tend toward uniform length
- Repetition of phrases ('tapestry', etc.)
- Flexible syntax and natural variation lacking
- Sporadic audio drop-outs (WebSocket instability)
- Conversations capped at ~1 hour

#### Character & Agency
- Mother defaults to 'facilitator' role
- Asks questions rather than being asked
- Struggles to leave 'assistant axis' (Liu et al.)
- Prompt + RAG alone may not maintain character integrity across extended roleplay sessions

#### Memory & RAG
- Current RAG system (ElevenLabs KB) is limited
- Flat keyword search over plaintext
- No semantic or embedding-based recall
- Memory context fixed (last 20 lines)
- No episodic or relational memory structure

### Limitations – BR00D.PY

#### Identity & Growth
- What memories did Brood pick up during growth?
- How do past interactions shape personality?
- Currently: simple memory file with saved words
- No structured developmental model or personality evolution mechanism

#### Shared Cloud Constraints
- Same latency issues as Mother
- Cloud STT/LLM/TTS round-trip
- Same character integrity challenges
- Baseline 'assistant personality' bleeds through
- Same session duration limits (~1 hour cap)

---

## Student Challenges – Technical Development Tasks

### Challenge 1 – Local Deployment

#### Question
How do we deploy the entire agent pipeline locally, removing all cloud dependencies?

#### Scope
- Replace ElevenLabs STT with local whisper
- Replace cloud LLM (llama.cpp, vLLM, Ollama)
- Replace cloud TTS (Coqui, XTTS, Piper, fish-speech)
- Maintain real-time bidirectional audio pipeline
- Handle hardware constraints (GPU, RAM, latency)

#### Success Criteria
- Full conversation loop on local hardware
- No external API calls during a session

---

## Learning Outcomes

### After This Workshop You Will Be Able To...

1. **Understand Agentic AI Architecture**
   - LLM dialogue, RAG, voice synthesis, real-time pipelines

2. **Design Open-Source Alternatives**
   - Local deployment, modularity, transparency

3. **Evaluate Infrastructure Decisions**
   - Cloud vs. on-premise, latency, data sovereignty, ethics

4. **Collaborate Across Disciplines**
   - Work alongside artists and researchers

5. **Translate Art Into System Design**
   - How technical choices shape agency and personality

---

## Key Technical Considerations

| Aspect | Current State | Target State |
|--------|---------------|--------------|
| STT | ElevenLabs Cloud API | Local Whisper |
| LLM | Cloud-hosted | llama.cpp / vLLM / Ollama |
| TTS | ElevenLabs Cloud API | Coqui / XTTS / Piper / fish-speech |
| Memory | Plaintext file + KB sync | Structured episodic memory |
| RAG | Flat keyword search | Embedding-based semantic recall |
| Deployment | Cloud-dependent | Fully local/on-premise |
| Latency | High (cloud round-trip) | Optimized (local processing) |
| Data Sovereignty | Low (cloud storage) | High (local control) |

---

*Document generated from OURBROOD Workshop Slides – Session 1: Limitations & Challenges*