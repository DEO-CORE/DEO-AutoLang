package com.deoautolang.base

data class DiagnosticSession(
    val id: String,
    val createdAt: String,
    val appVersion: String,
    val profile: VehicleProfile,
    val compatibility: CompatibilityDecision,
    val events: List<SessionEvent> = emptyList(),
)

data class SessionEvent(
    val occurredAt: String,
    val code: String,
    val message: String,
    val isError: Boolean = false,
)
