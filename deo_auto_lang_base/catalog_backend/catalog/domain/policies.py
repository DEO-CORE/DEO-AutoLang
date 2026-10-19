from pathlib import Path


ALLOWED_FIRMWARE_EXTENSIONS = frozenset({".zip", ".bin", ".img", ".apk"})
MAX_FIRMWARE_SIZE_BYTES = 100 * 1024 * 1024


def firmware_file_errors(filename: str, size_bytes: int) -> tuple[str, ...]:
    errors = []
    if size_bytes > MAX_FIRMWARE_SIZE_BYTES:
        errors.append("Размер файла не должен превышать 100 МБ.")
    if Path(filename).suffix.lower() not in ALLOWED_FIRMWARE_EXTENSIONS:
        errors.append("Разрешены только ZIP, BIN, IMG или APK пакеты.")
    return tuple(errors)


def configuration_verification_errors(verified_at, evidence: str) -> tuple[str, ...]:
    missing = []
    if not verified_at:
        missing.append("дата проверки")
    if not evidence.strip():
        missing.append("доказательства проверки")
    return tuple(missing)


def firmware_approval_errors(
    checksum_exists: bool, has_verified_configuration: bool
) -> tuple[str, ...]:
    errors = []
    if not checksum_exists:
        errors.append("Сначала сохраните файл и рассчитайте его контрольную сумму.")
    if not has_verified_configuration:
        errors.append("Нужна хотя бы одна проверенная совместимая конфигурация.")
    return tuple(errors)
