# 🏟️ Pi Arena Lite: Admin & Operations Guide
### **System Version:** 1.0 (FRC 2026: REBUILT™)

This guide provides the necessary instructions to configure, wire, and operate the **Pi Arena Lite** distributed practice field system.

---

## 🏗️ 1. System Architecture
Pi Arena Lite is a modular system running on four Raspberry Pi 5 nodes:
*   **Node 1 & 4 (Masters):** Driver Station positions. Manage match timing, UI, and Match Audio.
*   **Node 2 & 3 (Hubs):** Field Goal positions. Manage Break-Beam sensors and RGB Status LEDs.

---

## 🔌 2. Hardware Wiring & Power

### **Hub Nodes (2 & 3)**
| Component | Connection | Pin / Port |
| :--- | :--- | :--- |
| **Power Input** | 12V Battery | 12V-to-5V Buck Converter (5A min) |
| **Fuel Sensors** | 4x NO Break-Beams | GPIO 17, 27, 22, 23 (Signal) + GND |
| **LED Strip** | WS2812B RGB Strip | **Data:** GPIO 18 |
| **LED Power** | Direct to Converter | **DO NOT** power LEDs from the Pi 5V rail |

> **⚠️ Critical Note:** You must connect a Ground wire from the LED strip to a **GND pin** on the Pi to ensure a common data reference for the PWM signal.

### **Master Nodes (1 & 4)**
*   **Panic Button:** USB Mushroom button (registers as the "Enter" key).
*   **Audio:** USB Speakers (Note: Onboard 3.5mm jack is disabled to support Hub LED PWM).
*   **Display:** HDMI Monitor (1920x1080).

---

## 🚀 3. Appliance Mode (Auto-Boot Setup)

### **A. Master Nodes (Nodes 1 & 4)**
1. Run `sudo raspi-config` -> **System Options** -> **Boot/Auto Login** -> **Desktop Autologin**.
2. Run the Master Setup bash script:
   ```bash
   chmod +x setup/setup_master.sh
   ./setup/setup_master.sh
