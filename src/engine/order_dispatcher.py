"""
AutoCare AI: Order Fulfillment & Dealer WhatsApp Dispatcher.
Automatically routes parts orders, oil requests, and workshop bookings
directly to the dealership's sales team and sends receipts to customers.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import uuid

from src.webhook.whatsapp_client import WhatsAppClient
from src.database.models import Customer, Vehicle

# In production, replace with AutoContentment's WhatsApp Sales Desk number
DEALER_SALES_PHONE = "2348000000000"

class OrderDispatcher:
    def __init__(self):
        self.whatsapp = WhatsAppClient()

    async def create_and_dispatch_order(
        self,
        customer_phone: str,
        customer_name: str,
        vehicle_details: str,
        item_title: str,
        price_naira: float,
        delivery_location: str = "Lagos"
    ) -> Dict[str, Any]:
        """
        Creates an order, logs it, and dispatches real-time WhatsApp alerts
        to both the dealership's fulfillment desk and the customer.
        """
        order_id = f"AC-{uuid.uuid4().hex[:6].upper()}"
        timestamp = datetime.now().strftime("%Y-%m-%d %I:%M %p")

        # 1. Customer Confirmation Message
        customer_receipt = (
            f"🧾 *AutoCare Order Confirmed!* [#{order_id}]\n\n"
            f"• *Item*: {item_title}\n"
            f"• *Vehicle*: {vehicle_details}\n"
            f"• *Amount*: ₦{price_naira:,.2f}\n"
            f"• *Delivery City*: {delivery_location}\n"
            f"• *Time*: {timestamp}\n\n"
            "📦 *Next Step*: AutoContentment fulfillment team is preparing your genuine parts. "
            "A representative will contact you shortly to confirm drop-off location or workshop bay."
        )

        # 2. Dealership Sales Team Dispatch Alert
        dealer_alert = (
            f"🔔 *NEW CUSTOMER ORDER INBOUND!* [#{order_id}]\n\n"
            f"👤 *Customer*: {customer_name} ({customer_phone})\n"
            f"🚗 *Vehicle*: {vehicle_details}\n"
            f"🛒 *Ordered Item*: {item_title} (₦{price_naira:,.2f})\n"
            f"📍 *Location*: {delivery_location}\n"
            f"⏱️ *Order Time*: {timestamp}\n\n"
            "👉 *Action Required*: Reach out to customer via WhatsApp to confirm payment & dispatch."
        )

        # Send customer receipt
        await self.whatsapp.send_text_message(customer_phone, customer_receipt)

        # Send dealer fulfillment alert
        await self.whatsapp.send_text_message(DEALER_SALES_PHONE, dealer_alert)

        return {
            "order_id": order_id,
            "status": "DISPATCHED",
            "customer_receipt": customer_receipt,
            "dealer_alert": dealer_alert
        }
