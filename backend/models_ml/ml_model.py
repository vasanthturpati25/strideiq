"""
models_ml/ml_model.py — Random Forest injury risk classifier
"""
import os
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

MODEL_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(MODEL_DIR, "rf_model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")

FEATURE_COLS = [
    "cadence",
    "knee_drive_angle",
    "forward_lean",
    "foot_strike_offset",
    "arm_crossing_index",
]


def _generate_training_data(n: int = 2000) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    rows = []
    for _ in range(n):
        cadence = rng.normal(172, 12)
        knee_drive = rng.normal(68, 12)
        lean = rng.normal(8, 4)
        foot_offset = rng.normal(0.05, 0.03)
        arm_cross = rng.normal(0.12, 0.05)

        risk_score = 0
        if cadence < 160: risk_score += 2
        elif cadence < 170: risk_score += 1
        if knee_drive > 80: risk_score += 2
        elif knee_drive > 75: risk_score += 1
        if lean < 3 or lean > 15: risk_score += 2
        elif lean < 5 or lean > 12: risk_score += 1
        if foot_offset > 0.08: risk_score += 2
        elif foot_offset > 0.07: risk_score += 1
        if arm_cross > 0.20: risk_score += 1

        label = "High" if risk_score >= 5 else "Medium" if risk_score >= 2 else "Low"
        rows.append({
            "cadence": max(120, min(220, cadence)),
            "knee_drive_angle": max(30, min(120, knee_drive)),
            "forward_lean": max(-5, min(30, lean)),
            "foot_strike_offset": max(0, min(0.2, foot_offset)),
            "arm_crossing_index": max(0, min(0.4, arm_cross)),
            "risk_label": label,
        })
    return pd.DataFrame(rows)


def train_and_save():
    df = _generate_training_data(3000)
    le = LabelEncoder()
    y = le.fit_transform(df["risk_label"])
    X = df[FEATURE_COLS].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    clf = RandomForestClassifier(
        n_estimators=200, max_depth=10, min_samples_leaf=5,
        random_state=42, class_weight="balanced",
    )
    clf.fit(X_train, y_train)

    print("[ML] Training complete.")
    print(classification_report(y_test, clf.predict(X_test), target_names=le.classes_))

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(clf, f)
    with open(ENCODER_PATH, "wb") as f:
        pickle.dump(le, f)

    print(f"[ML] Model saved → {MODEL_PATH}")
    return clf, le


def load_model():
    if not os.path.exists(MODEL_PATH):
        print("[ML] No saved model found. Training now...")
        return train_and_save()
    with open(MODEL_PATH, "rb") as f:
        clf = pickle.load(f)
    with open(ENCODER_PATH, "rb") as f:
        le = pickle.load(f)
    return clf, le


_clf, _le = None, None


def _ensure_loaded():
    global _clf, _le
    if _clf is None:
        _clf, _le = load_model()


def predict_risk(metrics: dict) -> dict:
    _ensure_loaded()
    X = np.array([[metrics.get(f, 0) for f in FEATURE_COLS]])
    proba = _clf.predict_proba(X)[0]
    labels = _le.classes_
    pred_idx = int(np.argmax(proba))
    risk_level = labels[pred_idx]
    probabilities = {labels[i]: round(float(proba[i]), 4) for i in range(len(labels))}
    importances = _clf.feature_importances_
    shap_values = {
        FEATURE_COLS[i]: round(float(importances[i]), 4)
        for i in range(len(FEATURE_COLS))
    }
    return {
        "risk_level": risk_level,
        "probabilities": probabilities,
        "shap_values": shap_values,
    }
