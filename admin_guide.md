# 🏟️ Pi Arena Lite: Admin & Operations Guide
### **System Version:** 1.0 (FRC 2026: REBUILT™)

This guide provides the necessary instructions to configure, wire, and operate the **Pi Arena Lite** distributed practice field system.

---

## 🏗️ 1. System Architecture
Pi Arena Lite is a modular system running on four Raspberry Pi nodes:
*   **Node 1 & 4 (Masters):** Manage timing, UI, and Match Audio. Connected via Ethernet.
*   **Node 2 & 3 (Hubs):** Manage Break-Beam sensors and RGB Status LEDs. Connected via Wi-Fi.

---

## 🔌 2. Hardware Wiring & Power (Hub Nodes)

| Component | Connection | Pin / Port |
| :--- | :--- | :--- |
| **Power Input** | 12V Battery | 12V-to-5V Buck Converter (5A min) |
| **Fuel Sensors** | 4x NO Break-Beams | GPIO 17, 27, 22, 23 (Signal) + GND |
| **LED Strip** | WS2812B RGB Strip | **Data:** GPIO 18 (PWM) |

> **⚠️ Critical Note:** Connect the LED Ground wire to a **GND pin** on the Pi to ensure a common data reference for the PWM signal.

---

## 🚀 3. Appliance Mode (Automated Setup)

To treat the nodes as "appliances," use these scripts to configure them to boot directly into the game software.

### **A. Master Nodes (Nodes 1 & 4)**
1. Run `sudo raspi-config` -> **System Options** -> **Boot/Auto Login** -> **Desktop Autologin**.
2. Run the automated configuration script:
   ```bash
   chmod +x setup/master_config.sh
   ./setup/master_config.sh

   ## 🛠️ 4. Hub Calibration & Rules (Manual Maintenance)
Use these visual cues and rules to ensure the Hubs are match-ready, as the Hubs are headless.

### **A. The "Clear Hub" Rule**
*   **Rule:** Ensure no **FUEL** (balls) are blocking the break-beam sensors when powering on the Hubs.
*   **Reason:** Sensors calibrate their "empty" state at boot. A blocked beam during startup can "zero out" the sensor, causing it to ignore scored FUEL during the match.

### **B. LED Status Codes (Table 5-3 Adapted)**
*   **Solid Alliance Color:** HUB is active and ready for scoring.
*   **Pulsing Alliance Color:** Hub deactivation warning (starts 3s before shift change).
*   **Dim Alliance Color:** HUB is currently inactive (scoring disabled).
*   **Solid Green:** FIELD is safe/Idle.

---

## 🔊 5. Audio Troubleshooting (Table 5-4 Cues)
All audio must go through **USB Speakers**, as Raspberry Pi 5 does not have an analog jack.

1. **Selection:** Run `alsamixer`, press **F6**, and select your **USB Audio Device**.
2. **Unmute:** Ensure the volume shows `00` (unmuted) and not `MM`.
3. **Required Assets:** Ensure the `/assets` folder contains: 
   * `match_start.wav`, `match_stop.wav`, `teleop_start.wav`, `endgame_alarm.wav`, and `foghorn.wav`.

---

## 💻 6. Hardware Notes (Pi 4 vs. Pi 5)
*   **Pathing:** All software must reside in `/home/pi/frc2026/`.
*   **PWM Conflict:** Both models share the PWM timer with onboard audio. If LEDs flicker on **Pi 4**, ensure `dtparam=audio=off` is in `/boot/firmware/config.txt`.
*   **Performance:** Hub logic is optimized to run identically on Pi 4 and Pi 5 hardware.

---

## ⚖️ 7. Copyright & Attribution
*   **Core State Logic:** Adapted from Cheesy Arena by **Team 254 The Cheesy Poofs** (BSD 3-Clause).
*   **Technical Inspiration:** Influence from **Team 3476 Code Orange**.
*   **Game Rules:** Based on official **FIRST® REBUILT™ 2026** documentation.
*   **Implementation:** Developed as MIT-Licensed Open Source by **Team 3476 Code Orange**, with architectural assistance from Google Gemini.

