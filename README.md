# DEO AutoLang monorepo

DEO AutoLang is split into independently deployable applications with explicit data ownership. The public website backend has no integration with the platform. Platform compatibility and firmware records are owned by a separate Django catalog service; FastAPI consumes its authenticated internal read API.

## Project map

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for data ownership, dependency rules, and service boundaries.

- `frontend_site/` — existing public React/Vite website.
- `deo_auto_lang_app/` — Kotlin Multiplatform + Compose Desktop client. The first screen discovers ADB devices in read-only mode.
- `deo_auto_lang_base/src/` — shared Kotlin compatibility models and exact-match rules.
- `deo_auto_lang_base/catalog_backend/` — authoritative Django database and Jazzmin admin for supported vehicle configurations and firmware packages. The platform API reads verified catalog entries through its internal service endpoint.
- `backend_side/` — Django + DRF + Jazzmin backend used only by the public website. It has its own database, website requests, and separately curated public catalog; it never calls or reads the platform.
- `deo_auto_lang_backend/` — FastAPI backend for platform APIs. It is not called by the public website.
- `deo_auto_lang_console_app/` — planned curator/reviewer console; publishing is intentionally not exposed yet.
- `deo_auto_lang_base/contracts/openapi.yaml` — initial API contract.

## Run the web MVP locally

```sh
pnpm --dir frontend_site install
python3 -m venv backend_side/.venv
backend_side/.venv/bin/pip install -r backend_side/requirements.txt
backend_side/.venv/bin/python backend_side/manage.py migrate
python3 -m venv deo_auto_lang_backend/.venv
deo_auto_lang_backend/.venv/bin/pip install -r deo_auto_lang_backend/requirements.txt
python3 -m venv deo_auto_lang_base/catalog_backend/.venv
deo_auto_lang_base/catalog_backend/.venv/bin/pip install -r deo_auto_lang_base/catalog_backend/requirements.txt
deo_auto_lang_base/catalog_backend/.venv/bin/python deo_auto_lang_base/catalog_backend/manage.py migrate
pnpm dev
```

This starts React on `http://127.0.0.1:5173/`, the website-only Django API/admin on `http://127.0.0.1:4179/`, platform FastAPI on `http://127.0.0.1:4178/`, and the catalog service on `http://127.0.0.1:4180/`. Vite proxies `/site-api/` to the website backend and `/catalog-api/` to the catalog's public, read-only compatibility endpoint. The public website shows verified configurations and, separately, records explicitly marked “На проверке”; request submissions remain owned by the website backend. FastAPI continues to read only verified configurations through its separate internal service endpoint. `pnpm build` builds the public website.

To add the initial candidate set to a development catalog, run `deo_auto_lang_base/catalog_backend/.venv/bin/python deo_auto_lang_base/catalog_backend/manage.py seed_supported_vehicles`. The command is idempotent and creates eight entries in “На проверке”; it does not mark them compatible.

Create separate administrators with `backend_side/.venv/bin/python backend_side/manage.py createsuperuser` and `deo_auto_lang_base/catalog_backend/.venv/bin/python deo_auto_lang_base/catalog_backend/manage.py createsuperuser`. Website: `/admin/` on port 4179. Platform vehicle/firmware base: `/admin/` on port 4180. Never publish firmware file storage as static website assets.

The website backend and platform base each have their own SQLite database, migrations, credentials, and Jazzmin admin. FastAPI is a platform-facing API and does not own the vehicle/firmware catalog. Neither stack is production configured; do not expose development servers publicly. Set independent strong production secrets and a non-default `BASE_CATALOG_SERVICE_KEY` before deployment.

This is the first MVP foundation, not a release candidate. The desktop client currently discovers ADB devices and reads basic Android properties. Verified compatibility remains empty until an exact multimedia configuration and localization procedure are reviewed. Session history, PDF reports, role-protected console workflows, and a verified localization procedure remain future milestones.

## Desktop client

The desktop foundation uses Gradle and Kotlin Multiplatform. Install a JDK and Gradle, then run `gradle :deo_auto_lang_app:run` from this directory. Build verification cannot run on machines without a Java runtime.

Device writing and firmware operations are not part of this MVP. A confirmed test configuration and reviewed recovery procedure are required before any write capability is introduced.

## Website SEO

Set `VITE_SITE_URL` to the public HTTPS origin before building the site. Canonicals and the sitemap are generated from the route list; the domain is intentionally not hard-coded.
