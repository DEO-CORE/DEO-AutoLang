from .ports import VerifiedCatalogGateway


class ConfigurationNotFound(LookupError):
    pass


class GetVerifiedCatalog:
    def __init__(self, gateway: VerifiedCatalogGateway) -> None:
        self._gateway = gateway

    def execute(self) -> dict[str, object]:
        return self._gateway.fetch()


class GetVerifiedConfiguration:
    def __init__(self, gateway: VerifiedCatalogGateway) -> None:
        self._gateway = gateway

    def execute(self, configuration_id: str) -> dict[str, object]:
        catalog = self._gateway.fetch()
        configuration = next(
            (
                item
                for item in catalog.get("items", [])
                if item.get("id") == configuration_id
            ),
            None,
        )
        if configuration is None:
            raise ConfigurationNotFound(configuration_id)
        return configuration
