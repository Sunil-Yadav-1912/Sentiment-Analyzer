"""
Convenient startup script for the Sentiment Analysis API

This script provides a simple way to run the API server with various options.

Usage:
    python run.py                    # Run with default settings
    python run.py --host 127.0.0.1   # Run on localhost only
    python run.py --port 8080        # Run on custom port
    python run.py --no-reload        # Disable auto-reload
"""

import argparse
import uvicorn
from app.core.config import settings


def main():
    parser = argparse.ArgumentParser(
        description="Run the DistilBERT Sentiment Analysis API"
    )
    parser.add_argument(
        "--host",
        type=str,
        default=settings.HOST,
        help=f"Host to bind to (default: {settings.HOST})"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=settings.PORT,
        help=f"Port to bind to (default: {settings.PORT})"
    )
    parser.add_argument(
        "--no-reload",
        action="store_true",
        help="Disable auto-reload on code changes"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default=settings.LOG_LEVEL,
        choices=["critical", "error", "warning", "info", "debug"],
        help=f"Logging level (default: {settings.LOG_LEVEL})"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print(f"  {settings.APP_NAME}")
    print(f"  Version: {settings.APP_VERSION}")
    print("=" * 60)
    print(f"  Server: http://{args.host}:{args.port}")
    print(f"  Docs: http://{args.host}:{args.port}/docs")
    print(f"  ReDoc: http://{args.host}:{args.port}/redoc")
    print("=" * 60)
    print()
    
    uvicorn.run(
        "app:app",
        host=args.host,
        port=args.port,
        reload=not args.no_reload,
        log_level=args.log_level.lower()
    )


if __name__ == "__main__":
    main()
