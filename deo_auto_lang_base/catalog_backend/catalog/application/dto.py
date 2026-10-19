from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class VerifiedConfiguration:
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
class VerifiedCatalog:
    items: tuple[VerifiedConfiguration, ...]
    updated_at: date | None
