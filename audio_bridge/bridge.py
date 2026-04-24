import asyncio
import websockets
import pyaudio
import numpy as np
import json
import wave
import io
from silero_vad import load_silero_vad, VADIterator

# Configuration
WS_URL = "ws://localhost:5000/ws"
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 512  # Silero VAD prefers 512, 1024, or 1536 chunks

async def audio_bridge():
    p = pyaudio.PyAudio()
    
    # Load Silero VAD
    model = load_silero_vad()
    vad_iterator = VADIterator(model, sampling_rate=RATE)
    
    # Input stream (Mic)
    in_stream = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)
    
    # Output stream (Speaker)
    out_stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)

    print(f"Connecting to {WS_URL}...")
    async with websockets.connect(WS_URL) as websocket:
        print("Connected! Start speaking...")
        
        audio_buffer = []
        is_active = False

        try:
            while True:
                # 1. Read Mic
                data = in_stream.read(CHUNK, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16)
                
                # 2. Silero VAD Detection
                # Normalize to float32 between -1 and 1
                audio_float32 = audio_data.astype(np.float32) / 32768.0
                speech_dict = vad_iterator(audio_float32, return_seconds=True)

                if speech_dict:
                    if "start" in speech_dict:
                        print("User started speaking...")
                        is_active = True
                        audio_buffer = [data]
                    elif "end" in speech_dict and is_active:
                        print("User finished speaking. Sending to AI...")
                        full_audio = b"".join(audio_buffer)
                        await websocket.send(full_audio)
                        
                        # Reset for next turn
                        audio_buffer = []
                        is_active = False
                
                if is_active:
                    audio_buffer.append(data)

                # 3. Check for AI Responses (Non-blocking)
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=0.001)
                    if isinstance(message, bytes):
                        # Received raw audio from TTS
                        out_stream.write(message)
                    else:
                        # Received JSON (metadata)
                        resp = json.loads(message)
                        print(f"[{resp.get('persona', 'AI')}]: {resp.get('text', '')}")
                except asyncio.TimeoutError:
                    pass
                except Exception as e:
                    print(f"Error receiving: {e}")

        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            in_stream.stop_stream()
            in_stream.close()
            out_stream.stop_stream()
            out_stream.close()
            p.terminate()

if __name__ == "__main__":
    asyncio.run(audio_bridge())
