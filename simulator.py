"""
AutoCare AI: Interactive Master Mechanic Terminal Simulator.
Allows testing all diagnostic features (Pidgin, Yoruba, Igbo, Audio, Vision, Fuel tracking)
instantly without needing WhatsApp Cloud API keys or Meta approval.
"""

import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from src.engine.diagnostic_brain import DiagnosticBrain
from src.engine.acoustic_analyzer import AcousticAnalyzer
from src.engine.vision_scanner import VisionScanner
from src.engine.proactive_tracker import ProactiveTracker

console = Console()

async def run_simulator():
    brain = DiagnosticBrain()
    acoustic = AcousticAnalyzer()
    vision = VisionScanner()
    tracker = ProactiveTracker()

    console.print(Panel.fit(
        "[bold cyan]🚗 AutoCare AI: Master Mechanic Simulator[/bold cyan]\n"
        "[green]Speaks English, Nigerian Pidgin, Yoruba, & Igbo fluently.[/green]\n"
        "[dim]Independent Trust, Zero-Hardware Tracking & Proactive Maintenance[/dim]",
        border_style="cyan"
    ))

    # Default vehicle context
    car_info = {
        "make": "Mercedes-Benz",
        "model": "C300",
        "year": 2021,
        "engine_code": "M274"
    }

    fuel_history = []
    current_odometer = 34500.0

    while True:
        console.print("\n[bold yellow]Select a test mode:[/bold yellow]")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Option", style="dim", width=8)
        table.add_column("Scenario / Language")
        table.add_column("Description")

        table.add_row("1", "🇳🇬 Nigerian Pidgin", "Highway vibration / Jerking / Noise")
        table.add_row("2", "🟢 Yoruba Diagnosis", "Engine shaking in traffic (Ẹnjini n gbọ̀n)")
        table.add_row("3", "🔵 Igbo Diagnosis", "Acceleration noise & vibration (Mkpọtụ na-ada)")
        table.add_row("4", "🎧 10-Second Engine Purr Test", "Acoustic audio health check (Belt, Lifters, Knock)")
        table.add_row("5", "📸 Dashboard Photo Scan", "Vision OCR: Mileage check & Warning indicators")
        table.add_row("6", "⛽ Fuel Log & Anomaly Check", "Zero-hardware fuel economy tracking")
        table.add_row("7", "🏎️ In-Motion Vibration & Road Potholes", "Mechanical FFT analysis & G-force shock sensor")
        table.add_row("8", "✏️ Custom Input", "Type your own vehicle symptom in any language")
        table.add_row("0", "Exit", "Quit the simulator")

        console.print(table)
        choice = Prompt.ask("[bold green]Enter choice[/bold green]", choices=["0", "1", "2", "3", "4", "5", "6", "7", "8"], default="1")

        if choice == "0":
            console.print("[bold red]Exiting AutoCare AI Simulator. Goodbye![/bold red]")
            break

        elif choice == "1":
            user_msg = "My car dey vibrate for highway when I reach 80 km/h, wetin fit be the problem?"
            console.print(f"\n[bold cyan]User (Pidgin):[/bold cyan] {user_msg}")
            res = await brain.diagnose_symptom(user_msg, car_info, location="Lagos", language="pidgin")
            console.print(Panel(res["diagnosis_text"], title="[bold green]Master Mechanic Bot[/bold green]", border_style="green"))
            console.print(Panel(res["scam_alert"], title="[bold red]Scam Warning[/bold red]", border_style="red"))

        elif choice == "2":
            user_msg = "Ẹnjini yii n gbọ̀n ti mo ba duro si traffic, kini o n ṣe ọkọ mi?"
            console.print(f"\n[bold cyan]User (Yoruba):[/bold cyan] {user_msg}")
            res = await brain.diagnose_symptom(user_msg, car_info, location="Ibadan", language="yoruba")
            console.print(Panel(res["diagnosis_text"], title="[bold green]Master Mechanic Bot[/bold green]", border_style="green"))
            console.print(Panel(res["scam_alert"], title="[bold red]Ìkìlọ̀ Makaniki[/bold red]", border_style="red"))

        elif choice == "3":
            user_msg = "Nnaa, moto m na-eme mkpọtụ mgbe ọ bụla m gbara ya ọsọ, ọ na-ama jijiji."
            console.print(f"\n[bold cyan]User (Igbo):[/bold cyan] {user_msg}")
            res = await brain.diagnose_symptom(user_msg, car_info, location="Enugu", language="igbo")
            console.print(Panel(res["diagnosis_text"], title="[bold green]Master Mechanic Bot[/bold green]", border_style="green"))
            console.print(Panel(res["scam_alert"], title="[bold red]Ịdọ aka ná ntị[/bold red]", border_style="red"))

        elif choice == "4":
            console.print("\n[bold cyan]Simulating 10-Second Engine Purr Listening Test...[/bold cyan]")
            sound_type = Prompt.ask("Choose sound sample to test", choices=["belt_screech", "healthy_purr", "deep_knock"], default="healthy_purr")
            report = acoustic.analyze_audio_sample(sound_type)
            console.print(Panel(report["summary_text"], title="[bold green]Acoustic Health Inspection[/bold green]", border_style="blue"))

        elif choice == "5":
            console.print("\n[bold cyan]Simulating Dashboard Cluster Photo Upload...[/bold cyan]")
            scan_type = Prompt.ask("Choose cluster photo", choices=["healthy_dash", "check_engine_warning"], default="healthy_dash")
            scan = vision.scan_dashboard_image(scan_type, expected_range_km=current_odometer)
            current_odometer = scan["odometer_km"]
            console.print(Panel(scan["summary_text"], title="[bold green]Computer Vision Odometer & Gauges[/bold green]", border_style="magenta"))

        elif choice == "6":
            console.print("\n[bold cyan]Simulating Fuel Fill Entry...[/bold cyan]")
            liters = float(Prompt.ask("Enter liters bought", default="45"))
            cost = float(Prompt.ask("Enter total Naira paid", default="38000"))
            station = Prompt.ask("Station name", default="TotalEnergies Lekki")
            
            current_odometer += 380.0  # Simulate driving distance
            fuel_res = tracker.record_fuel_fill(liters, cost, current_odometer, fuel_history, station)
            fuel_history.append({"odometer": current_odometer, "km_per_liter": fuel_res.get("km_per_liter", 8.8)})
            console.print(Panel(fuel_res["message"], title="[bold green]Fuel Efficiency Tracker[/bold green]", border_style="yellow"))

        elif choice == "7":
            console.print("\n[bold cyan]Simulating In-Motion Accelerometer Telemetry...[/bold cyan]")
            from src.engine.vibration_telemetry import VibrationTelemetryEngine
            vibe_engine = VibrationTelemetryEngine()

            vibe_type = Prompt.ask(
                "Choose motion scenario",
                choices=["pothole_crater_impact", "highway_tire_wobble", "cv_driveline_vibration", "smooth_road"],
                default="pothole_crater_impact"
            )

            if vibe_type == "pothole_crater_impact":
                v_res = vibe_engine.analyze_vibration_telemetry(4.2, 2.75, 65.0, road_name="Lekki-Epe Expressway")
            elif vibe_type == "highway_tire_wobble":
                v_res = vibe_engine.analyze_vibration_telemetry(13.8, 1.15, 88.0, road_name="Lagos-Ibadan Expressway")
            elif vibe_type == "cv_driveline_vibration":
                v_res = vibe_engine.analyze_vibration_telemetry(32.0, 1.45, 75.0, road_name="Benin-Ore Bypass")
            else:
                v_res = vibe_engine.analyze_vibration_telemetry(0.5, 0.85, 90.0, road_name="Airport Road Abuja")

            console.print(Panel(
                f"📊 *Mechanical Telemetry*: Dominant Freq: {v_res['dominant_frequency_hz']} Hz | Shock: {v_res['peak_g_force']} G\n"
                f"🔬 *Engineering Principle*: {v_res['engineering_analysis']}\n\n"
                f"💬 *Plain English*: {v_res['plain_english']}\n\n"
                f"🇳🇬 *Pidgin Summary*: {v_res['pidgin_summary']}\n\n"
                f"{v_res['road_avoidance_tip'] or ''}",
                title="[bold green]In-Motion Diagnostic Telemetry[/bold green]",
                border_style="magenta"
            ))

        elif choice == "8":
            custom_msg = Prompt.ask("\n[bold cyan]Enter custom symptom/complaint[/bold cyan]")
            lang_choice = Prompt.ask("Preferred response language", choices=["pidgin", "english", "yoruba", "igbo"], default="pidgin")
            res = await brain.diagnose_symptom(custom_msg, car_info, location="Lagos", language=lang_choice)
            console.print(Panel(res["diagnosis_text"], title="[bold green]Master Mechanic Bot[/bold green]", border_style="green"))
            console.print(Panel(res["scam_alert"], title="[bold red]Scam Warning[/bold red]", border_style="red"))

if __name__ == "__main__":
    asyncio.run(run_simulator())
