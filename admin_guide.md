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

> **⚠️ Critical Note:** You must connect a Ground wire from the LED strip to a **GND pin** on the Pi to ensure a common data reference for the PWM signal.

---

## 🚀 3. Appliance Mode (Auto-Boot Setup)

### **A. Master Nodes (Nodes 1 & 4)**
Masters require the Desktop to load before the UI can render.
1. Run `sudo raspi-config` -> **System Options** -> **Boot/Auto Login** -> **Desktop Autologin**.
2. **Setup Command:**

cat < ~/frc2026-practice-field/setup/setup_master.sh
#!/bin/bash
mkdir -p /home/pi/.config/autostart
cat < /home/pi/.config/autostart/piarena.desktop
[Desktop Entry]
Type=Application
Name=Pi Arena Master
Exec=python3 /home/pi/frc2026-practice-field/master_node/main.py
WorkingDirectory=/home/pi/frc2026-practice-field
EOT
chmod +x /home/pi/frc2026-practice-field/master_node/main.py
EOF
chmod +x ~/frc2026-practice-field/setup/setup_master.sh
~/frc2026-practice-field/setup/setup_master.sh

### **B. Hub Nodes (Nodes 2 & 3)**
Hubs run as background services and do not require a login.
1. **Setup Command:**

cat < ~/frc2026-practice-field/setup/setup_hub.sh
#!/bin/bash
sudo bash -c 'cat < /etc/systemd/system/piarena-hub.service
[Unit]
Description=Pi Arena Hub Controller
After=network.target
[Service]
ExecStart=/usr/bin/python3 -u /home/pi/frc2026-practice-field/hub_node/main.py
WorkingDirectory=/home/pi/frc2026-practice-field
Restart=always
RestartSec=5
User=pi
[Install]
WantedBy=multi-user.target
EOT'
sudo systemctl daemon-reload
sudo systemctl enable piarena-hub.service
sudo systemctl start piarena-hub.service
EOF
chmod +x ~/frc2026-practice-field/setup/setup_hub.sh
~/frc2026-practice-field/setup/setup_hub.sh
---

## 🛠️ 4. Hub Calibration & Maintenance
Because the Hubs are headless, use these visual cues and rules to ensure they are match-ready.

### **A. The "Clear Hub" Rule**
*   **Rule:** Ensure no **FUEL** (balls) are blocking the break-beam sensors when powering on the Hubs.
*   **Reason:** The Pi 5 initializes GPIO states at boot. A blocked beam during startup can "zero out" the sensor, causing it to ignore scored FUEL during the match.

### **B. LED Status Codes (Table 5-3 Adapted)**
Refer to these colors to diagnose the Hub's current state:
*   **Solid Alliance Color:** HUB is active and ready for scoring.
*   **Pulsing Alliance Color:** Hub deactivation warning (starts 3s before shift change).
*   **Dim Alliance Color:** HUB is currently inactive (scoring disabled).

---

## 🔊 5. Audio Troubleshooting (Table 5-4 Cues)
Raspberry Pi 5 does not have an analog jack. All audio must go through **USB Speakers**.

1. Open a terminal and run: `alsamixer`.
2. Press **F6** to select your **USB Audio Device**.
3. Use **Arrow Keys** to raise the volume. Ensure it shows `00` (unmuted).
4. Save settings with: `sudo alsactl store`.

---

## 🛠️ 6. Maintenance & Validation

### **Path Integrity Check**
The Master Node validates the following structure on boot. Ensure you run scripts from the **root** folder:
```text
~/frc2026-practice-field/
├── assets/ (match_start.wav, match_stop.wav, teleop_start.wav, endgame_alarm.wav, foghorn.wav)
├── common/ (config.json, constants.py, network_utils.py, logger.py)
├── master_node/ (main.py, ui_display.py, audio_controller.py)
└── hub_node/ (main.py, sensors.py, leds.py)

## ⚖️ 7. Copyright & Attribution
*   **Match State Logic:** Derived from **Cheesy Arena** by **Team 254 (The Cheesy Poofs)**.
*   **Technical Inspiration:** Influence from **Team 3476 (Code Orange)**.
*   **Game Rules:** Official **FIRST® REBUILT™ 2026** documentation.
*   **Implementation:** Developed with assistance from AI on Google Search which is powered by the Gemini family of models.

Licensed under the MIT License.


