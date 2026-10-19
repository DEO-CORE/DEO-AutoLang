from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health(request):
    return JsonResponse({"status": "ok", "service": "website-backend"})


urlpatterns = [
    path("health/", health),
    path("admin/", admin.site.urls),
    path("site-api/v1/", include("site_api.urls")),
]
