from .dto import (
    CompatibilityRequestInput,
    SubmittedCompatibilityRequest,
    WebsiteCompatibilityCatalog,
    WebsiteVerifiedConfiguration,
)
from .ports import WebsiteCompatibilityRepository


class ConsentRequiredError(ValueError):
    pass


class ListWebsiteConfigurations:
    def __init__(self, repository: WebsiteCompatibilityRepository) -> None:
        self._repository = repository

    def execute(self) -> WebsiteCompatibilityCatalog:
        items = self._repository.list_published()
        verified_dates = [item.verified_at for item in items if item.verified_at]
        return WebsiteCompatibilityCatalog(
            items=items, updated_at=max(verified_dates, default=None)
        )


class SubmitWebsiteCompatibilityRequest:
    def __init__(self, repository: WebsiteCompatibilityRepository) -> None:
        self._repository = repository

    def execute(
        self, request: CompatibilityRequestInput
    ) -> SubmittedCompatibilityRequest:
        if not request.consent_accepted:
            raise ConsentRequiredError("Согласие на сохранение заявки обязательно.")
        return self._repository.submit(request)
