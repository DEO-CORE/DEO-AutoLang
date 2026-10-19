import json
from urllib.error import URLError
from urllib.request import Request, urlopen


class CatalogUnavailable(RuntimeError):
    """The catalog owner could not be reached or returned an invalid response."""


class BaseCatalogHttpGateway:
    def __init__(self, base_url: str, service_key: str, timeout_seconds: float = 3.0):
        self._base_url = base_url
        self._service_key = service_key
        self._timeout_seconds = timeout_seconds

    def fetch(self) -> dict[str, object]:
        request = Request(
            self._base_url,
            headers={"X-Base-Catalog-Key": self._service_key},
        )
        try:
            with urlopen(request, timeout=self._timeout_seconds) as response:
                result = json.loads(response.read().decode("utf-8"))
        except (URLError, TimeoutError, json.JSONDecodeError) as error:
            raise CatalogUnavailable from error
        items = result.get("items") if isinstance(result, dict) else None
        if not isinstance(items, list) or any(
            not isinstance(item, dict) for item in items
        ):
            raise CatalogUnavailable(
                "Catalog response did not match the expected contract."
            )
        return result
