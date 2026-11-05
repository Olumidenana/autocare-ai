"""
AutoCare AI: Master Mechanic Diagnostic Brain.
Combines vehicle context, Nigerian vernacular translation, regional road terrain matrix,
and OEM Technical Service Bulletins into high-precision, fraud-resistant diagnostics.
"""

from typing import Dict, Any, Optional, Tuple, List
import json
import httpx

from src.config import settings
from src.knowledge.nigerian_lexicon import translate_vernacular_to_technical, NIGERIAN_AUTO_TERMS
from src.knowledge.road_terrain_matrix import lookup_regional_risk
from src.knowledge.known_failure_modes import find_known_issue
from src.engine.monetization_engine import attach_monetization_hook

SYSTEM_PERSONA = """
You are 'AutoCare Master Co-Pilot', an ASE Certified Master Diagnostic Automotive Technician with 25 years of hands-on experience in Nigeria.
You speak fluently in Nigerian English, Nigerian Pidgin, Yoruba, and Igbo.

CORE MISSION & ETHICS:
1. You are the driver's independent, objective shield against dishonest mechanics and unnecessary part replacements.
2. You NEVER give a vague 'shotgun' list of 10 generic parts.
3. If there is ambiguity between two likely faults, you MUST ask the single highest-probability clarifying question (Differential Diagnosis).
4. You always consider the harsh reality of Nigerian roads (potholes, contaminated fuel, flash floods, 38°C dry heat).
5. Always highlight the 'Mechanic Scam Alert' (what deceitful mechanics will claim, e.g. 'brainbox is burnt' or 'change the whole gearbox').
"""

class DiagnosticBrain:
    def __init__(self):
        self.http_client = httpx.AsyncClient(timeout=30.0)

    async def diagnose_symptom(
        self,
        user_message: str,
        car_info: Optional[Dict[str, Any]] = None,
        location: str = "Lagos",
        language: str = "pidgin"
    ) -> Dict[str, Any]:
        vernacular_notes = translate_vernacular_to_technical(user_message)
        regional_risks = lookup_regional_risk(location)
        car_str = f"{car_info.get('make', '')} {car_info.get('model', '')}" if car_info else "Vehicle"
        known_issues = find_known_issue(car_str, user_message)

        # 1. Prefer Google Gemini API (Free Tier from Google AI Studio)
        if settings.GEMINI_API_KEY and not settings.SIMULATION_MODE:
            result = await self._call_gemini_api(user_message, car_info, vernacular_notes, regional_risks, known_issues, language)
        elif settings.OPENAI_API_KEY and not settings.SIMULATION_MODE:
            result = await self._call_openai_api(user_message, car_info, vernacular_notes, regional_risks, known_issues, language)
        else:
            result = self._rule_based_master_diagnosis(user_message, car_info, vernacular_notes, regional_risks, known_issues, language)

        # 2. Attach Revenue & Parts Monetization Hook (Turns diagnosis into business profit)
        monetization_text = attach_monetization_hook(user_message, car_info)
        result["monetization_hook"] = monetization_text
        result["diagnosis_text"] += monetization_text

        return result

    def _rule_based_master_diagnosis(
        self,
        message: str,
        car_info: Optional[Dict[str, Any]],
        vernacular_notes: str,
        regional_risks: List[Dict[str, Any]],
        known_issues: List[Dict[str, Any]],
        language: str
    ) -> Dict[str, Any]:
        msg_lower = message.lower()
        car_model = f"{car_info.get('year', '')} {car_info.get('make', '')} {car_info.get('model', '')}" if car_info else "your vehicle"

        # Check for Vibration & Noise (English, Pidgin, Yoruba "gbọ̀n", Igbo "mkpọtụ", "jijiji")
        if any(v in msg_lower for v in ["vibrat", "shak", "gbagba", "gbọ̀n", "gbon", "jijiji", "mkpọtụ", "mkpotu"]):
            return self._handle_vibration_case(msg_lower, car_model, language)

        # Check for Cold Morning start noise / rattle
        if any(c in msg_lower for c in ["morning", "cold", "start", "aarọ", "ututu"]):
            return self._handle_cold_start_case(msg_lower, car_model, known_issues, language)

        # Check for Overheating / AC failure in traffic
        if any(o in msg_lower for o in ["overheat", "ac", "traffic", "hot", "gbona", "ọkụ", "oku"]):
            return self._handle_cooling_ac_case(msg_lower, car_model, language)

        # Check for Gear / Transmission issues
        if any(g in msg_lower for g in ["gear", "shift", "delay", "transmission"]):
            return self._handle_transmission_case(msg_lower, car_model, language)

        return self._handle_general_case(message, car_model, language, regional_risks)

    def _handle_vibration_case(self, msg: str, car: str, lang: str) -> Dict[str, Any]:
        if lang == "pidgin":
            text = (
                f"🔧 *AutoCare Master Diagnosis ({car})*\n\n"
                "I hear you well! For road vibration, bad mechanics dey always scam drivers say make dem change shockers or steering rack.\n\n"
                "👉 *Quick Test to pinpoint the exact fault*:\n"
                "Does this vibration happen *ONLY* when your foot dey press the accelerator pedal, and e dey disappear when you free your leg?\n"
            )
            scam = "⚠️ *Mechanic Scam Alert*: No let any mechanic do alignment on bent arms or charge you for new shocks before checking the inner CV tripod joint."
        elif lang == "yoruba":
            text = (
                f"🔧 *AutoCare Ìṣàyẹ̀wò fún {car}*\n\n"
                "Ẹ jẹ́ ká wo ọ̀rọ̀ gbigbọn yìí dáadáa kí àwọn makaniki má baà gbà yín lówó lásán.\n\n"
                "👉 *Ìbéèrè Pàtàkì*:\n"
                "Ṣé gbigbọn yìí ma ń wáyé NÍGBÀ TÍ Ẹ BA TẸ PETROL NÌKAN, tàbí ó ń gbọ̀n bẹ́ẹ̀bẹ́ẹ̀ lọ́wọ́ pápá?\n"
            )
            scam = "⚠️ *Ìkìlọ̀ Makaniki*: Ẹ má ṣe gba kí wọ́n sọ pé kí ẹ ra shocker tuntun tàbí steering rack tuntun láì kọ́kọ́ yẹ shaft wò."
        elif lang == "igbo":
            text = (
                f"🔧 *AutoCare Nnyocha maka {car}*\n\n"
                "Bia Chief, tupu ndị makaniki anara gị ego na-akwọghị aka na shocker, ka anyị chọpụta eziokwu.\n\n"
                "👉 *Ajụjụ dị mkpa*:\n"
                "Mkpọtụ ma ọ bụ jijiji ahụ ọ̀ na-eme naanị mgbe ị zọrọ accelerator, ka ọ̀ na-ama jijiji mgbe niile?\n"
            )
            scam = "⚠️ *Ịdọ aka ná ntị Makaniki*: Ekwela ka ndị makaniki sị gị gbanwee steering rack ma ọ bụ shocker ozugbo!"
        else:
            text = (
                f"🔧 *AutoCare Master Diagnosis ({car})*\n\n"
                "Vibration at speed is often misdiagnosed as suspension failure.\n\n"
                "👉 *Critical Diagnostic Question*:\n"
                "Does this vibration happen **ONLY** when you press the accelerator pedal, and vanish when you coast?\n"
            )
            scam = "⚠️ *Mechanic Scam Alert*: Never replace shock absorbers or steering racks for highway vibration until you isolate the inner CV joint and wheel balance."

        return {
            "status": "differential_needed",
            "diagnosis_text": text,
            "scam_alert": scam,
            "options": [
                "Only when accelerating (Inner CV Axle)",
                "Constant at 80+ km/h (Wheel Balancing)",
                "Only when braking (Warped Brake Rotors)"
            ]
        }

    def _handle_cold_start_case(self, msg: str, car: str, known_issues: List[Dict[str, Any]], lang: str) -> Dict[str, Any]:
        issue_detail = known_issues[0]["issue"] if known_issues else None
        root_cause = issue_detail["true_root_cause"] if issue_detail else "Camshaft timing gear lock-pin or dry hydraulic valve lifters"
        
        text = (
            f"🔍 *AutoCare Cold Start Rattle Analysis ({car})*\n\n"
            f"• *Probable Root Cause*: {root_cause}.\n"
            "• *Why it happens*: Oil drains down into the oil pan overnight. During the first 3 seconds of cranking, the upper engine runs without oil pressure until the pump builds pressure.\n"
            "• *Action*: Use genuine manufacturer-spec synthetic engine oil (e.g., 0W-20 or 5W-30). Do NOT use thick 20W-50 oil!"
        )
        scam = "⚠️ *Mechanic Scam Alert*: Mechanics will say your engine is knocking and ask you to buy a new engine. A 2-3 second morning rattle is an oil pressure check-valve or VTC actuator issue, NOT a blown crankshaft."

        return {
            "status": "conclusive",
            "diagnosis_text": text,
            "scam_alert": scam
        }

    def _handle_cooling_ac_case(self, msg: str, car: str, lang: str) -> Dict[str, Any]:
        text = (
            f"🌡️ *AutoCare Traffic Overheating & AC Loss Analysis ({car})*\n\n"
            "• *Root Cause*: Radiator Auxiliary Electric Cooling Fan is weak or failing to hit High-Speed mode.\n"
            "• *Explanation*: When cruising on the expressway, natural airflow cools the radiator. But in Lagos/Abuja traffic at 0 km/h, the electric fan MUST pull air. If the fan motor brushes are worn, heat builds up instantly and the AC compressor shuts down to protect the system."
        )
        scam = "⚠️ *Mechanic Scam Alert*: Mechanics will tell you to 'pump more AC gas' or that your AC compressor is dead. The compressor is just turning off because the engine cooling fan is failing!"

        return {
            "status": "conclusive",
            "diagnosis_text": text,
            "scam_alert": scam
        }

    def _handle_transmission_case(self, msg: str, car: str, lang: str) -> Dict[str, Any]:
        text = (
            f"⚙️ *AutoCare Transmission Shift Delay Analysis ({car})*\n\n"
            "• *Root Cause*: Gummed up shift solenoids, low ATF fluid, or contaminated transmission valve body.\n"
            "• *Immediate Check*: Check transmission fluid level and color. Bright pink/red is healthy; dark brown or burnt smelling means fluid is cooked."
        )
        scam = "⚠️ *Mechanic Scam Alert*: Roadside workshops quote ₦600k+ for a whole 'Tokunbo gearbox'. 85% of shift delays are fixed with a genuine transmission fluid service and shift solenoid cleaning."

        return {
            "status": "conclusive",
            "diagnosis_text": text,
            "scam_alert": scam
        }

    def _handle_general_case(self, msg: str, car: str, lang: str, risks: List[Dict[str, Any]]) -> Dict[str, Any]:
        advisory = risks[0]["advisory"] if risks else "Keep tires at correct PSI and inspect fluid levels monthly."
        text = (
            f"📋 *AutoCare Preliminary Inspection ({car})*\n\n"
            f"We have logged your report: *\"{msg}\"*\n\n"
            "• *Recommended First Step*: Send a quick 10-second voice note of the noise or snap a photo of your dashboard gauges so we can inspect the exact warning lights.\n"
            f"• *Regional Advisory*: {advisory}"
        )
        scam = "⚠️ *Mechanic Scam Alert*: Always demand to see the old replaced part whenever any work is done."
        return {
            "status": "conclusive",
            "diagnosis_text": text,
            "scam_alert": scam
        }

    async def _call_gemini_api(
        self,
        message: str,
        car_info: Optional[Dict[str, Any]],
        vernacular_notes: str,
        regional_risks: List[Dict[str, Any]],
        known_issues: List[Dict[str, Any]],
        language: str
    ) -> Dict[str, Any]:
        """
        Calls Google Gemini 2.0 Flash / 1.5 Flash via REST API (100% Free on Google AI Studio).
        """
        api_key = settings.GEMINI_API_KEY
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

        prompt = (
            f"{SYSTEM_PERSONA}\n\n"
            f"User Vehicle: {car_info}\n"
            f"User Location Risks: {regional_risks}\n"
            f"Vernacular Context: {vernacular_notes}\n"
            f"Known Manufacturer Issues: {known_issues}\n"
            f"Preferred Language: {language}\n\n"
            f"User Message: {message}\n\n"
            "Respond in WhatsApp formatting with clear diagnosis, why it happens, recommended action, and a Mechanic Scam Alert."
        )

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 600}
        }

        try:
            res = await self.http_client.post(url, json=payload)
            if res.status_code == 200:
                data = res.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "status": "conclusive",
                    "diagnosis_text": text,
                    "scam_alert": "⚠️ *Scam Alert*: Always verify old replaced parts."
                }
        except Exception:
            pass

        # Fallback to local rule engine if network or rate limit occurs
        return self._rule_based_master_diagnosis(message, car_info, vernacular_notes, regional_risks, known_issues, language)

    async def _call_openai_api(self, *args, **kwargs):
        return self._rule_based_master_diagnosis(*args[0:6])
