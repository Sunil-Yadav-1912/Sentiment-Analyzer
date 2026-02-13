"""
DistilBERT Sentiment Analysis API - Main Entry Point

This is the main entry point for the FastAPI sentiment analysis application.
Run this file to start the server.

Usage:
    python main.py
"""

import uvicorn
from app import app
from app.core.config import settings


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
