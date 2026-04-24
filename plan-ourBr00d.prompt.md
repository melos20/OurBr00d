## Plan: Zero-Cloud Our Br00d Local Deployment

Design a Mac Studio-first, zero-cloud, low-latency dual-agent architecture and produce architecture.md that preserves RGP immersion while replacing cloud STT/LLM/TTS with local inference. The approach uses a modular MIC->SPEAKER pipeline, deterministic orchestration with dual sequential responders, persistent Br00d growth across days, and a staged ChromaDB-to-FAISS memory evolution path.

**Steps**
1. Phase 1 - Baseline Local Audio Loop (blocks all later phases)
   - Specify the full modular dataflow from MIC to SPEAKER: capture (CoreAudio/AVAudioEngine), resample, VAD, AEC, streaming STT, orchestration, LLM routing, memory lookup, streaming TTS, playback, sync, CTRL kill-switch.
   - Define state-machine transitions with interruption semantics: LISTENING -> THINKING -> SPEAKING, with full-duplex interrupt-as-turn behavior that atomically halts playback/generation and starts a new turn.
   - Set explicit latency budgets per stage and end-to-first-audio target (<1s): VAD endpoint, STT partial/final, routing+RAG, first token, TTFA.
2. Phase 2 - Local Model/Runtime Selection (depends on 1)
   - Lock Mac Studio-first runtime stack: Metal acceleration, GGUF quantized models via Ollama/llama.cpp.
   - Define persona-specific model roles and quantization tiers:
     - M0ther: stable authoritative guide (Llama 3.1 8B Q5_K/Q6_K).
     - Br00d: evolving expressive companion (Mistral-Nemo 12B Q4_K/Q5_K).
   - Define STT/TTS choices and fallback ladder:
     - STT baseline: Whisper local streaming path; low-latency candidate: Moonshine (benchmark gate).
     - TTS primary/fallback: XTTS (expressive) and Piper (latency resilience), with persona voice mapping and TTFA thresholds.
3. Phase 3 - Dual-Agent Orchestration and Memory Growth (depends on 1, parallel with parts of 2)
   - Formalize orchestrator arbitration for dual sequential responders (M0ther then Br00d, with optional skip based on intent confidence and latency budget).
   - Define shared blackboard/state stores (session log + world state + turn metadata) and write-order guarantees to avoid race conditions.
   - Implement Br00d cross-day growth policy: daily summarization -> persistent developmental profile -> next-day boot injection.
   - Define local RAG progression:
     - Phase A: ChromaDB for velocity and metadata-rich iteration.
     - Phase B: FAISS + SQLite metadata for lower-latency scaling once retrieval behavior stabilizes.
   - Specify retrieval policy: hybrid semantic + recency weighting, persona-conditioned filtering, conflict handling for contradictory memory snippets.
4. Phase 4 - Risk Controls and Operational Hardening (depends on 1-3)
   - VRAM/unified-memory controls: model residency policy, context caps, quantization downgrade tiers, emergency single-responder mode.
   - Thermal controls for exhibition runtime: telemetry thresholds, adaptive degradation policy, scheduling to avoid sustained peak load.
   - Audio-loop mitigation: WebRTC AEC reference path, self-voice rejection guard, speaker ducking, and half-duplex failsafe trigger conditions.
   - Zero-cloud guarantees: network isolation test protocol and dependency audit to verify no external API calls during active sessions.
5. Phase 5 - Author architecture.md (depends on 1-4)
   - Produce architecture.md with exactly these sections:
     1) Modular Pipeline (MIC->SPEAKER with concrete local tools),
     2) Technical Rationale (model/runtime choices tied to M0ther/Br00d personas),
     3) Risks & Mitigation (VRAM, thermal, audio feedback),
     4) Unresolved Questions (hardware envelope details, multi-agent state edge cases),
     5) Next Steps (phased implementation roadmap).
   - Ensure the narrative lens is explicit: M0ther as authoritative guide, Br00d as evolving AI baby, memory as developmental continuity mechanism.
6. Phase 6 - Verification and Readiness Review (depends on 5)
   - Define measurable acceptance tests:
     - End-to-first-audio latency,
     - Interrupt correctness under duplex speech,
     - Memory continuity across day boundary,
     - Persona consistency under sequential dual responses,
     - Soak stability over exhibition-length runtime.
   - Define dry-run checklist for on-site deployment and rollback conditions.

**Relevant files**
- `/Users/melihkoc/Desktop/HM/8.Semester/OurBr00d/background_info/challenge.md` — authoritative challenge scope and success criteria for zero-cloud local loop.
- `/Users/melihkoc/Desktop/HM/8.Semester/OurBr00d/architecture_gemini.md` — prior architecture direction, model candidates, and unresolved constraints to refine.
- `/Users/melihkoc/Desktop/HM/8.Semester/OurBr00d/architecture.md` — target architecture document to create in implementation mode.

**Verification**
1. Confirm architecture.md includes all five required sections and a concrete MIC->SPEAKER local toolchain.
2. Validate latency budget feasibility on Mac Studio with fixed scripted utterance tests (quiet/noisy environment variants).
3. Validate full-duplex interrupt-as-turn behavior with barge-in tests during both M0ther and Br00d speech.
4. Validate dual sequential response policy against mixed-intent prompts and enforce max response-time budget.
5. Validate Br00d growth continuity using day-boundary simulation (archive, summarize, reboot, recall).
6. Validate zero-cloud operation with outbound network blocked and runtime logs confirming no external endpoints.
7. Run a multi-hour soak test and verify thermal and memory-pressure degradation behavior remains within SLO.

**Decisions**
- Confirmed: Mac Studio (Apple Silicon) as primary deployment target.
- Confirmed: Full-duplex interrupt-as-turn semantics.
- Confirmed: Br00d evolves across days (developmental continuity required).
- Confirmed: Dual sequential responders are allowed per turn.
- Confirmed: RAG backend path is hybrid (start ChromaDB, optimize toward FAISS when stable).
- Included scope: Architecture and implementation roadmap document for local deployment.
- Excluded scope: Source-code implementation, model fine-tuning, and infrastructure automation details.

**Further Considerations**
1. Sequential-response guardrail recommendation: enforce dynamic timeout so Br00d follow-up is skipped when turn latency threatens immersion.
2. Memory safety recommendation: define redaction/retention policy for visitor data before persistent storage.
3. Deployment readiness question: confirm exact Mac Studio SKU (RAM size, storage, cooling context) to finalize quantization limits and parallelism headroom.
