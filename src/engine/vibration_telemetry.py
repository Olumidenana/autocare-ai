"""
AutoCare AI: In-Motion Vibration Telemetry & Road Roughness Engine.
Applies mechanical engineering vibration principles (Fast Fourier Transform frequency bands,
Peak G-force shock detection, and chassis resonance) and translates them into plain-language
action items and road-hazard avoidance warnings.
"""

from typing import Dict, Any, List, Optional
import math

class VibrationTelemetryEngine:
    """
    Analyzes in-motion inertial accelerometer telemetry (Z-axis vertical shocks,
    X/Y lateral oscillations, and dominant frequency in Hertz).
    """

    # Mechanical Vibration Frequency Bands (Engineering Standard)
    # 1. 1 - 4 Hz: Sprung Mass (Vehicle Body bounce/heave - Shock absorber damping failure)
    # 2. 10 - 18 Hz: Unsprung Mass (Wheel hop / 1st Order Tire rotational imbalance)
    # 3. 25 - 45 Hz: Driveline / CV Half-shaft rotational harmonics (Inner tripod joint wear)
    # 4. > 50 Hz: High-frequency engine mount / transmission mounting vibration

    def analyze_vibration_telemetry(
        self,
        dominant_freq_hz: float,
        peak_g_force: float,
        speed_kmh: float,
        gps_lat: Optional[float] = None,
        gps_lng: Optional[float] = None,
        road_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processes real-time accelerometer readings from the driver's phone.
        """
        # 1. Engineering Classification
        engineering_cause = ""
        plain_english = ""
        pidgin_advice = ""
        severity = "LOW"
        pothole_detected = False

        # Check for Severe Impact / Pothole (> 2.2G vertical shock)
        if peak_g_force >= 2.2:
            pothole_detected = True
            severity = "CRITICAL"
            engineering_cause = f"High-energy transient vertical shock ({peak_g_force:.2f}G) exceeding wheel rim yield stress."
            plain_english = (
                f"Severe pothole/crater impact recorded ({peak_g_force:.1f}G shock). "
                "Inspect your tire for sidewall bulges and check the inner rim lip for bending."
            )
            pidgin_advice = "Oga, that pothole impact hard well-well! Check your tire make e no form egg or bend rim."

        # Check for 10-18 Hz Wheel / Tire Imbalance
        elif 9.0 <= dominant_freq_hz <= 19.0:
            severity = "MODERATE"
            engineering_cause = f"1st-order rotational harmonic excitation at {dominant_freq_hz:.1f} Hz (correlates with tire angular velocity at {speed_kmh:.0f} km/h)."
            plain_english = (
                f"Wheel assembly wobble detected at {speed_kmh:.0f} km/h. "
                "Your wheel balancing weights have fallen off, or a tire has an uneven tread spot."
            )
            pidgin_advice = "Your tire dey wobble like say the wheel balancing don comot. Vulcanizer need to balance am."

        # Check for 25-45 Hz Driveline / CV Axle Harmonics
        elif 22.0 <= dominant_freq_hz <= 48.0:
            severity = "HIGH"
            engineering_cause = f"2nd-order driveline vibration at {dominant_freq_hz:.1f} Hz under driving torque."
            plain_english = (
                "Driveline vibration detected. The inner CV joint (half-shaft) is worn or has loose bearings."
            )
            pidgin_advice = "The shaft inside dey vibrate under load. Make mechanic check your inner drive shaft."

        # Check for 1-4 Hz Body Bounce (Dead Shock Absorbers)
        elif 1.0 <= dominant_freq_hz <= 4.5:
            severity = "MODERATE"
            engineering_cause = "Sub-harmonic chassis pitch/bounce (under-damped sprung mass oscillation)."
            plain_english = (
                "Excessive vehicle floating/bouncing detected over bumps. "
                "Your shock absorbers have lost hydraulic fluid damping resistance."
            )
            pidgin_advice = "Your motor dey jump up and down like boat; your shock absorbers don weak."

        else:
            engineering_cause = "Harmonic baseline within acceptable road tolerance."
            plain_english = "Ride quality is smooth. Suspension damping is optimal."
            pidgin_advice = "Motor dey roll smooth, no wahala."

        return {
            "dominant_frequency_hz": round(dominant_freq_hz, 1),
            "peak_g_force": round(peak_g_force, 2),
            "speed_kmh": round(speed_kmh, 1),
            "pothole_detected": pothole_detected,
            "severity": severity,
            "engineering_analysis": engineering_cause,
            "plain_english": plain_english,
            "pidgin_summary": pidgin_advice,
            "road_avoidance_tip": (
                f"📍 *Route Alert ({road_name or 'Current Route'})*: Severe surface roughness logged. "
                "Consider taking the center lane or alternate route to preserve suspension arms."
                if pothole_detected else None
            )
        }
