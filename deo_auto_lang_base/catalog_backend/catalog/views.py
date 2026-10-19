import secrets

from django.conf import settings
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.application.use_cases import ListVerifiedConfigurations
from catalog.infrastructure.django_repositories import (
    DjangoVerifiedConfigurationRepository,
)
from catalog.serializers import VerifiedConfigurationSerializer


class PlatformServicePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        expected = settings.BASE_CATALOG_SERVICE_KEY
        supplied = request.headers.get("X-Base-Catalog-Key", "")
        return bool(expected and secrets.compare_digest(expected, supplied))


class PlatformVerifiedCatalogView(APIView):
    permission_classes = [PlatformServicePermission]

    def get(self, request):
        catalog = ListVerifiedConfigurations(
            DjangoVerifiedConfigurationRepository()
        ).execute()
        items = VerifiedConfigurationSerializer(catalog.items, many=True).data
        updated_at = catalog.updated_at.isoformat() if catalog.updated_at else None
        return Response({"items": items, "total": len(items), "updatedAt": updated_at})
