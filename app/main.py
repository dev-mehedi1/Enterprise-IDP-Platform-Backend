from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.core.exceptions import setup_exception_handlers

setup_logging()
logger = get_logger(__name__)

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        description="Enterprise Intelligent Document Processing API",
        version="0.1.0",
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # In production, restrict this
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Setup metrics
    Instrumentator().instrument(app).expose(app)
    
    # Setup Exception handlers
    setup_exception_handlers(app)

    @app.on_event("startup")
    async def startup_event():
        logger.info("Starting up IDP Platform Backend...")
        from app.infrastructure.database.init_db import init_db
        await init_db()
        logger.info("MongoDB and Beanie initialized successfully.")

    @app.get("/health")
    async def health_check():
        return {"status": "ok", "service": settings.PROJECT_NAME}

    from app.api.v1.api import api_router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app

app = create_app()
