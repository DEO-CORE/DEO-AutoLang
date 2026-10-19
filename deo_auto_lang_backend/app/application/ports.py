from typing import Protocol


class VerifiedCatalogGateway(Protocol):
    def fetch(self) -> dict[str, object]:
        """Fetch the verified platform catalog from its owning service."""
