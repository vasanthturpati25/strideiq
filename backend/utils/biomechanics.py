"""
utils/biomechanics.py — Rule-based scoring engine
"""

BENCHMARKS = {
    "cadence":            {"optimal_min": 170, "optimal_max": 180, "unit": "spm",  "label": "Cadence"},
    "knee_drive_angle":   {"optimal_min": 55,  "optimal_max": 75,  "unit": "°",    "label": "Knee Drive Angle"},
    "forward_lean":       {"optimal_min": 5,   "optimal_max": 10,  "unit": "°",    "label": "Forward Lean"},
    "foot_strike_offset": {"optimal_min": 0.02,"optimal_max": 0.06,"unit": "norm", "label": "Foot Strike Offset"},
    "arm_crossing_index": {"optimal_min": 0.05,"optimal_max": 0.15,"unit": "norm", "label": "Arm Crossing Index"},
}

INJURY_RULES = [
    {"metric": "cadence",            "condition": lambda v: v < 160,  "injury": "Shin Splints",           "explanation": "Low cadence increases ground contact time and tibial stress.", "fix": "Aim for 170–180 spm. Use a metronome app during runs."},
    {"metric": "cadence",            "condition": lambda v: v < 165,  "injury": "Patellofemoral Pain",    "explanation": "Low cadence raises peak knee load per stride.", "fix": "Increase cadence by 5–10% gradually over 2–3 weeks."},
    {"metric": "knee_drive_angle",   "condition": lambda v: v > 80,   "injury": "IT Band Syndrome",       "explanation": "Insufficient knee drive limits hip extension and loads the IT band.", "fix": "Drive the knee forward and upward during the swing phase."},
    {"metric": "forward_lean",       "condition": lambda v: v < 3,    "injury": "Lower Back Pain",        "explanation": "Upright posture shifts load to the lumbar spine.", "fix": "Lean slightly forward from the ankles (not waist)."},
    {"metric": "forward_lean",       "condition": lambda v: v > 15,   "injury": "Hamstring Strain",       "explanation": "Excessive lean increases hamstring eccentric load at toe-off.", "fix": "Reduce forward lean. Keep your ears over your hips."},
    {"metric": "foot_strike_offset", "condition": lambda v: v > 0.08, "injury": "Knee Pain (Overstriding)","explanation": "Large foot-strike offset means landing ahead of your centre of mass.", "fix": "Shorten your stride. Land with foot under, not in front of, your hips."},
    {"metric": "arm_crossing_index", "condition": lambda v: v > 0.20, "injury": "Hip Rotational Stress",  "explanation": "Arms crossing the midline create counter-rotation through the hips.", "fix": "Keep arms swinging forward-back, elbows at ~90°."},
]


def score_metric(metric: str, value: float) -> float:
    b = BENCHMARKS.get(metric)
    if not b:
        return 50.0
    lo, hi = b["optimal_min"], b["optimal_max"]
    mid = (lo + hi) / 2
    half_range = (hi - lo) / 2
    if lo <= value <= hi:
        dist = abs(value - mid) / (half_range + 1e-9)
        return round(100 - dist * 20, 1)
    overshoot = max(lo - value, value - hi, 0)
    penalty = min(overshoot / (half_range + 1e-9) * 40, 80)
    return round(max(20, 80 - penalty), 1)


def evaluate(metrics: dict) -> dict:
    scores = {m: score_metric(m, v) for m, v in metrics.items()}
    overall_score = round(sum(scores.values()) / len(scores), 1)

    triggered_injuries, feedback = [], []
    for rule in INJURY_RULES:
        m = rule["metric"]
        if m in metrics and rule["condition"](metrics[m]):
            triggered_injuries.append(rule["injury"])
            feedback.append({
                "metric": m,
                "label": BENCHMARKS[m]["label"],
                "value": metrics[m],
                "unit": BENCHMARKS[m]["unit"],
                "score": scores.get(m, 50),
                "injury": rule["injury"],
                "explanation": rule["explanation"],
                "fix": rule["fix"],
            })

    risk_level = "Low" if overall_score >= 80 else "Medium" if overall_score >= 60 else "High"

    return {
        "overall_score": overall_score,
        "risk_level": risk_level,
        "scores": scores,
        "injuries": list(dict.fromkeys(triggered_injuries)),
        "feedback": feedback,
        "metrics": metrics,
    }
