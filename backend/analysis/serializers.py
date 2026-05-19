"""
analysis/serializers.py — DRF serializers
"""
from rest_framework import serializers
from .models import Analysis


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = "__all__"
        read_only_fields = ["id", "created_at"]


class AnalysisSummarySerializer(serializers.ModelSerializer):
    """Lighter serializer for history list view."""
    class Meta:
        model = Analysis
        fields = [
            "id", "session_id", "filename", "risk_level",
            "overall_score", "injuries", "created_at",
        ]
