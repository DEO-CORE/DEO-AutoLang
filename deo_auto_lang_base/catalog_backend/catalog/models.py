import hashlib
from django.core.exceptions import ValidationError
from django.db import models

from catalog.domain.policies import (
    configuration_verification_errors,
    firmware_approval_errors,
    firmware_file_errors,
)


def validate_firmware_file(upload):
    errors = firmware_file_errors(upload.name, upload.size)
    if errors:
        raise ValidationError(errors)


class VehicleConfiguration(models.Model):
    class ReviewStatus(models.TextChoices):
        DRAFT = "draft", "Черновик"
        TESTING = "testing", "На проверке"
        VERIFIED = "verified", "Проверено"
        REJECTED = "rejected", "Отклонено"

    id = models.SlugField("Идентификатор", primary_key=True, max_length=120)
    make = models.CharField("Марка", max_length=80)
    model = models.CharField("Модель", max_length=120)
    generation = models.CharField("Поколение", max_length=120, blank=True)
    year_from = models.PositiveSmallIntegerField("Год с", null=True, blank=True)
    year_to = models.PositiveSmallIntegerField("Год по", null=True, blank=True)
    region = models.CharField("Регион", max_length=80, blank=True)
    system_type = models.CharField("Тип мультимедиа", max_length=80)
    hardware_revision = models.CharField(
        "Аппаратная ревизия", max_length=120, blank=True
    )
    software_version = models.CharField("Версия ПО", max_length=120, blank=True)
    review_status = models.CharField(
        "Статус проверки",
        max_length=16,
        choices=ReviewStatus.choices,
        default=ReviewStatus.DRAFT,
    )
    verified_at = models.DateField("Дата проверки", null=True, blank=True)
    limitations = models.TextField("Ограничения", blank=True)
    evidence = models.TextField("Ссылка на протокол/доказательства", blank=True)
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        verbose_name = "Конфигурация автомобиля"
        verbose_name_plural = "Поддерживаемые автомобили"
        ordering = ["make", "model", "generation"]

    def __str__(self):
        return f"{self.make} {self.model} · {self.system_type}"

    def clean(self):
        if self.review_status == self.ReviewStatus.VERIFIED:
            missing = configuration_verification_errors(self.verified_at, self.evidence)
            if missing:
                raise ValidationError(
                    {
                        "review_status": "Для статуса «Проверено» заполните: "
                        + ", ".join(missing)
                        + "."
                    }
                )


class FirmwarePackage(models.Model):
    class ReviewStatus(models.TextChoices):
        QUARANTINE = "quarantine", "На проверке файла"
        APPROVED = "approved", "Одобрен"
        REVOKED = "revoked", "Отозван"

    id = models.SlugField("Идентификатор пакета", primary_key=True, max_length=120)
    name = models.CharField("Название", max_length=160)
    version = models.CharField("Версия", max_length=80)
    package_type = models.CharField("Тип пакета", max_length=40)
    file = models.FileField(
        "Файл прошивки",
        upload_to="firmware/%Y/%m/",
        validators=[validate_firmware_file],
    )
    sha256 = models.CharField("SHA-256", max_length=64, blank=True, editable=False)
    file_size = models.PositiveBigIntegerField(
        "Размер, байт", default=0, editable=False
    )
    review_status = models.CharField(
        "Статус пакета",
        max_length=16,
        choices=ReviewStatus.choices,
        default=ReviewStatus.QUARANTINE,
    )
    configurations = models.ManyToManyField(
        VehicleConfiguration,
        verbose_name="Совместимые конфигурации",
        related_name="firmware_packages",
        blank=True,
    )
    source = models.CharField("Источник", max_length=240, blank=True)
    notes = models.TextField("Примечания", blank=True)
    uploaded_at = models.DateTimeField("Загружено", auto_now_add=True)

    class Meta:
        verbose_name = "Пакет ПО"
        verbose_name_plural = "Прошивки и пакеты ПО"
        ordering = ["-uploaded_at"]

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            digest = hashlib.sha256()
            for chunk in self.file.chunks():
                digest.update(chunk)
            self.sha256 = digest.hexdigest()
        super().save(*args, **kwargs)

    def clean(self):
        if self.review_status == self.ReviewStatus.APPROVED:
            has_verified_configuration = (
                self.pk
                and self.configurations.filter(
                    review_status=VehicleConfiguration.ReviewStatus.VERIFIED
                ).exists()
            )
            errors = firmware_approval_errors(
                bool(self.sha256), bool(has_verified_configuration)
            )
            if errors:
                raise ValidationError({"review_status": errors})

    def __str__(self):
        return f"{self.name} · {self.version}"
