"""
AutoCare AI: Main Application Entrypoint.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import Request
from contextlib import asynccontextmanager
from pathlib import Path
import logging

from src.config import settings
from src.database.db import init_db
from src.webhook.routes import router as webhook_router
from src.engine.environmental_classifier import EnvironmentalAudioClassifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("autocare")

classifier = EnvironmentalAudioClassifier()

STATIC_DIR = Path(__file__).resolve().parent / "static"
MONITOR_HTML_PATH = STATIC_DIR / "vibration_monitor.html"

# Pre-cache HTML content for lightning-fast Vercel edge delivery
CACHED_MONITOR_HTML = ""
if MONITOR_HTML_PATH.exists():
    CACHED_MONITOR_HTML = MONITOR_HTML_PATH.read_text(encoding="utf-8")


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

# Mount static directory if directory exists
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/monitor", response_class=HTMLResponse)
async def get_monitor():
    """
    Serves the in-motion mechanical vibration & telemetry dashboard.
    Pre-cached in memory for zero-latency, 100% reliable Vercel serverless execution.
    """
    if CACHED_MONITOR_HTML:
        return HTMLResponse(content=CACHED_MONITOR_HTML)
    elif MONITOR_HTML_PATH.exists():
        return HTMLResponse(content=MONITOR_HTML_PATH.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>AutoCare Telemetry Cluster Initializing...</h1>", status_code=200)


@app.post("/api/classify-audio")
async def api_classify_audio(request: Request):
    """
    Classifies environmental and automotive sounds (Birds, Human voice, Whistling, Engine, Wind).
    """
    try:
        content_type = request.headers.get("content-type", "")
        if "application/json" in content_type:
            body = await request.json()
            freq = float(body.get("frequency", 120.0))
            peak = float(body.get("peak", 80.0))
            centroid = float(body.get("centroid", 500.0))
            return await classifier.classify_audio(b"", dominant_freq_hz=freq, peak_energy=peak, spectral_centroid=centroid)
        else:
            raw_audio = await request.body()
            return await classifier.classify_audio(raw_audio)
    except Exception as e:
        return {"sound_category": "UNKNOWN", "title": "Sound Detected", "description": str(e)}


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Direct root access serves the high-performance Telemetry Dashboard automatically.
    """
    return await get_monitor()


@app.get("/api/status")
async def api_status():
    """System health & API specifications."""
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
