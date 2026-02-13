from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.model_manager import model_manager
from app.api import router
from app.middleware.rate_limiter import RateLimiter
from app.middleware.request_logger import RequestLoggerMiddleware

# Setup logging
logger = setup_logging(settings.LOG_LEVEL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown events"""
    # Startup
    logger.info("Starting up DistilBERT Sentiment Analysis API...")
    logger.info(f"Configuration: {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Device preference: {settings.DEVICE}")
    
    try:
        # Load ML model
        model_manager.load_model()
        logger.info("Application startup complete!")
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise
    
    yield  # Application runs here
    
    # Shutdown
    logger.info("Shutting down application...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    app = FastAPI(
        title=settings.APP_NAME,
        description="A professional sentiment analysis API using DistilBERT transformer model",
        version=settings.APP_VERSION,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add request logger middleware
    app.add_middleware(RequestLoggerMiddleware)
    
    # Add rate limiter middleware (if enabled)
    if settings.RATE_LIMIT_ENABLED:
        app.add_middleware(
            RateLimiter,
            requests_limit=settings.RATE_LIMIT_REQUESTS,
            window_seconds=settings.RATE_LIMIT_WINDOW
        )
        logger.info(
            f"Rate limiting enabled: {settings.RATE_LIMIT_REQUESTS} requests "
            f"per {settings.RATE_LIMIT_WINDOW} seconds"
        )
    
    # Include API router
    app.include_router(router)
    
    return app


# Create app instance
app = create_app()
