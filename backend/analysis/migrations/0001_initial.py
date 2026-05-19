from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Analysis",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_id", models.CharField(db_index=True, max_length=64)),
                ("filename", models.CharField(max_length=255)),
                ("video_url", models.TextField(blank=True, default="")),
                ("annotated_url", models.TextField(blank=True, default="")),
                ("risk_level", models.CharField(choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High")], default="Medium", max_length=10)),
                ("overall_score", models.FloatField(default=0.0)),
                ("cadence", models.FloatField(blank=True, null=True)),
                ("knee_drive", models.FloatField(blank=True, null=True)),
                ("forward_lean", models.FloatField(blank=True, null=True)),
                ("foot_strike", models.FloatField(blank=True, null=True)),
                ("arm_crossing", models.FloatField(blank=True, null=True)),
                ("injuries", models.JSONField(default=list)),
                ("feedback", models.JSONField(default=list)),
                ("shap_values", models.JSONField(default=dict)),
                ("scores", models.JSONField(default=dict)),
                ("metrics", models.JSONField(default=dict)),
                ("probabilities", models.JSONField(default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
