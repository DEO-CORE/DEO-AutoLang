from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from catalog.console import resource_hub
from catalog.views import PublicVerifiedCatalogView

urlpatterns = [
    path("", resource_hub, name="resource-hub"),
    path(
        "health/",
        lambda request: JsonResponse({"status": "ok", "service": "platform-catalog"}),
    ),
    path("admin/", admin.site.urls),
    path("api/v1/compatibility/", PublicVerifiedCatalogView.as_view(), name="public-verified-catalog"),
    path("internal/", include("catalog.urls")),
]
