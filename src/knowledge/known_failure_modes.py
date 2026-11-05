"""
Known Failure Modes (KFMs) & Technical Service Bulletins (TSBs).
Covers specific vehicle platforms, engines, and transmissions popular in Nigeria.
"""

from typing import Dict, Any, List

KNOWN_FAILURE_MODES: Dict[str, Dict[str, Any]] = {
    "toyota_lexus_2gr_fe": {
        "models": ["lexus es350", "lexus rx350", "toyota camry v6", "toyota avalon", "toyota sienna"],
        "engine": "2GR-FE 3.5L V6",
        "known_issues": [
            {
                "symptom": "Burning oil smell when driving at expressway speeds",
                "false_mechanic_diagnosis": "Blown head gasket or engine ring damage (thousands of Naira quoted)",
                "true_root_cause": "Rubber rear VVTi oil line failure or front timing chain cover oil seepage.",
                "solution": "Replace with the updated all-metal OEM Toyota VVTi oil line pipe."
            },
            {
                "symptom": "Dull clunking/rattle over small pavement cracks at low speed",
                "false_mechanic_diagnosis": "Replace full steering rack and front shock absorbers",
                "true_root_cause": "Intermediate steering shaft spline dry wear or front stabilizer bar bushings.",
                "solution": "Inspect and grease/replace the intermediate steering shaft."
            },
            {
                "symptom": "Transmission flare / RPM slips up before catching 3rd or 4th gear when hot",
                "false_mechanic_diagnosis": "Dead U660E gearbox; buy Tokunbo replacement",
                "true_root_cause": "Shift solenoid valve body bore wear or degraded Toyota WS ATF fluid.",
                "solution": "Clean/service valve body solenoids and perform full genuine ATF fluid drain and fill."
            }
        ]
    },
    "mercedes_m274_m270": {
        "models": ["mercedes-benz c300", "mercedes c250", "mercedes glc300", "mercedes e300", "c300 w205"],
        "engine": "M274 2.0L Turbo Inline-4",
        "known_issues": [
            {
                "symptom": "Rattle on cold startup lasting 3-5 seconds, check engine light with P0016 / P0017",
                "false_mechanic_diagnosis": "Fuel pump failure or starter motor",
                "true_root_cause": "Camshaft position adjuster phasers (sprockets) worn, or cam magnets leaking oil.",
                "solution": "Inspect camshaft adjuster teeth and verify oil is not wicking into the engine wiring harness."
            },
            {
                "symptom": "Crank no-start or rough running after rain",
                "false_mechanic_diagnosis": "Burnt ECU (brainbox)",
                "true_root_cause": "Auxiliary battery failure or crankcase ventilation (PCV) oil separator line leak.",
                "solution": "Test voltage of auxiliary battery capacitor under passenger footwell and smoke test PCV line."
            },
            {
                "symptom": "Engine hesitation and loss of boost pressure at high RPM",
                "false_mechanic_diagnosis": "Turbocharger blown",
                "true_root_cause": "Turbo boost pressure transducer solenoid vacuum line cracked.",
                "solution": "Inspect ₦15k vacuum line before touching the turbocharger."
            }
        ]
    },
    "mercedes_m276_m278": {
        "models": ["mercedes gle350", "mercedes gle450", "mercedes gls450", "mercedes e350 v6"],
        "engine": "M276 3.5L V6 / 3.0L BiTurbo V6",
        "known_issues": [
            {
                "symptom": "Metallic tick/rattle for 3 seconds on cold morning start",
                "false_mechanic_diagnosis": "Engine knocking; change engine",
                "true_root_cause": "Secondary timing chain tensioner check valves bleeding down oil overnight (Mercedes TSB LI05.10-P-056435).",
                "solution": "Install OEM Mercedes secondary chain tensioner check valves."
            }
        ]
    },
    "toyota_prado_land_cruiser_1gr": {
        "models": ["toyota land cruiser prado", "toyota 4runner", "toyota fj cruiser", "toyota hilux v6"],
        "engine": "1GR-FE 4.0L V6",
        "known_issues": [
            {
                "symptom": "Engine temperature creeps above normal only when AC is on in slow traffic",
                "false_mechanic_diagnosis": "Change water pump and radiator immediately",
                "true_root_cause": "Viscous fan clutch silicon fluid degraded or AC condenser fins blocked with sand/mud.",
                "solution": "Perform newspaper stop-test on the radiator mechanical fan clutch and pressure wash condenser fins."
            }
        ]
    },
    "honda_k24_earth_dreams": {
        "models": ["honda accord", "honda cr-v", "honda crosstour"],
        "engine": "K24 2.4L i-VTEC",
        "known_issues": [
            {
                "symptom": "Loud, violent metallic grinding noise for 1-2 seconds on morning start only",
                "false_mechanic_diagnosis": "Engine rod knock / crankshaft damage",
                "true_root_cause": "Variable Timing Control (VTC) intake cam actuator lock pin failure (Honda TSB 09-010).",
                "solution": "Replace VTC cam gear actuator with the revised OEM Honda part."
            }
        ]
    }
}


def find_known_issue(car_query: str, symptom_query: str) -> List[Dict[str, Any]]:
    """
    Looks up known factory TSBs and failure modes for a specific vehicle and symptom.
    """
    car_q = car_query.lower()
    symp_q = symptom_query.lower()
    matches = []
    
    for key, data in KNOWN_FAILURE_MODES.items():
        models = data.get("models", [])
        if any(m in car_q for m in models) or car_q in key:
            for issue in data.get("known_issues", []):
                symptom_text = issue["symptom"].lower()
                # Check for common semantic tokens
                tokens = [t for t in symp_q.split() if len(t) > 3]
                if any(t in symptom_text for t in tokens) or any(t in issue["true_root_cause"].lower() for t in tokens):
                    matches.append({
                        "platform": data["engine"],
                        "issue": issue
                    })
    return matches
