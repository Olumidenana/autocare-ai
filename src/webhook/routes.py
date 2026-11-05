"""
FastAPI Webhook Endpoints for Meta WhatsApp Cloud API.
"""

from fastapi import APIRouter, Request, Response, HTTPException, status
from typing import Dict, Any
import logging

from src.config import settings
from src.webhook.whatsapp_client import WhatsAppClient
from src.engine.diagnostic_brain import DiagnosticBrain
from src.engine.acoustic_analyzer import AcousticAnalyzer
from src.engine.vision_scanner import VisionScanner
from src.engine.proactive_tracker import ProactiveTracker

router = APIRouter()
logger = logging.getLogger("autocare.webhook")

whatsapp_client = WhatsAppClient()
brain = DiagnosticBrain()
acoustic_analyzer = AcousticAnalyzer()
vision_scanner = VisionScanner()
tracker = ProactiveTracker()


@router.get("/webhook")
async def verify_webhook(request: Request):
    """
    Meta Verification Endpoint.
    Responds to Meta's initial challenge handshake.
    """
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
        logger.info("WhatsApp webhook verified successfully!")
        return Response(content=challenge, media_type="text/plain")

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Verification token mismatch")


@router.post("/webhook")
async def handle_incoming_whatsapp(request: Request):
    """
    Primary Inbound Message Pipeline.
    Receives text, audio voice notes, and dashboard photos.
    """
    body = await request.json()

    # Meta webhook payload safety check
    entry = body.get("entry", [])
    if not entry:
        return {"status": "ignored"}

    changes = entry[0].get("changes", [])
    if not changes:
        return {"status": "ignored"}

    value = changes[0].get("value", {})
    messages = value.get("messages", [])
    if not messages:
        return {"status": "no_messages"}

    msg = messages[0]
    from_phone = msg.get("from")
    msg_type = msg.get("type")

    # In production, look up customer and car profile from database
    simulated_car = {
        "make": "Mercedes-Benz",
        "model": "C300",
        "year": 2021,
        "engine_code": "M274"
    }

    # 1. Text Message Flow
    if msg_type == "text":
        user_text = msg.get("text", {}).get("body", "")
        
        # Check for Fuel Logging intent (e.g., "Bought 45L fuel for 35000")
        if "fuel" in user_text.lower() or "liter" in user_text.lower():
            res = tracker.record_fuel_fill(
                liters=45.0,
                cost_naira=35000.0,
                current_odometer=34500.0,
                previous_fuel_logs=[{"odometer": 34100.0, "km_per_liter": 8.9}],
                station="TotalEnergies"
            )
            await whatsapp_client.send_text_message(from_phone, res["message"])
            return {"status": "fuel_logged"}

        # Diagnostic symptom triage
        diag = await brain.diagnose_symptom(
            user_message=user_text,
            car_info=simulated_car,
            location="Lagos",
            language="pidgin"
        )

        full_reply = f"{diag['diagnosis_text']}\n\n{diag.get('scam_alert', '')}"

        if diag.get("status") == "differential_needed" and diag.get("options"):
            await whatsapp_client.send_button_options(from_phone, full_reply, diag["options"])
        else:
            await whatsapp_client.send_text_message(from_phone, full_reply)

    # 2. Audio Voice Note Flow
    elif msg_type == "audio":
        audio_id = msg.get("audio", {}).get("id")
        # Perform acoustic analysis / health inspection
        acoustic_report = acoustic_analyzer.analyze_audio_sample(audio_id)
        await whatsapp_client.send_text_message(from_phone, acoustic_report["summary_text"])

    # 3. Image Flow (Dashboard Photo)
    elif msg_type == "image":
        image_id = msg.get("image", {}).get("id")
        scan_report = vision_scanner.scan_dashboard_image(image_id)
        await whatsapp_client.send_text_message(from_phone, scan_report["summary_text"])

    # 4. Interactive Button Reply
    elif msg_type == "interactive":
        button_id = msg.get("interactive", {}).get("button_reply", {}).get("id")
        button_title = msg.get("interactive", {}).get("button_reply", {}).get("title")
        
        reply_msg = (
            f"✅ *Received Option*: *{button_title}*\n\n"
            "• *Isolated Diagnosis*: Inner CV Axle Tripod Joint wear.\n"
            "• *Action*: Tell your mechanic to replace the inner joint boot and tripod bearings.\n"
            "• *Scam Warning*: Do NOT pay for whole new shock absorbers!"
        )
        await whatsapp_client.send_text_message(from_phone, reply_msg)

    return {"status": "processed"}
