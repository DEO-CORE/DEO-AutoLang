from rest_framework import generics, permissions, serializers
from rest_framework.response import Response

from site_api.application.dto import CompatibilityRequestInput
from site_api.application.use_cases import (
    ConsentRequiredError,
    ListWebsiteConfigurations,
    SubmitWebsiteCompatibilityRequest,
)
from site_api.infrastructure.repositories import DjangoWebsiteCompatibilityRepository
from site_api.serializers import (
    CompatibilityRequestSerializer,
    VerifiedConfigurationSerializer,
)


class CompatibilityListView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = VerifiedConfigurationSerializer

    def get(self, request, *args, **kwargs):
        repository = DjangoWebsiteCompatibilityRepository()
        catalog = ListWebsiteConfigurations(repository).execute()
        items = self.get_serializer(catalog.items, many=True).data
        return Response(
            {
                "items": items,
                "total": len(items),
                "updatedAt": catalog.updated_at,
            }
        )


class CompatibilityRequestCreateView(generics.GenericAPIView):
    serializer_class = CompatibilityRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        values = serializer.validated_data
        request_input = CompatibilityRequestInput(
            make=values["make"],
            model=values["model"],
            year=values.get("year"),
            region=values.get("region") or "",
            system_type=values.get("systemType") or "",
            hardware_revision=values.get("hardwareRevision") or "",
            software_version=values.get("softwareVersion") or "",
            details=values.get("details") or "",
            consent_accepted=values["consentAccepted"],
        )
        repository = DjangoWebsiteCompatibilityRepository()
        try:
            result = SubmitWebsiteCompatibilityRequest(repository).execute(
                request_input
            )
        except ConsentRequiredError as error:
            raise serializers.ValidationError(
                {"consentAccepted": str(error)}
            ) from error
        return Response(
            {
                "id": str(result.id),
                "status": result.status,
                "createdAt": result.created_at.isoformat(),
            },
            status=201,
        )
