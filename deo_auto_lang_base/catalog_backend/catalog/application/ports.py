from typing import Protocol
from .dto import VerifiedConfiguration


class VerifiedConfigurationRepository(Protocol):
    def list_verified(self) -> tuple[VerifiedConfiguration, ...]:
        """Return only configurations that passed the review process."""
