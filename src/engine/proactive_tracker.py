"""
AutoCare AI: Proactive Fuel Economy & Consumables Tracker.
Tracks fuel fills, computes real-world fuel economy (km/L & NGN/km),
and detects abnormal fuel consumption spikes before check engine lights trigger.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

class ProactiveTracker:
    """
    Manages zero-hardware vehicle tracking, fuel economy monitoring, and proactive alerts.
    """

    def record_fuel_fill(
        self,
        liters: float,
        cost_naira: float,
        current_odometer: float,
        previous_fuel_logs: List[Dict[str, Any]],
        station: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculates fuel efficiency and checks for sudden fuel burn anomalies.
        """
        price_per_liter = cost_naira / liters if liters > 0 else 0.0

        if not previous_fuel_logs:
            # Baseline entry
            return {
                "status": "baseline_established",
                "liters": liters,
                "cost_naira": cost_naira,
                "price_per_liter": round(price_per_liter, 2),
                "km_per_liter": None,
                "message": (
                    f"⛽ *Fuel Log Recorded*\n\n"
                    f"• *Volume*: {liters:.1f} Liters\n"
                    f"• *Total*: ₦{cost_naira:,.2f} (@ ₦{price_per_liter:.0f}/L)\n"
                    f"• *Station*: {station or 'Local Station'}\n"
                    f"• *Odometer*: {current_odometer:,.0f} km\n\n"
                    "📌 *Baseline established*: On your next fill, I will calculate your exact km/Liter fuel economy!"
                )
            }

        last_fill = previous_fuel_logs[-1]
        distance_driven = current_odometer - last_fill.get("odometer", current_odometer)

        if distance_driven <= 0:
            km_per_liter = 8.5  # Typical default average
        else:
            km_per_liter = distance_driven / liters

        naira_per_km = cost_naira / distance_driven if distance_driven > 0 else 0.0

        # Anomaly Detection: Check if fuel consumption spiked (> 20% drop in km/L)
        historical_avg = sum(l.get("km_per_liter", 8.5) for l in previous_fuel_logs if l.get("km_per_liter")) / max(len(previous_fuel_logs), 1)
        anomaly_detected = False
        anomaly_msg = ""

        if historical_avg > 0 and km_per_liter < (historical_avg * 0.78):
            anomaly_detected = True
            anomaly_msg = (
                "\n\n⚠️ *Proactive Anomaly Alert*:\n"
                f"Your fuel consumption jumped by *{round((1 - (km_per_liter / historical_avg)) * 100)}%* on this tank!\n"
                "• *Common Culprits*: Clogged engine air filter, leaking fuel injector, or failing upstream O2 sensor.\n"
                "• *Recommendation*: Clean your air filter box to restore fuel economy."
            )

        return {
            "status": "calculated",
            "distance_driven_km": round(distance_driven, 1),
            "km_per_liter": round(km_per_liter, 2),
            "naira_per_km": round(naira_per_km, 2),
            "anomaly_detected": anomaly_detected,
            "message": (
                f"⛽ *Fuel Efficiency Report*\n\n"
                f"• *Trip Distance*: {distance_driven:,.1f} km\n"
                f"• *Fuel Added*: {liters:.1f} Liters (₦{cost_naira:,.0f})\n"
                f"• *Efficiency*: *{km_per_liter:.2f} km/L* (₦{naira_per_km:.0f}/km)\n"
                f"• *Station*: {station or 'Local Station'}"
                f"{anomaly_msg}"
            )
        }

    def check_maintenance_due(
        self,
        current_odometer: float,
        last_oil_service_km: float,
        recommended_interval_km: float = 7500.0
    ) -> Dict[str, Any]:
        """
        Determines remaining lifespan of engine oil and key service items.
        """
        km_since_last_service = current_odometer - last_oil_service_km
        km_remaining = recommended_interval_km - km_since_last_service

        if km_remaining <= 0:
            status = "DUE_NOW"
            advice = "🚨 *Maintenance Overdue*: Your engine oil and oil filter change is due now. Delaying risks sludge accumulation."
        elif km_remaining <= 800:
            status = "DUE_SOON"
            advice = f"🟡 *Service Approaching*: You have approximately *{km_remaining:,.0f} km* remaining before scheduled oil service."
        else:
            status = "GOOD"
            advice = f"🟢 *Oil Life Healthy*: *{km_remaining:,.0f} km* remaining until next scheduled service."

        return {
            "status": status,
            "km_since_last_service": km_since_last_service,
            "km_remaining": km_remaining,
            "advice": advice
        }
