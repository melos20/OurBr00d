import uvicorn
from fastapi import FastAPI
import gradio as gr
from src.ui.app import app as gradio_app
from src.api.routes import router

app = FastAPI(title="TTS Benchmark Tool")

# Include API Router
app.include_router(router)

# Mount Gradio sub-app at / UI path
app = gr.mount_gradio_app(app, gradio_app, path="/")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)