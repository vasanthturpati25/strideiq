from django.urls import path
from . import views

urlpatterns = [
    path("analyze/", views.analyze, name="analyze"),
    path("history/", views.history, name="history"),
    path("analysis/<int:pk>/", views.analysis_detail, name="analysis-detail"),
]
