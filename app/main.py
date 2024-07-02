from contextlib import asynccontextmanager

import dotenv
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.views import v1_router

# from app.api.v1.views import v1_router
from core.database import init_database_connection
from core.utils import logger
from middleware import ExceptionHandlerMiddleware, LogHandlerMiddleware

dotenv.load_dotenv(".env")


@asynccontextmanager
async def lifespan(_app: FastAPI):  # type: ignore
    """Initialize application repositories."""
    # Initialize database connection
    await init_database_connection(_app)

    logger.info("Startup complete")
    yield
    logger.info("Shutdown complete")


app = FastAPI(
    title="SIGNIT",
    lifespan=lifespan,
)

app.include_router(v1_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ExceptionHandlerMiddleware)
app.add_middleware(LogHandlerMiddleware)
app.add_middleware(CorrelationIdMiddleware)
