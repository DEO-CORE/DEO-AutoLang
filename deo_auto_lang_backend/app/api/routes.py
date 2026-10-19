import os
from fastapi import APIRouter, Depends, HTTPException

from app.application.ports import VerifiedCatalogGateway
from app.application.use_cases import (
    ConfigurationNotFound,
    GetVerifiedCatalog,
    GetVerifiedConfiguration,
)
from app.infrastructure.base_catalog_http import (
    BaseCatalogHttpGateway,
    CatalogUnavailable,
)

router = APIRouter(prefix="/api/v1", tags=["compatibility"])


def get_catalog_gateway() -> VerifiedCatalogGateway:
    service_key = os.environ.get("BASE_CATALOG_SERVICE_KEY")
    if not service_key:
        raise HTTPException(
            status_code=503, detail="platform_catalog_credentials_missing"
        )
    return BaseCatalogHttpGateway(
        base_url=os.environ.get(
            "BASE_CATALOG_URL",
            "http://127.0.0.1:4180/internal/platform/verified-configurations/",
        ),
        service_key=service_key,
    )


def catalog_response(gateway: VerifiedCatalogGateway):
    try:
        return GetVerifiedCatalog(gateway).execute()
    except CatalogUnavailable as error:
        raise HTTPException(
            status_code=503, detail="platform_catalog_unavailable"
        ) from error


@router.get("/compatibility")
def compatibility_list(
    gateway: VerifiedCatalogGateway = Depends(get_catalog_gateway),
) -> dict[str, object]:
    return catalog_response(gateway)


@router.get("/compatibility/{configuration_id}")
def compatibility_detail(
    configuration_id: str,
    gateway: VerifiedCatalogGateway = Depends(get_catalog_gateway),
) -> dict[str, object]:
    try:
        return GetVerifiedConfiguration(gateway).execute(configuration_id)
    except ConfigurationNotFound as error:
        raise HTTPException(
            status_code=404, detail="configuration_not_found"
        ) from error
    except CatalogUnavailable as error:
        raise HTTPException(
            status_code=503, detail="platform_catalog_unavailable"
        ) from error
