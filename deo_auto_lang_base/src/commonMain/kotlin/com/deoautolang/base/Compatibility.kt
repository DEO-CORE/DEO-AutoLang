package com.deoautolang.base

enum class CompatibilityStatus {
    VERIFIED,
    REQUIRES_REVIEW,
    INSUFFICIENT_DATA,
    NOT_SUPPORTED,
    CHECK_FAILED,
}

enum class MediaType {
    FACTORY_ANDROID,
    AFTERMARKET_ANDROID,
    UNKNOWN,
}

enum class DataSource {
    DEVICE,
    CATALOG,
    MANUAL,
    UNCONFIRMED,
}

data class SourcedValue(
    val value: String,
    val source: DataSource,
    val confidence: Float? = null,
)

data class VehicleProfile(
    val make: SourcedValue? = null,
    val model: SourcedValue? = null,
    val generation: SourcedValue? = null,
    val region: SourcedValue? = null,
    val mediaType: MediaType = MediaType.UNKNOWN,
    val hardwareRevision: SourcedValue? = null,
    val softwareVersion: SourcedValue? = null,
    val buildFingerprint: SourcedValue? = null,
)

data class CompatibilityRecord(
    val id: String,
    val make: String,
    val model: String,
    val generation: String,
    val region: String,
    val mediaType: MediaType,
    val hardwareRevision: String,
    val softwareVersion: String,
    val procedureVersion: String,
    val packageChecksum: String,
    val status: CompatibilityStatus,
    val verifiedAt: String?,
    val limitations: List<String> = emptyList(),
)

data class CompatibilityDecision(
    val status: CompatibilityStatus,
    val reason: String,
    val matchedRecord: CompatibilityRecord? = null,
)

/** Only an exact published match is allowed to produce VERIFIED. */
class CompatibilityMatcher {
    fun evaluate(profile: VehicleProfile, records: List<CompatibilityRecord>): CompatibilityDecision {
        val required = listOf(
            "марка" to profile.make,
            "модель" to profile.model,
            "поколение" to profile.generation,
            "регион" to profile.region,
            "аппаратная ревизия" to profile.hardwareRevision,
            "версия ПО" to profile.softwareVersion,
        )
        val missing = required.filter { (_, value) -> value?.value.isNullOrBlank() }.map { it.first }
        if (profile.mediaType == MediaType.UNKNOWN) {
            return CompatibilityDecision(CompatibilityStatus.INSUFFICIENT_DATA, "Не определён тип мультимедиа.")
        }
        if (missing.isNotEmpty()) {
            return CompatibilityDecision(
                CompatibilityStatus.INSUFFICIENT_DATA,
                "Не хватает данных: ${missing.joinToString()}.",
            )
        }

        val exactRecord = records.firstOrNull { record ->
            record.make.equals(profile.make!!.value, ignoreCase = true) &&
                record.model.equals(profile.model!!.value, ignoreCase = true) &&
                record.generation.equals(profile.generation!!.value, ignoreCase = true) &&
                record.region.equals(profile.region!!.value, ignoreCase = true) &&
                record.mediaType == profile.mediaType &&
                record.hardwareRevision.equals(profile.hardwareRevision!!.value, ignoreCase = true) &&
                record.softwareVersion.equals(profile.softwareVersion!!.value, ignoreCase = true)
        }
        return when (exactRecord?.status) {
            CompatibilityStatus.VERIFIED -> {
                if (exactRecord.procedureVersion.isBlank() || exactRecord.packageChecksum.isBlank() || exactRecord.verifiedAt.isNullOrBlank()) {
                    CompatibilityDecision(CompatibilityStatus.CHECK_FAILED, "В записи не хватает версии процедуры, контрольной суммы пакета или даты проверки.", exactRecord)
                } else {
                    CompatibilityDecision(CompatibilityStatus.VERIFIED, "Найдено точное опубликованное совпадение.", exactRecord)
                }
            }
            CompatibilityStatus.NOT_SUPPORTED -> CompatibilityDecision(CompatibilityStatus.NOT_SUPPORTED, "Эта точная конфигурация исключена из поддержки.", exactRecord)
            CompatibilityStatus.CHECK_FAILED -> CompatibilityDecision(CompatibilityStatus.CHECK_FAILED, "Последняя проверка конфигурации не пройдена.", exactRecord)
            else -> CompatibilityDecision(
                CompatibilityStatus.REQUIRES_REVIEW,
                "Точного опубликованного совпадения нет. Изменяющие действия недоступны.",
                exactRecord,
            )
        }
    }
}
