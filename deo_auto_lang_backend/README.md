# FastAPI платформы

Этот сервис предоставляет API платформе DEO AutoLang. Он не является backend публичного сайта и не принимает заявки с сайта.

FastAPI получает только проверенные конфигурации из `deo_auto_lang_base/catalog_backend/` по внутреннему API с заголовком `X-Base-Catalog-Key`. Он не владеет базой автомобилей или файлами прошивок. Загрузка и хранение firmware package принадлежат Django-базе платформы.

Локальный запуск из корня проекта после установки зависимостей (для локальной разработки задайте временный ключ; не используйте его при публикации):

```sh
BASE_CATALOG_SERVICE_KEY=local-dev-platform-only-key deo_auto_lang_backend/.venv/bin/python -m uvicorn app.main:app --app-dir deo_auto_lang_backend --host 127.0.0.1 --port 4178
```

Сервис разработки привязан к loopback. Для production потребуются TLS, отдельные production credentials и ограничение доступа между сервисами.
