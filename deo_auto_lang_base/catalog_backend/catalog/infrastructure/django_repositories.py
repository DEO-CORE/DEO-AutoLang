from catalog.application.dto import VerifiedConfiguration
from catalog.models import VehicleConfiguration


class DjangoVerifiedConfigurationRepository:
    def list_verified(self) -> tuple[VerifiedConfiguration, ...]:
        records = VehicleConfiguration.objects.filter(
            review_status=VehicleConfiguration.ReviewStatus.VERIFIED
        ).order_by("make", "model", "generation")
        return tuple(
            VerifiedConfiguration(
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
