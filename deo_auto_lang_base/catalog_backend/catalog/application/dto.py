from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class VehicleConfigurationSummary:
    id: str
    make: str
    model: str
    generation: str
    region: str
    system_type: str
    hardware_revision: str
    software_version: str
    verified_at: date | None
    limitations: str
    review_status: str = "verified"
    year_from: int | None = None
    year_to: int | None = None


@dataclass(frozen=True, slots=True)
class VerifiedCatalog:
    items: tuple[VehicleConfigurationSummary, ...]
    updated_at: date | None


@dataclass(frozen=True, slots=True)
class PublicVehicleCatalog:
    items: tuple[VehicleConfigurationSummary, ...]
    candidates: tuple[VehicleConfigurationSummary, ...]
    updated_at: date | None
