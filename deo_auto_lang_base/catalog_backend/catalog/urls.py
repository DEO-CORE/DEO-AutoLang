from django.urls import path
from .views import PlatformVerifiedCatalogView

urlpatterns = [
    path(
        "platform/verified-configurations/",
        PlatformVerifiedCatalogView.as_view(),
        name="platform-verified-catalog",
    )
]
