"""
Meta WhatsApp Cloud API Client.
Handles sending messages, interactive buttons, and media downloads.
"""

from typing import Dict, Any, List, Optional
import httpx
from src.config import settings

GRAPH_API_VERSION = "v21.0"
BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

class WhatsAppClient:
    def __init__(self):
        self.token = settings.WHATSAPP_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.http_client = httpx.AsyncClient(timeout=30.0)

    async def send_text_message(self, to_phone: str, message: str) -> Dict[str, Any]:
        """
        Sends a standard text message to a user on WhatsApp.
        """
        if not self.token or not self.phone_number_id:
            # Running in local simulation / unconfigured mode
            return {"status": "simulated", "to": to_phone, "message": message}

        url = f"{BASE_URL}/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_phone,
            "type": "text",
            "text": {"preview_url": False, "body": message}
        }

        response = await self.http_client.post(url, headers=headers, json=payload)
        return response.json()

    async def send_button_options(
        self,
        to_phone: str,
        body_text: str,
        options: List[str]
    ) -> Dict[str, Any]:
        """
        Sends an interactive message with up to 3 quick-reply buttons on WhatsApp.
        """
        if not self.token or not self.phone_number_id:
            return {"status": "simulated", "to": to_phone, "body": body_text, "options": options}

        buttons = []
        for i, opt in enumerate(options[:3]):
            buttons.append({
                "type": "reply",
                "reply": {
                    "id": f"btn_{i}",
                    "title": opt[:20]  # WhatsApp 20-character title limit
                }
            })

        url = f"{BASE_URL}/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_phone,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body_text},
                "action": {"buttons": buttons}
            }
        }

        response = await self.http_client.post(url, headers=headers, json=payload)
        return response.json()

    async def download_media(self, media_id: str) -> bytes:
        """
        Retrieves and downloads encrypted media (audio voice notes or photos) from Meta.
        """
        if not self.token:
            return b"simulated_media_bytes"

        # Step 1: Get media URL
        url = f"{BASE_URL}/{media_id}"
        headers = {"Authorization": f"Bearer {self.token}"}
        res = await self.http_client.get(url, headers=headers)
        media_url = res.json().get("url")

        if not media_url:
            raise ValueError(f"Could not retrieve media URL for id {media_id}")

        # Step 2: Download raw binary
        media_res = await self.http_client.get(media_url, headers=headers)
        return media_res.content
