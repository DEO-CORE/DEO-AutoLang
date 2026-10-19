from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class CompatibilityRequestInput:
    make: str
    model: str
    year: int | None
    region: str
    system_type: str
    hardware_revision: str
    software_version: str
    details: str
    consent_accepted: bool


@dataclass(frozen=True, slots=True)
class WebsiteVerifiedConfiguration:
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


@dataclass(frozen=True, slots=True)
class WebsiteCompatibilityCatalog:
    items: tuple[WebsiteVerifiedConfiguration, ...]
    updated_at: date | None


@dataclass(frozen=True, slots=True)
class SubmittedCompatibilityRequest:
    id: UUID
    status: str
    created_at: datetime
