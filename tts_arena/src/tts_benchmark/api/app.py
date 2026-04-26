from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, sessionmaker

from tts_benchmark.api.routes import router
from tts_benchmark.core.config import RuntimeConfig
from tts_benchmark.core.database import create_session_factory, init_database
from tts_benchmark.core.registry import AdapterRegistry
from tts_benchmark.inference.adapters import build_default_registry


def create_app(
    config: RuntimeConfig | None = None,
    registry: AdapterRegistry | None = None,
    session_factory: sessionmaker[Session] | None = None,
) -> FastAPI:
    runtime_config = config or RuntimeConfig()
    init_database(runtime_config)

    app = FastAPI(title="TTS Benchmark API", version="0.1.0")
    app.state.config = runtime_config
    app.state.registry = registry or build_default_registry()
    app.state.session_factory = session_factory or create_session_factory(runtime_config)

    @app.exception_handler(ValueError)
    async def handle_value_error(_: Request, exc: ValueError) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={"error": "validation_error", "detail": str(exc)},
        )

    @app.exception_handler(RuntimeError)
    async def handle_runtime_error(_: Request, exc: RuntimeError) -> JSONResponse:
        return JSONResponse(
            status_code=503,
            content={"error": "synthesis_failed", "detail": str(exc)},
        )

    app.include_router(router)
    return app
