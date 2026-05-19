"""
analysis/views.py — DRF API views for StrideIQ
"""
import os
import uuid
import tempfile
import logging

from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import Analysis
from .serializers import AnalysisSerializer, AnalysisSummarySerializer
from utils.pose_estimator import extract_landmarks, compute_biomechanics
from utils.biomechanics import evaluate
from utils.storage import upload_file
from models_ml.ml_model import predict_risk

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {"mp4", "mov", "avi", "webm"}


def _allowed(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ── POST /api/analyze/ ────────────────────────────────────────────────────

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def analyze(request):
    if "video" not in request.FILES:
        return Response({"error": "No video file provided."}, status=status.HTTP_400_BAD_REQUEST)

    video_file = request.FILES["video"]
    if not _allowed(video_file.name):
        return Response(
            {"error": "Unsupported file type. Use mp4, mov, avi, or webm."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    session_id = request.data.get("session_id") or str(uuid.uuid4())
    suffix = "." + video_file.name.rsplit(".", 1)[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        for chunk in video_file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    annotated_path = tmp_path.replace(suffix, f"_annotated{suffix}")

    try:
        # Pose extraction
        result = extract_landmarks(tmp_path, annotated_output_path=annotated_path)
        if not result["success"]:
            return Response({"error": result["error"]}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        if result["detected_count"] < 10:
            return Response(
                {"error": "Too few pose detections. Ensure a clear side-view video."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        # Biomechanics
        metrics = compute_biomechanics(result["frames"], result["fps"])
        evaluation = evaluate(metrics)

        # ML prediction
        ml_result = predict_risk(metrics)
        evaluation["risk_level"] = ml_result["risk_level"]
        evaluation["probabilities"] = ml_result["probabilities"]
        evaluation["shap_values"] = ml_result["shap_values"]

        # Upload videos
        video_url = upload_file(tmp_path, prefix="videos")
        annotated_url = ""
        if os.path.exists(annotated_path):
            annotated_url = upload_file(annotated_path, prefix="annotated")

        # Save to DB
        obj = Analysis.objects.create(
            session_id=session_id,
            filename=video_file.name,
            video_url=video_url,
            annotated_url=annotated_url,
            risk_level=evaluation["risk_level"],
            overall_score=evaluation["overall_score"],
            cadence=metrics.get("cadence"),
            knee_drive=metrics.get("knee_drive_angle"),
            forward_lean=metrics.get("forward_lean"),
            foot_strike=metrics.get("foot_strike_offset"),
            arm_crossing=metrics.get("arm_crossing_index"),
            injuries=evaluation["injuries"],
            feedback=evaluation["feedback"],
            shap_values=evaluation["shap_values"],
            scores=evaluation["scores"],
            metrics=metrics,
            probabilities=evaluation["probabilities"],
        )

        serializer = AnalysisSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error("Analysis error: %s", e, exc_info=True)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    finally:
        for p in [tmp_path, annotated_path]:
            try:
                if os.path.exists(p):
                    os.remove(p)
            except OSError:
                pass


# ── GET /api/history/?session_id=<id> ────────────────────────────────────

@api_view(["GET"])
def history(request):
    session_id = request.query_params.get("session_id")
    if not session_id:
        return Response({"error": "session_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    qs = Analysis.objects.filter(session_id=session_id)
    serializer = AnalysisSummarySerializer(qs, many=True)
    return Response({"history": serializer.data})


# ── GET /api/analysis/<id>/ ───────────────────────────────────────────────

@api_view(["GET"])
def analysis_detail(request, pk):
    try:
        obj = Analysis.objects.get(pk=pk)
    except Analysis.DoesNotExist:
        return Response({"error": "Analysis not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = AnalysisSerializer(obj)
    return Response(serializer.data)
