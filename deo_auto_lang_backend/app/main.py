from fastapi import FastAPI
from app.api.routes import router as compatibility_router

app = FastAPI(
    title="DEO AutoLang Platform API",
    description="Платформенный API. Публичный сайт использует отдельный Django backend.",
    version="0.1.0",
)
app.include_router(compatibility_router)


@app.get("/health", tags=["service"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "deo-auto-lang-backend"}
