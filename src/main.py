"""
AutoCare AI: Main Application Entrypoint.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from pathlib import Path
import logging

from src.config import settings
from src.database.db import init_db
from src.webhook.routes import router as webhook_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("autocare")

STATIC_DIR = Path(__file__).resolve().parent / "static"

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing AutoCare database schema...")
    await init_db()
    logger.info(f"AutoCare AI Engine started [Version: {settings.APP_VERSION}]")
    yield
    logger.info("AutoCare AI Engine shutdown complete.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

app.include_router(webhook_router, tags=["WhatsApp Webhook"])

# Mount static directory for in-motion vibration monitor
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/monitor")
async def get_monitor():
    """Serves the in-motion accelerometer & pothole detection telemetry dashboard."""
    monitor_file = STATIC_DIR / "vibration_monitor.html"
    return FileResponse(str(monitor_file))


@app.get("/")
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online",
        "supported_languages": ["English", "Nigerian Pidgin", "Yoruba", "Igbo"],
        "endpoints": {
            "in_motion_monitor": "/monitor (Real-time accelerometer vibration & pothole scanner)",
            "webhook_get": "/webhook (Meta verification)",
            "webhook_post": "/webhook (Inbound message pipeline)"
        }
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
