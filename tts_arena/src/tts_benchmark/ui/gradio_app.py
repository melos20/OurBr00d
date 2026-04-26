from __future__ import annotations

import json

import gradio as gr
import httpx


def build_interface(api_base: str) -> gr.Blocks:
    client = httpx.Client(base_url=api_base, timeout=30.0)

    def refresh_models() -> tuple[list[dict], str]:
        try:
            # Use a very short timeout for startup/refresh to avoid hanging the UI
            response = client.get("/v1/models", timeout=2.0)
            response.raise_for_status()
            models = response.json()["models"]
            first = models[0]["model_key"] if models else ""
            return models, first
        except (httpx.HTTPError, httpx.TimeoutException):
            print("Note: Could not connect to TTS API. Please ensure the API is running (mode --api).")
            return [], ""

    def model_choices(models: list[dict]) -> list[str]:
        return [m["model_key"] for m in models]

    def voice_choices(models: list[dict], model_key: str) -> tuple[list[str], str]:
        for model in models:
            if model["model_key"] == model_key:
                voices = model.get("voices", [])
                return voices, (voices[0] if voices else "")
        return [], ""

    def run_synthesis(
        text: str,
        model_key: str,
        voice_key: str,
        speed: float,
        settings_json: str,
    ) -> tuple[str | None, str, str]:
        if not model_key:
            raise ValueError("No model selected. Ensure the API is running and click Refresh models.")

        settings = {}
        if settings_json.strip():
            settings = json.loads(settings_json)
            if not isinstance(settings, dict):
                raise ValueError("settings JSON must be an object")

        payload = {
            "text": text,
            "model_key": model_key,
            "voice_key": voice_key or None,
            "speed": speed,
            "settings": settings,
        }
        try:
            response = client.post("/v1/synthesize", json=payload, timeout=60.0)
            response.raise_for_status()
            body = response.json()
        except httpx.HTTPError as exc:
            raise RuntimeError(f"API request failed: {exc}") from exc

        return body["audio_path"], body["run_id"], json.dumps(body["metadata"], indent=2)

    def submit_evaluation(
        run_id: str,
        latency: int,
        naturalness: int,
        tone_quality: int,
        stability: int,
        reviewer_note: str,
    ) -> str:
        payload = {
            "run_id": run_id,
            "latency_rating": latency,
            "naturalness_rating": naturalness,
            "tone_quality_rating": tone_quality,
            "stability_rating": stability,
            "reviewer_note": reviewer_note or None,
        }
        try:
            response = client.post("/v1/evaluations", json=payload, timeout=10.0)
            response.raise_for_status()
            return json.dumps(response.json(), indent=2, default=str)
        except httpx.HTTPError as exc:
            raise RuntimeError(f"API request failed: {exc}") from exc

    def fetch_evaluation(evaluation_id: str) -> str:
        try:
            response = client.get(f"/v1/evaluations/{evaluation_id}", timeout=10.0)
            response.raise_for_status()
            return json.dumps(response.json(), indent=2, default=str)
        except httpx.HTTPError as exc:
            raise RuntimeError(f"API request failed: {exc}") from exc

    def refresh_models_update() -> tuple[gr.update, gr.update]:
        models, selected_model = refresh_models()
        voices, selected_voice = voice_choices(models, selected_model)
        return (
            gr.update(choices=model_choices(models), value=selected_model),
            gr.update(choices=voices, value=selected_voice),
        )

    def update_voice_for_model(model_key: str) -> gr.update:
        models, _ = refresh_models()
        voices, selected_voice = voice_choices(models, model_key)
        return gr.update(choices=voices, value=selected_voice)

    initial_models, initial_selected_model = refresh_models()
    initial_model_choices = model_choices(initial_models)
    initial_voice_choices, initial_selected_voice = voice_choices(initial_models, initial_selected_model)

    with gr.Blocks(title="TTS Benchmark") as demo:
        gr.Markdown("# TTS Benchmark and Evaluation")

        with gr.Tab("Generate"):
            gr.Markdown("Start the API first (`--mode api`) and then click **Refresh models**.")
            text = gr.Textbox(label="Prompt", lines=4)
            model_key = gr.Dropdown(label="Model", choices=initial_model_choices, value=initial_selected_model)
            voice_key = gr.Dropdown(
                label="Voice",
                choices=initial_voice_choices,
                value=initial_selected_voice,
            )
            speed = gr.Slider(label="Speed", minimum=0.5, maximum=2.0, value=1.0, step=0.1)
            settings_json = gr.Textbox(
                label="Model settings JSON",
                lines=4,
                value='{"gain": 0.2}',
            )
            refresh_btn = gr.Button("Refresh models")
            generate_btn = gr.Button("Generate")
            audio = gr.Audio(label="Output audio", type="filepath")
            run_id = gr.Textbox(label="Run ID")
            metadata = gr.Code(label="Metadata", language="json")

            refresh_btn.click(
                fn=refresh_models_update,
                outputs=[model_key, voice_key],
            )
            model_key.change(fn=update_voice_for_model, inputs=[model_key], outputs=[voice_key])

            generate_btn.click(
                fn=run_synthesis,
                inputs=[text, model_key, voice_key, speed, settings_json],
                outputs=[audio, run_id, metadata],
            )

        with gr.Tab("Evaluate"):
            eval_run_id = gr.Textbox(label="Run ID")
            latency = gr.Slider(label="Latency", minimum=1, maximum=5, value=3, step=1)
            naturalness = gr.Slider(label="Naturalness", minimum=1, maximum=5, value=3, step=1)
            tone_quality = gr.Slider(label="Tone Quality", minimum=1, maximum=5, value=3, step=1)
            stability = gr.Slider(label="Stability", minimum=1, maximum=5, value=3, step=1)
            note = gr.Textbox(label="Reviewer note", lines=2)
            submit_btn = gr.Button("Submit evaluation")
            eval_result = gr.Code(label="Saved evaluation", language="json")

            submit_btn.click(
                fn=submit_evaluation,
                inputs=[eval_run_id, latency, naturalness, tone_quality, stability, note],
                outputs=[eval_result],
            )

        with gr.Tab("Retrieve"):
            evaluation_id = gr.Textbox(label="Evaluation ID")
            retrieve_btn = gr.Button("Fetch")
            retrieve_output = gr.Code(label="Evaluation details", language="json")
            retrieve_btn.click(fn=fetch_evaluation, inputs=[evaluation_id], outputs=[retrieve_output])

    return demo
