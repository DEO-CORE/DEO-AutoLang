import uuid
from django.db import models


class WebsiteVerifiedConfiguration(models.Model):
    """Website-owned public catalog. Publishing requires a manual technical review."""

    id = models.SlugField(primary_key=True, max_length=120)
    make = models.CharField("Марка", max_length=80)
    model = models.CharField("Модель", max_length=120)
    generation = models.CharField("Поколение", max_length=120, blank=True)
    region = models.CharField("Регион", max_length=80, blank=True)
    system_type = models.CharField("Тип системы", max_length=80)
    hardware_revision = models.CharField(
        "Аппаратная ревизия", max_length=120, blank=True
    )
    software_version = models.CharField("Версия ПО", max_length=120, blank=True)
    verified_at = models.DateField("Дата проверки", null=True, blank=True)
    limitations = models.TextField("Ограничения", blank=True)
    is_published = models.BooleanField("Опубликовано", default=False)

    class Meta:
        verbose_name = "Проверенная конфигурация сайта"
        verbose_name_plural = "Каталог совместимости сайта"
        ordering = ["make", "model", "generation"]

    def __str__(self):
        return f"{self.make} {self.model} · {self.system_type}"


class WebsiteCompatibilityRequest(models.Model):
    class Status(models.TextChoices):
        RECEIVED = "received", "Получена"
        REVIEWING = "reviewing", "На проверке"
        ANSWERED = "answered", "Обработана"
        CLOSED = "closed", "Закрыта"

    id = models.UUIDField(
        "Номер заявки", primary_key=True, default=uuid.uuid4, editable=False
    )
    created_at = models.DateTimeField("Получена", auto_now_add=True)
    status = models.CharField(
        "Статус", max_length=20, choices=Status.choices, default=Status.RECEIVED
    )
    make = models.CharField("Марка", max_length=80)
    model = models.CharField("Модель", max_length=120)
    year = models.PositiveSmallIntegerField("Год", null=True, blank=True)
    region = models.CharField("Регион", max_length=80, blank=True)
    system_type = models.CharField("Тип мультимедиа", max_length=20, blank=True)
    hardware_revision = models.CharField(
        "Аппаратная ревизия", max_length=120, blank=True
    )
    software_version = models.CharField("Версия ПО", max_length=120, blank=True)
    details = models.TextField("Дополнительные сведения", blank=True)
    consent_accepted = models.BooleanField("Согласие на обработку", default=False)

    class Meta:
        verbose_name = "Заявка с сайта"
        verbose_name_plural = "Заявки сайта"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.make} {self.model} · {self.get_status_display()}"
