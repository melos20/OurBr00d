from __future__ import annotations

import argparse

import uvicorn

from tts_benchmark.api.app import create_app
from tts_benchmark.ui.gradio_app import build_interface


def main() -> None:
    parser = argparse.ArgumentParser(description="TTS benchmark runtime")
    parser.add_argument("--mode", choices=["api", "ui"], default="api")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--api-base", default="http://127.0.0.1:8000")
    args = parser.parse_args()

    if args.mode == "api":
        app = create_app()
        uvicorn.run(app, host=args.host, port=args.port or 8000)
        return

    demo = build_interface(api_base=args.api_base)
    demo.launch(server_name=args.host, server_port=args.port or 7860)


if __name__ == "__main__":
    main()
