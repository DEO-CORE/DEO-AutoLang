from typing import Protocol
from .dto import (
    CompatibilityRequestInput,
    SubmittedCompatibilityRequest,
    WebsiteVerifiedConfiguration,
)


class WebsiteCompatibilityRepository(Protocol):
    def list_published(self) -> tuple[WebsiteVerifiedConfiguration, ...]: ...

    def submit(
        self, request: CompatibilityRequestInput
    ) -> SubmittedCompatibilityRequest: ...
