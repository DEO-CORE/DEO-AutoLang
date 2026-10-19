from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

urlpatterns = [
    path(
        "health/",
        lambda request: JsonResponse({"status": "ok", "service": "platform-catalog"}),
    ),
    path("admin/", admin.site.urls),
    path("internal/", include("catalog.urls")),
]
