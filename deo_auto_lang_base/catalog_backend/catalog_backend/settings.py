import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = os.environ.get("BASE_DJANGO_DEBUG", "1") == "1"
SECRET_KEY = os.environ.get("BASE_DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if not DEBUG:
        raise RuntimeError(
            "BASE_DJANGO_SECRET_KEY must be set when BASE_DJANGO_DEBUG is disabled."
        )
    SECRET_KEY = "local-development-only-change-before-deploy"
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "BASE_DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost"
    ).split(",")
    if host.strip()
]
INSTALLED_APPS = [
    "jazzmin",
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "catalog",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "catalog_backend.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "catalog_backend.wsgi.application"
ASGI_APPLICATION = "catalog_backend.asgi.application"
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    import dj_database_url

    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL, conn_max_age=0, ssl_require=True
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "catalog.sqlite3",
        },
    }
MEDIA_ROOT = BASE_DIR / "private_media"
MEDIA_URL = "/private-media/"
DATA_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "ru"
TIME_ZONE = "Asia/Bishkek"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("BASE_DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
BASE_CATALOG_SERVICE_KEY = os.environ.get(
    "BASE_CATALOG_SERVICE_KEY",
    "local-dev-platform-only-key" if DEBUG else "",
)
if not BASE_CATALOG_SERVICE_KEY:
    raise RuntimeError(
        "BASE_CATALOG_SERVICE_KEY must be set outside local development."
    )

CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in (
        os.environ.get("BASE_CORS_ALLOWED_ORIGINS")
        or "https://autolang.deo-core.codes,http://localhost:5173,http://127.0.0.1:5173"
    ).split(",")
    if origin.strip()
]

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
}
JAZZMIN_SETTINGS = {
    "site_title": "DEO AutoLang · База",
    "site_header": "DEO AutoLang",
    "site_brand": "База автомобилей и ПО",
    "welcome_sign": "Управление проверенными конфигурациями и пакетами",
    "show_ui_builder": False,
}
