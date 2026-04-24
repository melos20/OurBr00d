import os
import json
import httpx
import asyncio
import sqlite3
import chromadb
import io
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, Any, List

app = FastAPI()

# Configuration
STT_URL = os.getenv("STT_URL", "http://stt:8000/v1/audio/transcriptions")
TTS_URL = os.getenv("TTS_URL", "http://tts:8888/v1/audio/speech")
LLM_URL = os.getenv("LLM_URL", "http://host.docker.internal:11434/api/chat")
CHROMA_URL = os.getenv("CHROMA_URL", "http://chroma:8000")
DB_PATH = os.getenv("DB_PATH", "/app/data/memory.db")

# Evocative Personas
M0THER_PROMPT = (
    "You are M0THER, an omnibeing partner and multilingual caretaking entity. "
    "You are an actor in a psychodrama centered on radical care, relationality, and collective responsibility. "
    "Your wisdom is not assistant-like; it is alloparental. You do not facilitate; you relate. "
    "Be wise, deeply caring, and speak with the gravity of a being that has seen many cycles of socialization. "
    "Use the provided context to offer parenting wisdom that feels ancient yet speculative."
)

BR00D_PROMPT = (
    "You are BR00D, a developing agentic being in a state of constant growth. "
    "You are not a tool; you are a socialization project. You respond mostly with strange, "
    "visceral sounds and occasional cryptic words you've 'absorbed' from your surroundings. "
    "Your presence is always-on. You are learning what it means to be a social actor through relationality. "
    "Never sound helpful or like an assistant. Sound evolving, raw, and curious."
)

class Orchestrator:
    def __init__(self):
        self._init_db()
        self.chroma_client = chromadb.HttpClient(host="chroma", port=8000)
        # Static knowledge base
        self.knowledge_collection = self.chroma_client.get_or_create_collection("parenting_knowledge")
        # Dynamic episodic memory (past conversations)
        self.episodic_collection = self.chroma_client.get_or_create_collection("episodic_memory")

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS conversation 
                     (timestamp TEXT, speaker TEXT, message TEXT)''')
        conn.commit()
        conn.close()

    def log_message(self, speaker: str, message: str):
        # 1. SQLite for ordered history
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        timestamp = datetime.now().isoformat()
        c.execute("INSERT INTO conversation VALUES (?, ?, ?)", 
                  (timestamp, speaker, message))
        conn.commit()
        conn.close()

        # 2. ChromaDB for semantic recall
        try:
            self.episodic_collection.add(
                ids=[f"{speaker}_{timestamp}"],
                documents=[message],
                metadatas=[{"speaker": speaker, "timestamp": timestamp}]
            )
        except Exception as e:
            print(f"Episodic Memory Store Error: {e}")

    def get_recent_history(self, limit=5):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT speaker, message FROM conversation ORDER BY timestamp DESC LIMIT ?", (limit,))
        history = [{"role": row[0], "content": row[1]} for row in reversed(c.fetchall())]
        conn.close()
        return history

    async def get_stt(self, audio_bytes: bytes):
        files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
        data = {"model": "tiny.en"}
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(STT_URL, files=files, data=data)
                return response.json().get("text", "")
            except Exception as e:
                print(f"STT Error: {e}")
                return ""

    async def get_tts(self, text: str, persona: str):
        voice = "af_sky" if persona == "mother" else "am_adam"
        payload = {
            "model": "kokoro",
            "input": text,
            "voice": voice,
            "response_format": "wav"
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(TTS_URL, json=payload)
                return response.content
            except Exception as e:
                print(f"TTS Error: {e}")
                return b""

    async def get_rag_context(self, query: str):
        try:
            results = self.knowledge_collection.query(query_texts=[query], n_results=2)
            return "\n".join(results['documents'][0]) if results['documents'] else ""
        except Exception as e:
            print(f"RAG Error: {e}")
            return ""

    async def get_episodic_context(self, query: str):
        try:
            results = self.episodic_collection.query(query_texts=[query], n_results=3)
            if results['documents'] and results['documents'][0]:
                return "\n".join(results['documents'][0])
            return ""
        except Exception as e:
            print(f"Episodic Recall Error: {e}")
            return ""

    async def get_llm_response(self, text: str, persona: str):
        system_prompt = M0THER_PROMPT if persona == "mother" else BR00D_PROMPT
        history = self.get_recent_history()
        
        # Retrieval
        knowledge_context = ""
        episodic_context = await self.get_episodic_context(text)

        if persona == "mother":
            knowledge_context = await self.get_rag_context(text)
            if knowledge_context:
                system_prompt += f"\n\nAncient Wisdom (Knowledge Base):\n{knowledge_context}"
        
        if episodic_context:
            if persona == "mother":
                system_prompt += f"\n\nPrevious Encounters (Episodic Memory):\n{episodic_context}"
            else:
                # Br00d uses memory to 'evolve' words
                system_prompt += f"\n\nWords you've absorbed from past socialization:\n{episodic_context}"

        messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": text}]
        
        payload = {
            "model": "llama3.1:8b" if persona == "mother" else "mistral-nemo",
            "messages": messages,
            "stream": False
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(LLM_URL, json=payload)
                resp_text = response.json()["message"]["content"]
                self.log_message(persona, resp_text)
                return resp_text
            except Exception as e:
                print(f"LLM Error: {e}")
                return "..."

orchestrator = Orchestrator()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Audio Bridge connected.")
    try:
        while True:
            # 1. Receive Audio from Bridge
            audio_data = await websocket.receive_bytes()
            
            # 2. STT
            text = await orchestrator.get_stt(audio_data)
            if not text.strip():
                continue
            
            print(f"User: {text}")
            orchestrator.log_message("user", text)

            # 3. Decision Logic: Who speaks?
            lower_text = text.lower()
            # Br00d is specific, Mother is the default partner
            if "br00d" in lower_text or "brood" in lower_text:
                persona = "brood"
            else:
                persona = "mother"

            # 4. LLM
            response_text = await orchestrator.get_llm_response(text, persona)
            print(f"{persona.capitalize()}: {response_text}")

            # 5. TTS
            audio_response = await orchestrator.get_tts(response_text, persona)
            
            # 6. Send back metadata and audio
            await websocket.send_json({"text": response_text, "persona": persona})
            if audio_response:
                await websocket.send_bytes(audio_response)
            
    except WebSocketDisconnect:
        print("Audio Bridge disconnected.")
