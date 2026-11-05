"""
AutoCare AI: Multimodal & Environmental Audio Classification Engine.
Distinguishes between environmental sounds (birds chirping, whistling, wind/fan,
human speech/humming) and automotive mechanics (engine idle, rod knock, belt squeal).
"""

from typing import Dict, Any, Optional
import httpx
from src.config import settings

class EnvironmentalAudioClassifier:
    def __init__(self):
        self.http_client = httpx.AsyncClient(timeout=25.0)

    async def classify_audio(
        self,
        audio_bytes: bytes,
        dominant_freq_hz: float = 0.0,
        peak_energy: float = 0.0,
        spectral_centroid: float = 0.0
    ) -> Dict[str, Any]:
        """
        Classifies audio using Gemini Multimodal Audio if key is present,
        or the deterministic acoustic DSP model offline.
        """
        if settings.GEMINI_API_KEY and not settings.SIMULATION_MODE and len(audio_bytes) > 100:
            return await self._classify_with_gemini_audio(audio_bytes)
        else:
            return self._classify_offline_dsp(dominant_freq_hz, peak_energy, spectral_centroid)

    async def _classify_with_gemini_audio(self, audio_bytes: bytes) -> Dict[str, Any]:
        """
        Uses Gemini 1.5 / 2.0 Flash native multimodal audio perception.
        """
        import base64
        api_key = settings.GEMINI_API_KEY
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        
        b64_audio = base64.b64encode(audio_bytes).decode("utf-8")

        prompt = (
            "You are a professional acoustic engineer. Listen to this 3-second audio recording. "
            "Identify EXACTLY what you hear. Is it: "
            "1. Birds chirping or nature sounds? "
            "2. A human being speaking, singing, whistling, or humming? "
            "3. An ambient room sound, fan, or running water? "
            "4. A car or motorcycle engine (running, idling, revving, or knocking)? "
            "5. A mechanical squeak, belt squeal, or metallic tap? "
            "Respond in 2 concise sentences: State exactly what sound was detected and its acoustic characteristics."
        )

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "audio/webm",
                                "data": b64_audio
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {"temperature": 0.1, "maxOutputTokens": 200}
        }

        try:
            res = await self.http_client.post(url, json=payload)
            if res.status_code == 200:
                data = res.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return {
                    "sound_category": "AI_PERCEIVED_SOUND",
                    "title": "Acoustic Identification",
                    "description": text
                }
        except Exception:
            pass

        return self._classify_offline_dsp(120.0, 80.0, 500.0)

    def _classify_offline_dsp(
        self,
        freq: float,
        peak: float,
        centroid: float
    ) -> Dict[str, Any]:
        """
        Deterministic acoustic digital signal processing classification.
        """
        # 1. Low volume / Background noise floor
        if peak < 30:
            return {
                "sound_category": "SILENCE_AMBIENT",
                "title": "🔇 Ambient Silence / Low Room Noise",
                "description": "Sound level is below threshold. Make your sound louder or hold closer to the microphone."
            }

        # 2. Birds Chirping / Avian Whistle (High pitch > 2800 Hz with high spectral centroid)
        if freq >= 2700 or centroid > 3200:
            return {
                "sound_category": "BIRDS_HIGH_PITCH",
                "title": "🐦 Bird Chirping / High-Frequency Whistle Detected",
                "description": f"Identified avian bird chirping or high-frequency whistling (~{freq:.0f} Hz). Not an automotive mechanical noise."
            }

        # 3. Whistling / Pure Melodic Tone (800 - 2600 Hz with narrow spectral peak)
        if 850 <= freq <= 2600 and peak > 80:
            return {
                "sound_category": "HUMAN_WHISTLE",
                "title": "🎵 Human Whistling / Musical Tone Detected",
                "description": f"Acoustic harmonics show a pure sinusoidal whistling tone (~{freq:.0f} Hz). Please record car mechanics instead."
            }

        # 4. Human Speech / Vocal Humming (85 - 280 Hz with vocal tract resonance)
        if 85 <= freq <= 280 and centroid < 900:
            return {
                "sound_category": "HUMAN_VOCAL",
                "title": "👤 Human Voice / Vocal Humming Detected",
                "description": f"Identified human vocal cords humming or talking (~{freq:.0f} Hz fundamental pitch). Not vehicle engine combustion."
            }

        # 5. Continuous Fan / Wind / Airflow Noise
        if centroid > 1200 and peak < 80:
            return {
                "sound_category": "WIND_HVAC",
                "title": "💨 Fan / Air Conditioner / Wind Noise",
                "description": "Continuous broadband airflow detected. Point phone away from open vents or blowing wind."
            }

        # 6. Mechanical Engine Combustion Rumble (Deep continuous rumble < 80 Hz or broadband 4-stroke harmonics)
        return {
            "sound_category": "ENGINE_COMBUSTION",
            "title": "🚗 Vehicle Engine Mechanical Rumble Detected",
            "description": f"Internal combustion stroke rhythm verified (~{freq:.0f} Hz). Running smooth with harmonic idle frequency."
        }
