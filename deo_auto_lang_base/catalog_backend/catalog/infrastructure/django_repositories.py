from catalog.application.dto import VehicleConfigurationSummary
from catalog.models import VehicleConfiguration


class DjangoVerifiedConfigurationRepository:
    def list_verified(self) -> tuple[VehicleConfigurationSummary, ...]:
        records = VehicleConfiguration.objects.filter(
            review_status=VehicleConfiguration.ReviewStatus.VERIFIED
        ).order_by("make", "model", "generation")
        return tuple(self._to_summary(record) for record in records)

    def list_in_review(self) -> tuple[VehicleConfigurationSummary, ...]:
        records = VehicleConfiguration.objects.filter(
            review_status=VehicleConfiguration.ReviewStatus.TESTING
        ).order_by("make", "model", "generation")
        return tuple(self._to_summary(record) for record in records)

    @staticmethod
    def _to_summary(record: VehicleConfiguration) -> VehicleConfigurationSummary:
        return VehicleConfigurationSummary(
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
            review_status=record.review_status,
            year_from=record.year_from,
            year_to=record.year_to,
        )
