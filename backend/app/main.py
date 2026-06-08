from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.db.session import engine
from app.models.hr import Base
from app.monitoring.metrics import metrics_middleware

logger = structlog.get_logger()
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    if settings.environment in {"local", "test"}:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)
    logger.info("service_started", service=settings.app_name, environment=settings.environment)
    yield
    logger.info("service_stopped", service=settings.app_name)


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Enterprise HR workforce intelligence API for Microsoft 365 Copilot agents.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
app.middleware("http")(metrics_middleware)
app.include_router(api_router, prefix=settings.api_prefix)
