package com.deoautolang.app

import java.util.concurrent.TimeUnit

data class AdbDevice(val serial: String, val state: String, val description: String = "") {
    val ready: Boolean get() = state == "device"
    val statusLabel: String get() = when (state) {
        "device" -> "Готово к чтению"
        "unauthorized" -> "Нужно разрешение на экране устройства"
        "offline" -> "Устройство не отвечает"
        else -> state
    }
}

data class DeviceScanResult(val devices: List<AdbDevice>, val message: String)

class AdbDiscovery {
    fun scan(): DeviceScanResult {
        val output = runAdb(listOf("devices", "-l")) ?: return DeviceScanResult(
            emptyList(), "ADB не найден или не отвечает. Установите Android Platform Tools и повторите попытку.",
        )
        val devices = output.lineSequence().drop(1).mapNotNull { line ->
            val parts = line.trim().split(Regex("\\s+"))
            if (parts.size < 2 || parts[0].isBlank()) return@mapNotNull null
            AdbDevice(parts[0], parts[1], parts.drop(2).joinToString(" "))
        }.toList()
        return when {
            devices.isEmpty() -> DeviceScanResult(emptyList(), "Устройства не обнаружены. Проверьте кабель, режим USB и доступность ADB.")
            devices.any { it.ready } -> DeviceScanResult(devices, "Найдено устройств: ${devices.size}. Доступные устройства готовы к безопасному чтению.")
            else -> DeviceScanResult(devices, "Устройство найдено, но для диагностики требуется состояние «Готово к чтению».")
        }
    }

    fun readBasicProperties(serial: String): Map<String, String> {
        val propertyNames = listOf(
            "ro.product.manufacturer" to "Производитель устройства",
            "ro.product.model" to "Модель устройства",
            "ro.build.version.release" to "Версия Android",
            "ro.build.fingerprint" to "Отпечаток сборки",
        )
        return propertyNames.mapNotNull { (property, label) ->
            val value = runAdb(listOf("-s", serial, "shell", "getprop", property))?.trim()?.takeIf { it.isNotBlank() }
            value?.let { label to it }
        }.toMap()
    }

    private fun runAdb(arguments: List<String>): String? = try {
        val process = ProcessBuilder(listOf("adb") + arguments).redirectErrorStream(true).start()
        if (!process.waitFor(4, TimeUnit.SECONDS)) {
            process.destroyForcibly()
            null
        } else if (process.exitValue() != 0) null else process.inputStream.bufferedReader().use { it.readText() }
    } catch (_: Exception) {
        null
    }
}
