# TTS Benchmark Tool Quickstart

## Installation
1. Ensure you have Python 3.10+ installed.
2. Clone or access the `001-tts-benchmark-tool` branch.
3. Install dependencies:
   ```bash
   pip install -r services/tts_benchmark/requirements.txt
   ```

## Running the Tool
Start the standalone FastAPI server, which mounts the Gradio UI:

```bash
uvicorn services.tts_benchmark.main:app --host 0.0.0.0 --port 8000
```

## Accessing the Interface
1. **Gradio UI:** Open your browser and navigate to `http://localhost:8000/`.
2. **API Documentation:** The Swagger docs are available at `http://localhost:8000/docs`.

### API Usage Example
Generate audio directly via curl without using the browser:
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/generate' \
  -H 'accept: audio/wav' \
  -H 'Content-Type: application/json' \
  -d '{
  "text": "This is a benchmark test.",
  "model_id": "kokoro-82m"
}' --output test_audio.wav
```
