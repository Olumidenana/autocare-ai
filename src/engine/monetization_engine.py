"""
AutoCare AI: Revenue & Referral Monetization Engine.
Turns diagnostic outputs into immediate commercial revenue for the dealership
via genuine fluids/oil, OEM spare parts, and partner workshop referral commissions.
"""

from typing import Dict, Any, Optional

# Dealership / Partner Product Catalog (Naira Pricing)
PRODUCT_CATALOG = {
    "engine_oil": {
        "title": "Genuine OEM Synthetic Engine Oil",
        "description": "Manufacturer-spec 0W-20 / 5W-30 Full Synthetic (Prevents sludge & timing chain wear)",
        "price_naira": 45000,
        "cta": "🛍️ *Order Genuine Oil*: Tap to have 5L OEM oil delivered or reserved at the showroom."
    },
    "brake_pads": {
        "title": "OEM Ceramic Front Brake Pads",
        "description": "Quiet, zero-dust ceramic pads matching factory braking coefficient",
        "price_naira": 38000,
        "cta": "🛍️ *Order Genuine Brake Pads*: Tap to order OEM pads with 6-month warranty."
    },
    "stabilizer_links": {
        "title": "Heavy-Duty Suspension Stabilizer Links (Pair)",
        "description": "Reinforced ball joints built specifically for Nigerian potholes",
        "price_naira": 28000,
        "cta": "🛍️ *Order Heavy-Duty Links*: Tap to buy durable links that eliminate road rattle."
    },
    "transmission_fluid": {
        "title": "Genuine OEM Automatic Transmission Fluid (ATF)",
        "description": "Factory-spec fluid (Toyota WS / Mercedes MB 236.15) for smooth gear shifting",
        "price_naira": 55000,
        "cta": "🛍️ *Order Genuine ATF*: Tap to buy original fluid and prevent gearbox replacement."
    },
    "workshop_booking": {
        "title": "Certified Partner Workshop Inspection",
        "description": "Vetted master technician inspection with zero quackery guarantee",
        "commission_naira": 5000,
        "cta": "👨‍🔧 *Book Verified Workshop*: Tap to book a verified partner garage near your location."
    }
}


def attach_monetization_hook(diagnosis_category: str, car_info: Optional[Dict[str, Any]] = None) -> str:
    """
    Appends an actionable revenue conversion hook to the diagnostic message.
    """
    cat = diagnosis_category.lower()

    if "vibration" in cat or "cv" in cat or "shocker" in cat:
        item = PRODUCT_CATALOG["stabilizer_links"]
    elif "gear" in cat or "transmission" in cat:
        item = PRODUCT_CATALOG["transmission_fluid"]
    elif "cold_start" in cat or "oil" in cat:
        item = PRODUCT_CATALOG["engine_oil"]
    elif "brake" in cat:
        item = PRODUCT_CATALOG["brake_pads"]
    else:
        item = PRODUCT_CATALOG["workshop_booking"]

    return (
        f"\n\n━━━━━━━━━━━━━━━━━━━━\n"
        f"🛒 *Dealer Store & Verified Fulfillment*\n"
        f"• *Recommended*: {item['title']}\n"
        f"• *Estimate*: ~₦{item.get('price_naira', item.get('commission_naira', 0)):,}\n"
        f"{item['cta']}\n"
        f"*(100% Genuine Guarantee — Avoid Counterfeits)*"
    )
