from django.contrib import admin
from .models import WebsiteCompatibilityRequest


@admin.register(WebsiteCompatibilityRequest)
class WebsiteCompatibilityRequestAdmin(admin.ModelAdmin):
    list_display = ("created_at", "make", "model", "year", "status")
    list_filter = ("status", "system_type", "created_at")
    search_fields = ("make", "model", "region", "hardware_revision", "software_version")
    readonly_fields = ("id", "created_at", "consent_accepted")
    ordering = ("-created_at",)
    fieldsets = (
        ("Обращение", {"fields": ("id", "created_at", "status", "consent_accepted")}),
        (
            "Конфигурация",
            {
                "fields": (
                    "make",
                    "model",
                    "year",
                    "region",
                    "system_type",
                    "hardware_revision",
                    "software_version",
                    "details",
                )
            },
        ),
    )
