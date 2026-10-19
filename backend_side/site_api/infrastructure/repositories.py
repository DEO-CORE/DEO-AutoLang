from site_api.application.dto import (
    CompatibilityRequestInput,
    SubmittedCompatibilityRequest,
    WebsiteVerifiedConfiguration,
)
from site_api.models import (
    WebsiteCompatibilityRequest,
    WebsiteVerifiedConfiguration as WebsiteConfigurationModel,
)


class DjangoWebsiteCompatibilityRepository:
    """Django ORM adapter for data owned by the public website."""

    def list_published(self) -> tuple[WebsiteVerifiedConfiguration, ...]:
        records = WebsiteConfigurationModel.objects.filter(is_published=True)
        return tuple(
            WebsiteVerifiedConfiguration(
                id=record.id,
                make=record.make,
                model=record.model,
                generation=record.generation,
                region=record.region,
                system_type=record.system_type,
                hardware_revision=record.hardware_revision,
                software_version=record.software_version,
                verified_at=record.verified_at,
                limitations=record.limitations,
            )
            for record in records
        )

    def submit(
        self, request: CompatibilityRequestInput
    ) -> SubmittedCompatibilityRequest:
        record = WebsiteCompatibilityRequest.objects.create(
            make=request.make,
            model=request.model,
            year=request.year,
            region=request.region,
            system_type=request.system_type,
            hardware_revision=request.hardware_revision,
            software_version=request.software_version,
            details=request.details,
            consent_accepted=request.consent_accepted,
        )
        return SubmittedCompatibilityRequest(
            id=record.id,
            status=record.status,
            created_at=record.created_at,
        )
