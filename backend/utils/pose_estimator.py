"""
utils/pose_estimator.py — MediaPipe Pose landmark extraction from video frames
"""
import cv2
import numpy as np
import mediapipe as mp
import math
import os

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

LM = mp_pose.PoseLandmark


def extract_landmarks(video_path: str, annotated_output_path: str = None) -> dict:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"success": False, "error": "Cannot open video file.", "frames": []}

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer = None
    if annotated_output_path:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(annotated_output_path, fourcc, fps, (width, height))

    all_frames = []

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        smooth_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)

            if results.pose_landmarks:
                lm_list = [
                    {"x": lm.x, "y": lm.y, "z": lm.z, "visibility": lm.visibility}
                    for lm in results.pose_landmarks.landmark
                ]
                all_frames.append(lm_list)
                if writer:
                    mp_drawing.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
                    )
            else:
                all_frames.append(None)

            if writer:
                writer.write(frame)

    cap.release()
    if writer:
        writer.release()

    detected = [f for f in all_frames if f is not None]
    return {
        "success": True,
        "error": None,
        "frames": detected,
        "fps": fps,
        "frame_count": len(all_frames),
        "detected_count": len(detected),
    }


def _angle(a, b, c) -> float:
    ba = np.array([a["x"] - b["x"], a["y"] - b["y"]])
    bc = np.array([c["x"] - b["x"], c["y"] - b["y"]])
    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-9)
    return math.degrees(math.acos(np.clip(cos_angle, -1, 1)))


def _lm(frame, idx):
    return frame[idx.value]


def compute_biomechanics(frames: list, fps: float) -> dict:
    if not frames:
        return {}

    knee_angles, lean_angles, foot_offsets, arm_indices = [], [], [], []
    ankle_y_series = []

    for frame in frames:
        if frame is None:
            continue
        try:
            hip = _lm(frame, LM.RIGHT_HIP)
            knee = _lm(frame, LM.RIGHT_KNEE)
            ankle = _lm(frame, LM.RIGHT_ANKLE)
            knee_angles.append(_angle(hip, knee, ankle))

            r_shoulder = _lm(frame, LM.RIGHT_SHOULDER)
            r_hip = _lm(frame, LM.RIGHT_HIP)
            dx = r_hip["x"] - r_shoulder["x"]
            dy = r_hip["y"] - r_shoulder["y"]
            lean = math.degrees(math.atan2(abs(dx), abs(dy)))
            lean_angles.append(lean)

            foot_offsets.append(abs(ankle["x"] - hip["x"]))

            l_wrist = _lm(frame, LM.LEFT_WRIST)
            r_wrist = _lm(frame, LM.RIGHT_WRIST)
            mid_x = (r_shoulder["x"] + _lm(frame, LM.LEFT_SHOULDER)["x"]) / 2
            arm_indices.append(abs(l_wrist["x"] - mid_x) + abs(r_wrist["x"] - mid_x))

            ankle_y_series.append(ankle["y"])
        except (IndexError, KeyError):
            continue

    cadence = _estimate_cadence(ankle_y_series, fps)

    return {
        "knee_drive_angle": float(np.percentile(knee_angles, 25)) if knee_angles else 90.0,
        "cadence": cadence,
        "forward_lean": float(np.mean(lean_angles)) if lean_angles else 5.0,
        "foot_strike_offset": float(np.mean(foot_offsets)) if foot_offsets else 0.05,
        "arm_crossing_index": float(np.mean(arm_indices)) if arm_indices else 0.1,
    }


def _estimate_cadence(ankle_y: list, fps: float) -> float:
    if len(ankle_y) < 10:
        return 160.0
    arr = np.array(ankle_y)
    diff = np.diff(arr)
    peaks = np.where((diff[:-1] < 0) & (diff[1:] >= 0))[0]
    if len(peaks) < 2:
        return 160.0
    duration_seconds = len(ankle_y) / fps
    return round((len(peaks) * 2 / duration_seconds) * 60, 1)
