# 🏟️ Pi Arena Lite: Admin & Operations Guide
### **System Version:** 1.0 (FRC 2026: REBUILT™)

This guide provides the necessary instructions to configure, wire, and operate the **Pi Arena Lite** distributed practice field system.

---

## 🏗️ 1. System Architecture
Pi Arena Lite is a modular system running on four Raspberry Pi 5 nodes:
*   **Node 1 & 4 (Masters):** Manage match timing, UI, and Match Audio.
*   **Node 2 & 3 (Hubs):** Manage Break-Beam sensors and RGB Status LEDs.

---

## 🔌 2. Hardware Wiring & Power

### **Hub Nodes (2 & 3)**
*   **Power:** 12V Battery → 12V-to-5V Buck Converter.
*   **Sensors:** 4x NO Break-Beams to **GPIO 17, 27, 22, 23** + GND.
*   **LEDs:** Data to **GPIO 18**. Power LEDs directly from the converter.
*   **⚠️ Note:** Ensure a common ground between the LED strip and Pi.

### **Master Nodes (1 & 4)**
*   **Panic Button:** USB Mushroom button (registers as "Enter").
*   **Audio:** USB Speakers (Note: Onboard 3.5mm jack must be disabled).
*   **Display:** HDMI Monitor (1080p).

---

## 🚀 3. Appliance Mode (Auto-Boot Setup)

### **A. Master Nodes (Nodes 1 & 4)**
Masters require the Desktop to load before the UI can render.
1. Run `sudo raspi-config` -> **System Options** -> **Boot/Auto Login** -> **Desktop Autologin**.
2. Run the Master Setup script:
   ```bash
   chmod +x setup/setup_master.sh
   ./setup/setup_master.sh

