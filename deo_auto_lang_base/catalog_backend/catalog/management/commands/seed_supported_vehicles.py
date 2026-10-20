from django.core.management.base import BaseCommand

from catalog.models import VehicleConfiguration


STARTER_VEHICLES = (
    {
        "id": "starter-toyota-camry-xv70",
        "make": "Toyota",
        "model": "Camry",
        "generation": "XV70",
        "year_from": 2017,
        "year_to": 2023,
    },
    {
        "id": "starter-toyota-rav4-xa50",
        "make": "Toyota",
        "model": "RAV4",
        "generation": "XA50",
        "year_from": 2018,
        "year_to": 2025,
    },
    {
        "id": "starter-lexus-rx-al20",
        "make": "Lexus",
        "model": "RX",
        "generation": "AL20",
        "year_from": 2015,
        "year_to": 2022,
    },
    {
        "id": "starter-hyundai-tucson-nx4",
        "make": "Hyundai",
        "model": "Tucson",
        "generation": "NX4",
        "year_from": 2020,
        "year_to": 2025,
    },
    {
        "id": "starter-kia-sportage-nq5",
        "make": "Kia",
        "model": "Sportage",
        "generation": "NQ5",
        "year_from": 2021,
        "year_to": 2025,
    },
    {
        "id": "starter-geely-monjaro",
        "make": "Geely",
        "model": "Monjaro",
        "generation": "KX11",
        "year_from": 2021,
        "year_to": 2025,
    },
    {
        "id": "starter-chery-tiggo-8-pro",
        "make": "Chery",
        "model": "Tiggo 8 Pro",
        "generation": "",
        "year_from": 2021,
        "year_to": 2025,
    },
    {
        "id": "starter-haval-jolion",
        "make": "Haval",
        "model": "Jolion",
        "generation": "",
        "year_from": 2020,
        "year_to": 2025,
    },
)


class Command(BaseCommand):
    help = "Создать начальные записи автомобилей со статусом «На проверке»."

    def handle(self, *args, **options):
        created_count = 0
        existing_count = 0

        for vehicle in STARTER_VEHICLES:
            _, created = VehicleConfiguration.objects.get_or_create(
                id=vehicle["id"],
                defaults={
                    **vehicle,
                    "region": "",
                    "system_type": "Не идентифицирована",
                    "hardware_revision": "",
                    "software_version": "",
                    "review_status": VehicleConfiguration.ReviewStatus.TESTING,
                    "limitations": (
                        "Начальная запись для проверки. Совместимость и возможность "
                        "русификации не подтверждены. Заполните точную конфигурацию "
                        "мультимедиа и приложите доказательства проверки."
                    ),
                },
            )
            if created:
                created_count += 1
            else:
                existing_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Добавлено записей на проверку: {created_count}; "
                f"уже существовало: {existing_count}."
            )
        )
