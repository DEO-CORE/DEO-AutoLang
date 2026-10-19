# Backend сайта

`backend_side/` — изолированный backend только для публичного React-сайта. Он использует Django, Django REST Framework и Jazzmin, а его SQLite-база находится в `backend_side/db.sqlite3`.

Сайт обращается к этому сервису по `/site-api/` для отправки и обработки заявок. Каталог автомобилей сайта загружается напрямую из публичного read-only API `deo_auto_lang_base/catalog_backend/`; единственный источник опубликованных конфигураций — Django/Jazzmin-админка каталога. В админке сайта остаются только заявки. Backend сайта не владеет данными автомобилей и не получает внутренний ключ каталога.

**Этот проект не подключается к платформе.** Он не импортирует FastAPI-код, не обращается к API платформы, её базе или файловому хранилищу. `deo_auto_lang_backend/` — отдельный FastAPI backend платформы.

## Локальный запуск

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:4179
```

Админка: `http://127.0.0.1:4179/admin/`. Сервис намеренно привязывается к loopback для локальной разработки. Перед размещением в интернете нужно отдельно настроить секреты, HTTPS, ограничение запросов на прокси, резервное копирование, хранение и сроки удаления данных.
