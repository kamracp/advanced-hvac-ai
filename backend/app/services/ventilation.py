"""
ASHRAE 62.1 Ventilation Service (SI units)
Ported from advanced-hvac-ai/modules/ventilation_engine.py (SI-converted version).
"""

ASHRAE_TABLE = {
    "Office Space": {"Rp": 2.36, "Ra": 0.30},
    "Conference Room": {"Rp": 2.36, "Ra": 0.30},
    "Restaurant Dining": {"Rp": 3.54, "Ra": 0.91},
    "Retail Sales": {"Rp": 3.54, "Ra": 0.61},
    "Classroom": {"Rp": 4.72, "Ra": 0.61},
    "Gym/Exercise Room": {"Rp": 9.44, "Ra": 0.30},
    "Hotel Bedroom": {"Rp": 2.36, "Ra": 0.30},
    "Warehouse": {"Rp": 0, "Ra": 0.30},
}

EZ_FACTORS = {
    "Ceiling Supply Cool Air": 1.0,
    "Ceiling Supply Warm Air": 0.8,
    "Floor Supply": 1.0,
    "Displacement Ventilation": 1.2,
}


def ventilation_calculation(space_type: str, area_m2: float, occupancy: float, distribution: str) -> dict:
    db = ASHRAE_TABLE.get(space_type, {"Rp": 2.36, "Ra": 0.30})
    rp = db["Rp"]
    ra = db["Ra"]
    ez = EZ_FACTORS.get(distribution, 1.0)

    vbz = occupancy * rp + area_m2 * ra
    voz = vbz / ez

    vbz_m3hr = vbz * 3.6
    voz_m3hr = voz * 3.6

    return {
        "space_type": space_type,
        "rp_ls_per_person": rp,
        "ra_ls_per_m2": ra,
        "ez": ez,
        "vbz_ls": round(vbz, 2),
        "vbz_m3hr": round(vbz_m3hr, 0),
        "voz_ls": round(voz, 2),
        "voz_m3hr": round(voz_m3hr, 0),
    }
