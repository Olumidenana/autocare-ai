"""
Nigerian Road, City & Terrain Diagnostic Matrix.
Maps geographical realities and transit corridors to vehicle failure modes.
"""

from typing import Dict, Any, List

NIGERIAN_REGIONS: Dict[str, Dict[str, Any]] = {
    "lagos_island": {
        "cities": ["lekki", "ajah", "victoria island", "ikoyi", "oniru", "chevron"],
        "hazards": ["Saltwater spray", "Flash floods / waterlogged roads", "High salinity air"],
        "vulnerable_components": [
            "Automatic transmission breather vent (sucks water if flooded)",
            "Lower steering rack & pinion seals (saltwater rust)",
            "Cabin air filter (mildew/mold dampness)",
            "Rear differential oil (SUVs driving through Lekki floods)"
        ],
        "advisory": (
            "If vehicle crossed water exceeding tire center hub, inspect transmission fluid for "
            "strawberry-milkshake cloudiness immediately."
        )
    },
    "lagos_mainland": {
        "cities": ["ikeja", "surulere", "yaba", "maryland", "ikorodu", "oshodi", "festac", "berger"],
        "hazards": ["2-3 hour bumper-to-bumper standstill traffic", "Intense ambient idle heat", "Potholed inner roads"],
        "vulnerable_components": [
            "Radiator electric cooling fan motor brushes (burns out from continuous high RPM)",
            "Thermostat housing plastic fatigue",
            "Automatic transmission fluid (thermal degradation at low vehicle speeds)",
            "Engine motor mounts (shaken by rough road idling)"
        ],
        "advisory": (
            "High idle time cooks transmission fluid even if mileage is low. "
            "Recommend checking coolant reservoir levels weekly."
        )
    },
    "abuja_fct": {
        "cities": ["abuja", "garki", "wuse", "maitama", "asokoro", "kubwa", "airport road", "lugbe"],
        "hazards": ["Cruising at 120-160 km/h in 38°C dry heat", "Heavy sudden braking on expressways", "High solar radiation"],
        "vulnerable_components": [
            "Tire rubber tread delamination / sidewall blowouts from thermal expansion",
            "Front brake rotors (warping under sudden high-speed deceleration)",
            "Ignition coil hairline cracks (thermal breakdown misfire at high RPM)",
            "Air conditioning compressor thermal cut-off"
        ],
        "advisory": (
            "Never exceed manufacturer tire pressure in hot Abuja afternoon heat. "
            "Inspect tires for sidewall bubbles (eggs)."
        )
    },
    "south_east_south_south": {
        "cities": ["enugu", "onitsha", "aba", "owerri", "port harcourt", "warri", "benin", "asaba"],
        "hazards": ["Gully erosion / deep craters", "Acid rain & petrochemical soot (PH/Warri)", "Heavy gradient climbs"],
        "vulnerable_components": [
            "Lower control arm ball joints & tie-rod ends (bent by high-impact craters)",
            "Alloy wheel inner rim lips (bent/cracked, causing slow bead leaks)",
            "Engine oil sump pan (punctuated by road rocks/depressions)",
            "Brake caliper slide pins (gummed up by soot/acid moisture)"
        ],
        "advisory": (
            "Check inner rim lip and suspension ball joints after hitting deep craters "
            "before paying for repeated wheel alignment."
        )
    },
    "interstate_expressways": {
        "corridors": ["benin-ore", "lagos-ibadan", "lokoja-abuja", "enugu-port harcourt"],
        "hazards": ["Violent washboard corrugations", "High-frequency chassis vibration", "Debris impacts"],
        "vulnerable_components": [
            "Plastic radiator upper tank seams (stress-crack under vibration)",
            "ABS wheel speed sensor wiring harnesses (shaken loose or sliced)",
            "Plastic underbody engine splash shields (torn away)",
            "Catalytic converter internal ceramic matrix (shattered by impact)"
        ],
        "advisory": (
            "Vibrations on long interstate corridors loosen wire harnesses and plastic cooling tanks."
        )
    },
    "northern_nigeria": {
        "cities": ["kano", "kaduna", "jos", "sokoto", "maiduguri"],
        "hazards": ["Fine silica/red harmattan dust", "Dry high-temperature extremes", "Low air moisture"],
        "vulnerable_components": [
            "Engine air filter & Mass Airflow (MAF) sensor (silica grit contamination)",
            "Electronic throttle body butterfly valve (dust gumming)",
            "Alternator bearings & serpentine idler pulley",
            "Battery fluid evaporation (lead-acid batteries dry out)"
        ],
        "advisory": (
            "Blow out or replace engine air filter twice as often during Harmattan."
        )
    }
}


def lookup_regional_risk(location_query: str) -> List[Dict[str, Any]]:
    """
    Returns localized road risk analysis based on user location or transit route.
    """
    query = location_query.lower()
    matches = []
    
    for region_key, data in NIGERIAN_REGIONS.items():
        cities = data.get("cities", [])
        corridors = data.get("corridors", [])
        if any(c in query for c in cities) or any(co in query for co in corridors) or region_key in query:
            matches.append({
                "region": region_key,
                "hazards": data["hazards"],
                "vulnerabilities": data["vulnerable_components"],
                "advisory": data["advisory"]
            })
            
    return matches
