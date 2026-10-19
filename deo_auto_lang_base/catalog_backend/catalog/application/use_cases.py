from .dto import VerifiedCatalog
from .ports import VerifiedConfigurationRepository


class ListVerifiedConfigurations:
    def __init__(self, repository: VerifiedConfigurationRepository) -> None:
        self._repository = repository

    def execute(self) -> VerifiedCatalog:
        items = self._repository.list_verified()
        verified_dates = [item.verified_at for item in items if item.verified_at]
        return VerifiedCatalog(
            items=items, updated_at=max(verified_dates, default=None)
        )
