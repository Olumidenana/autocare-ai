"""
Unit / Smoke Test for AutoCare AI Core Modules.
"""

import asyncio
from src.database.db import init_db
from src.engine.diagnostic_brain import DiagnosticBrain
from src.engine.acoustic_analyzer import AcousticAnalyzer
from src.engine.vision_scanner import VisionScanner
from src.engine.proactive_tracker import ProactiveTracker

async def test_all_modules():
    print("1. Testing Database Initialization...")
    await init_db()
    print("   [OK] SQLite tables created successfully.")

    brain = DiagnosticBrain()
    car = {"make": "Mercedes-Benz", "model": "C300", "year": 2021}

    print("\n2. Testing Multilingual Diagnostic Brain...")
    # Pidgin test
    res_pidgin = await brain.diagnose_symptom("My car dey vibrate for highway", car, "Lagos", "pidgin")
    assert "AutoCare" in res_pidgin["diagnosis_text"]
    assert "vibration" in res_pidgin["diagnosis_text"].lower()
    print("   [OK] Pidgin diagnostic response verified.")

    # Yoruba test
    res_yoruba = await brain.diagnose_symptom("Ẹnjini yii n gbọ̀n ti mo ba duro si traffic", car, "Ibadan", "yoruba")
    assert "AutoCare" in res_yoruba["diagnosis_text"]
    assert "makaniki" in res_yoruba["scam_alert"].lower()
    print("   [OK] Yoruba diagnostic response verified.")

    # Igbo test
    res_igbo = await brain.diagnose_symptom("Nnaa moto m na-eme mkpọtụ", car, "Enugu", "igbo")
    assert "AutoCare" in res_igbo["diagnosis_text"]
    assert "makaniki" in res_igbo["scam_alert"].lower()
    print("   [OK] Igbo diagnostic response verified.")

    print("\n3. Testing Proactive Acoustic Analyzer...")
    acoustic = AcousticAnalyzer()
    report_healthy = acoustic.analyze_audio_sample("healthy_purr.ogg")
    assert report_healthy["acoustic_health_index"] == 94
    print("   [OK] Acoustic healthy purr: 94/100 verified.")

    report_belt = acoustic.analyze_audio_sample("belt_screech.ogg")
    assert report_belt["acoustic_health_index"] == 68
    print("   [OK] Acoustic belt anomaly: 68/100 verified.")

    print("\n4. Testing Computer Vision Scanner...")
    vision = VisionScanner()
    scan = vision.scan_dashboard_image("cluster.jpg", expected_range_km=45000.0)
    assert scan["odometer_km"] > 40000.0
    print(f"   [OK] Vision odometer OCR extracted: {scan['odometer_km']} km.")

    print("\n5. Testing Proactive Fuel Tracker...")
    tracker = ProactiveTracker()
    f1 = tracker.record_fuel_fill(40.0, 32000.0, 45000.0, [], "TotalEnergies")
    assert f1["status"] == "baseline_established"
    print("   [OK] Baseline fuel fill logged.")

    f2 = tracker.record_fuel_fill(40.0, 32000.0, 45360.0, [{"odometer": 45000.0, "km_per_liter": 9.0}], "TotalEnergies")
    assert f2["km_per_liter"] == 9.0
    print(f"   [OK] Trip efficiency computed: {f2['km_per_liter']} km/L.")

    print("\n6. Testing In-Motion Vibration Telemetry Engine...")
    from src.engine.vibration_telemetry import VibrationTelemetryEngine
    vibe = VibrationTelemetryEngine()
    
    # Test 12 Hz wheel imbalance
    v1 = vibe.analyze_vibration_telemetry(dominant_freq_hz=13.5, peak_g_force=1.1, speed_kmh=85.0)
    assert "Wheel assembly wobble" in v1["plain_english"]
    print(f"   [OK] 13.5 Hz wheel imbalance diagnosed: {v1['plain_english'][:40]}...")

    # Test 2.8G severe pothole impact
    v2 = vibe.analyze_vibration_telemetry(dominant_freq_hz=4.0, peak_g_force=2.8, speed_kmh=60.0, road_name="Lekki-Epe Expressway")
    assert v2["pothole_detected"] is True
    assert "Severe pothole" in v2["plain_english"]
    print(f"   [OK] 2.8G crater impact logged with road alert.")

    print("\n==========================================")
    print("[PASS] ALL 6 CORE MODULES PASSED WITH 100% SUCCESS!")
    print("==========================================")

if __name__ == "__main__":
    asyncio.run(test_all_modules())
