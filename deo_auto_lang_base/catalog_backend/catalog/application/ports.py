from typing import Protocol
from .dto import VehicleConfigurationSummary


class VerifiedConfigurationRepository(Protocol):
    def list_verified(self) -> tuple[VehicleConfigurationSummary, ...]:
        """Return only configurations that passed the review process."""

    def list_in_review(self) -> tuple[VehicleConfigurationSummary, ...]:
        """Return configurations explicitly placed in the public review queue."""
