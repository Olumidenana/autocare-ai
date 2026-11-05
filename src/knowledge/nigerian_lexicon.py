"""
Nigerian Automotive Lexicon & Dialect Mapping Engine.
Provides bidirectional semantic translation between automotive engineering terms
and Nigerian vernacular across Pidgin, Yoruba, and Igbo.
"""

from typing import Dict, List, Any

# Common Nigerian Automotive Vernacular Dictionary
NIGERIAN_AUTO_TERMS: Dict[str, Dict[str, Any]] = {
    "brainbox": {
        "engineering_term": "ECU / Engine Control Unit / PCM",
        "category": "Electronics",
        "description": "Vehicle computer controlling ignition, fuel injection, and engine timing.",
        "scam_alert": "Roadside mechanics blame the brainbox for 80% of electrical issues when it is usually a blown fuse, bad relay, or dirty ground strap."
    },
    "shocker": {
        "engineering_term": "Shock Absorber / Strut Assembly",
        "category": "Suspension",
        "description": "Dampens kinetic energy from potholes and road bumps.",
        "scam_alert": "Mechanics often claim shocks are dead when only the top strut mount or stabilizer link is worn."
    },
    "exhaust cat / seed": {
        "engineering_term": "Catalytic Converter",
        "category": "Exhaust & Emissions",
        "description": "Precious-metal honeycomb filter converting toxic exhaust gases.",
        "scam_alert": "CRITICAL SCAM: Dishonest mechanics secretly cut open and remove the catalytic converter honeycomb to sell for cash, causing a loud exhaust drone and permanent P0420 check engine light."
    },
    "top cylinder": {
        "engineering_term": "Cylinder Head / Head Gasket",
        "category": "Engine Core",
        "description": "Houses valves, camshafts, and seals combustion chambers.",
        "scam_alert": "Overheating diagnosis: Always test the cooling fan and thermostat before agreeing to 'skim' or shave the cylinder head."
    },
    "kick starter": {
        "engineering_term": "Starter Motor / Starter Solenoid",
        "category": "Electrical",
        "description": "Electric motor that turns the flywheel to initiate engine combustion.",
        "scam_alert": "Clicking sound during start is 90% a dead battery terminal or weak battery voltage, not a destroyed starter."
    },
    "shaft / drive shaft": {
        "engineering_term": "Constant Velocity (CV) Axle & Half-Shaft",
        "category": "Drivetrain",
        "description": "Transfers rotational torque from transmission to wheels.",
        "scam_alert": "Rapid clicking during full-lock turn indicates worn outer CV joints; vibration under acceleration indicates worn inner tripod joints."
    },
    "absorber cup / top mount": {
        "engineering_term": "Strut Mount & Bearing Plate",
        "category": "Suspension",
        "description": "Upper mounting point connecting strut to vehicle body.",
        "scam_alert": "Dull thud or creaking when turning the steering while parked is often this mount bearing, not a damaged steering rack."
    },
    "gear selector / gear box": {
        "engineering_term": "Automatic Transmission / Shift Solenoids",
        "category": "Transmission",
        "description": "Hydraulic or electronic gearbox transmitting speed/torque ratios.",
        "scam_alert": "Jerking into gear is frequently low or contaminated ATF fluid, or a gummed-up solenoid valve body—rarely requires a whole new transmission."
    }
}

# Phonetic & Vernacular Symptom Sound Mappings
ACOUSTIC_DESCRIPTIONS: Dict[str, Dict[str, str]] = {
    "gbagba-gbagba / kpo-kpo-kpo": {
        "probable_cause": "Worn stabilizer bar links, dried sway bar bushings, or bad ball joints.",
        "when_heard": "Driving over rough corrugated roads, potholes, or interlocking paving stones."
    },
    "gbii / gbi-gbi": {
        "probable_cause": "Bottoming out suspension, broken coil spring, or blown shock absorber absorbing direct chassis impact.",
        "when_heard": "Hitting deep depressions or speed bumps at speed."
    },
    "screeech / whiiiiing": {
        "probable_cause": "Slipping serpentine drive belt, worn alternator decouple pulley, or dry belt tensioner bearing.",
        "when_heard": "Immediately upon cold engine startup or when turning on the AC compressor."
    },
    "tik-tik-tik-tik": {
        "probable_cause": "Hydraulic valve lifter tick, low oil pressure, or high-pressure direct fuel injector pulse.",
        "when_heard": "At idle, speeding up proportionally with engine RPM."
    },
    "grrrrrr / humming": {
        "probable_cause": "Dry wheel hub bearing or worn differential pinion bearing.",
        "when_heard": "Cruising between 60 km/h and 100 km/h; pitch changes when gently swaying the vehicle left and right."
    }
}

# Igbo, Yoruba, and Pidgin Context Phrases
LANGUAGE_IDENTIFIERS: Dict[str, List[str]] = {
    "pidgin": [
        "dey", "wetin", "na", "fit", "kabu-kabu", "pothole", "match", "motor", "gear", "off", 
        "quack", "don", "dash", "gbagba", "vibrate", "scatter", "comot", "sound", "wahala"
    ],
    "yoruba": [
        "ẹnjini", "ọkọ", "kini", "ṣe", "ti", "gbọ̀n", "dun", "ba", "wọ́n", "makaniki", "eepo", "omi"
    ],
    "igbo": [
        "moto", "mkpọtụ", "mmanụ", "nnaa", "ọ̀", "na-eme", "kwụsịrị", "ike", "lelee", "enjin", "ihe"
    ]
}


def translate_vernacular_to_technical(text: str) -> str:
    """
    Scans a user's prompt or transcription for local colloquialisms and enriches
    the context with formal automotive engineering definitions.
    """
    enriched_notes = []
    text_lower = text.lower()
    
    for term, data in NIGERIAN_AUTO_TERMS.items():
        if term in text_lower:
            enriched_notes.append(
                f"[Term detected: '{term}' -> Refers to: {data['engineering_term']}. Context: {data['description']}]"
            )
            
    for sound, data in ACOUSTIC_DESCRIPTIONS.items():
        sounds_split = [s.strip() for s in sound.split("/")]
        if any(s in text_lower for s in sounds_split):
            enriched_notes.append(
                f"[Acoustic description detected: '{sound}' -> Likely culprit: {data['probable_cause']}]"
            )
            
    return "\n".join(enriched_notes)
