"""
StrideIQ root URL configuration
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok", "service": "StrideIQ API"})


urlpatterns = [
    path("api/health/", health_check),
    path("api/", include("analysis.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
