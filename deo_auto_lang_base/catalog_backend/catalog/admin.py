from django.contrib import admin
from .models import FirmwarePackage, VehicleConfiguration


@admin.register(VehicleConfiguration)
class VehicleConfigurationAdmin(admin.ModelAdmin):
    list_display = (
        "make",
        "model",
        "generation",
        "system_type",
        "review_status",
        "verified_at",
    )
    list_filter = ("review_status", "region", "system_type")
    search_fields = (
        "id",
        "make",
        "model",
        "generation",
        "hardware_revision",
        "software_version",
    )
    readonly_fields = ("created_at", "updated_at")
    actions = ("move_to_review",)
    fieldsets = (
        (
            "Автомобиль",
            {
                "fields": (
                    "id",
                    "make",
                    "model",
                    "generation",
                    "year_from",
                    "year_to",
                    "region",
                )
            },
        ),
        (
            "Система",
            {"fields": ("system_type", "hardware_revision", "software_version")},
        ),
        (
            "Проверка",
            {
                "fields": (
                    "review_status",
                    "verified_at",
                    "limitations",
                    "evidence",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.action(description="Перевести черновики в статус «На проверке»")
    def move_to_review(self, request, queryset):
        updated = queryset.filter(
            review_status=VehicleConfiguration.ReviewStatus.DRAFT
        ).update(review_status=VehicleConfiguration.ReviewStatus.TESTING)
        self.message_user(request, f"Переведено на проверку: {updated}.")


@admin.register(FirmwarePackage)
class FirmwarePackageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "version",
        "package_type",
        "review_status",
        "file_size",
        "uploaded_at",
    )
    list_filter = ("review_status", "package_type", "uploaded_at")
    search_fields = ("id", "name", "version", "sha256", "source")
    filter_horizontal = ("configurations",)
    readonly_fields = ("sha256", "file_size", "uploaded_at")
    fieldsets = (
        (
            "Пакет",
            {
                "fields": (
                    "id",
                    "name",
                    "version",
                    "package_type",
                    "file",
                    "sha256",
                    "file_size",
                    "review_status",
                )
            },
        ),
        (
            "Связи и источник",
            {"fields": ("configurations", "source", "notes", "uploaded_at")},
        ),
    )
