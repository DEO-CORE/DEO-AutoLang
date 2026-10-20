from .dto import PublicVehicleCatalog, VerifiedCatalog
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


class ListPublicVehicleCatalog:
    def __init__(self, repository: VerifiedConfigurationRepository) -> None:
        self._repository = repository

    def execute(self) -> PublicVehicleCatalog:
        items = self._repository.list_verified()
        candidates = self._repository.list_in_review()
        verified_dates = [item.verified_at for item in items if item.verified_at]
        return PublicVehicleCatalog(
            items=items,
            candidates=candidates,
            updated_at=max(verified_dates, default=None),
        )
