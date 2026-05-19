"""
analysis/models.py — Django ORM models for StrideIQ
"""
from django.db import models


class Analysis(models.Model):
    RISK_CHOICES = [("Low", "Low"), ("Medium", "Medium"), ("High", "High")]

    session_id = models.CharField(max_length=64, db_index=True)
    filename = models.CharField(max_length=255)
    video_url = models.TextField(blank=True, default="")
    annotated_url = models.TextField(blank=True, default="")

    # Risk / score
    risk_level = models.CharField(max_length=10, choices=RISK_CHOICES, default="Medium")
    overall_score = models.FloatField(default=0.0)

    # Raw metrics
    cadence = models.FloatField(null=True, blank=True)
    knee_drive = models.FloatField(null=True, blank=True)
    forward_lean = models.FloatField(null=True, blank=True)
    foot_strike = models.FloatField(null=True, blank=True)
    arm_crossing = models.FloatField(null=True, blank=True)

    # JSON blobs
    injuries = models.JSONField(default=list)
    feedback = models.JSONField(default=list)
    shap_values = models.JSONField(default=dict)
    scores = models.JSONField(default=dict)
    metrics = models.JSONField(default=dict)
    probabilities = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Analysis #{self.pk} — {self.session_id} — {self.risk_level}"
