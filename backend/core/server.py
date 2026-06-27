from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.database.setup import engine
from core.exceptions.handlers import add_exception_handlers
from core.fastapi.middlewares.response_logger import ResponseLoggerMiddleware

from api.hubs import router as hubs_router
from api.packages import router as packages_router
from api.routes import router as routes_router
from api.vehicles import router as vehicles_router

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage the FastAPI application lifecycle.

    On startup the async engine is already initialised by the module-level
    import of ``core.database.setup``. On shutdown the connection pool is
    disposed gracefully.
    """
    yield

    await engine.dispose()
    logging.getLogger("fasttrack").info("Database connections closed.")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance.

    Registers CORS middleware, the HTTP response logger, custom exception
    handlers, and all API routers.

    Returns:
        A fully configured FastAPI application ready to serve requests.
    """
    app = FastAPI(
        title="FastTrack API",
        description="Motor de Roteirização Multi-Objetivo",
        version="0.1.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(ResponseLoggerMiddleware)

    add_exception_handlers(app)

    app.include_router(packages_router)
    app.include_router(vehicles_router)
    app.include_router(hubs_router)
    app.include_router(routes_router)

    return app


app = create_app()
