from django.urls import path
from .views import CompatibilityListView, CompatibilityRequestCreateView

urlpatterns = [
    path(
        "compatibility/",
        CompatibilityListView.as_view(),
        name="site-compatibility-list",
    ),
    path(
        "compatibility-requests/",
        CompatibilityRequestCreateView.as_view(),
        name="site-compatibility-request-create",
    ),
]
