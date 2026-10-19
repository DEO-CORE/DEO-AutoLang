package com.deoautolang.app

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application
import androidx.compose.ui.window.rememberWindowState
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

private val Graphite = Color(0xFF101820)
private val Slate = Color(0xFF1B2A34)
private val Teal = Color(0xFF00BFA6)
private val Amber = Color(0xFFFFB547)
private val Paper = Color(0xFFF4F7F8)
private val Muted = Color(0xFFB5C1C6)

fun main() = application {
    Window(onCloseRequest = ::exitApplication, title = "DEO AutoLang", state = rememberWindowState(width = 1180.dp, height = 800.dp)) {
        MaterialTheme(colorScheme = darkColorScheme(primary = Teal, background = Graphite, surface = Slate)) {
            Dashboard()
        }
    }
}

@Composable
private fun Dashboard() {
    var devices by remember { mutableStateOf<List<AdbDevice>>(emptyList()) }
    var notice by remember { mutableStateOf("Сначала подключите Android-систему с разрешённым ADB.") }
    var scanning by remember { mutableStateOf(false) }
    var inspectingSerial by remember { mutableStateOf<String?>(null) }
    var inspectedSerial by remember { mutableStateOf<String?>(null) }
    var deviceInfo by remember { mutableStateOf<Map<String, String>>(emptyMap()) }
    val scope = rememberCoroutineScope()

    Row(Modifier.fillMaxSize().background(Graphite)) {
        Column(Modifier.width(230.dp).fillMaxHeight().background(Slate).padding(24.dp)) {
            Text("DEO", color = Paper, fontSize = 21.sp)
            Text("AUTOLANG / MVP", color = Teal, fontSize = 10.sp)
            Spacer(Modifier.height(42.dp))
            Text("РАБОЧЕЕ МЕСТО", color = Muted, fontSize = 10.sp)
            Spacer(Modifier.height(18.dp))
            Text("Новая диагностика", color = Paper)
            Spacer(Modifier.height(12.dp))
            Text("История сессий", color = Muted)
            Spacer(Modifier.height(12.dp))
            Text("Каталог", color = Muted)
            Spacer(Modifier.weight(1f))
            Text("Только безопасное чтение", color = Teal, fontSize = 11.sp)
        }

        Column(Modifier.fillMaxSize().padding(horizontal = 38.dp, vertical = 30.dp)) {
            Text("Новое подключение", color = Paper, fontSize = 28.sp)
            Spacer(Modifier.height(8.dp))
            Text("Обнаружение Android через доступный ADB-интерфейс", color = Muted)
            Spacer(Modifier.height(28.dp))
            Card(colors = CardDefaults.cardColors(containerColor = Slate), shape = RoundedCornerShape(14.dp)) {
                Column(Modifier.fillMaxWidth().padding(24.dp)) {
                    Text("УСТРОЙСТВА", color = Teal, fontSize = 10.sp)
                    Spacer(Modifier.height(12.dp))
                    Text(notice, color = Paper)
                    if (devices.isNotEmpty()) {
                        Spacer(Modifier.height(14.dp))
                        devices.forEach { device ->
                            Column(Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
                                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                    Text(device.serial, color = Paper)
                                    Text(device.statusLabel, color = if (device.ready) Teal else Amber)
                                }
                                if (device.description.isNotBlank()) Text(device.description, color = Muted, fontSize = 10.sp)
                                if (device.ready) {
                                    Button(
                                        enabled = inspectingSerial != device.serial,
                                        onClick = {
                                            inspectingSerial = device.serial
                                            scope.launch {
                                                deviceInfo = withContext(Dispatchers.IO) { AdbDiscovery().readBasicProperties(device.serial) }
                                                inspectedSerial = device.serial
                                                inspectingSerial = null
                                            }
                                        },
                                        colors = ButtonDefaults.buttonColors(containerColor = Slate, contentColor = Teal),
                                    ) { Text(if (inspectingSerial == device.serial) "Читаем…" else "Прочитать базовые сведения") }
                                }
                                if (inspectingSerial == null && inspectedSerial == device.serial && deviceInfo.isNotEmpty()) {
                                    deviceInfo.forEach { (label, value) ->
                                        Row(Modifier.fillMaxWidth().padding(vertical = 2.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                                            Text(label, color = Muted, fontSize = 11.sp)
                                            Text(value, color = Paper, fontSize = 11.sp)
                                        }
                                    }
                                }
                            }
                        }
                    }
                    Spacer(Modifier.height(20.dp))
                    Button(
                        enabled = !scanning,
                        onClick = {
                            scanning = true
                            deviceInfo = emptyMap()
                            inspectedSerial = null
                            scope.launch {
                                val result = withContext(Dispatchers.IO) { AdbDiscovery().scan() }
                                devices = result.devices
                                notice = result.message
                                scanning = false
                            }
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Teal, contentColor = Graphite),
                    ) { Text(if (scanning) "Проверяем…" else "Обнаружить устройства") }
                }
            }
            Spacer(Modifier.height(18.dp))
            Card(colors = CardDefaults.cardColors(containerColor = Color(0xFF2B281F)), shape = RoundedCornerShape(12.dp)) {
                Text(
                    "Режим MVP: обнаружение устройств и чтение доступных идентификаторов. Запись, прошивка и изменение системных файлов отключены.",
                    Modifier.padding(18.dp), color = Color(0xFFFFD58F), fontSize = 12.sp,
                )
            }
            Spacer(Modifier.weight(1f))
            Text("Локальная диагностика · данные не передаются без явного действия", color = Muted, fontSize = 11.sp)
        }
    }
}
