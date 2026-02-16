# Pi Arena Lite
### Distributed Practice Field Controller for FRC 2026: REBUILT™

**Pi Arena Lite** is a streamlined, Python-based field management system designed for Raspberry Pi 5 hardware. It manages real-time scoring, "Hub Shift" logic, and match timing for the 2026 game, REBUILT™.

---

## 🏗 System Architecture
*   **Nodes 1 & 4 (Master Stations):** Located at Driver Stations. Manage match clock (15s Auto / 135s Teleop), USB panic buttons, and live alliance score displays.
*   **Nodes 2 & 3 (Field Hubs):** Located inside the center field goals. Monitor 4x NO Break-Beam sensors for Fuel scoring and drive RGB LED status indicators.
*   **Network:** Hybrid Ethernet (Master-to-Master) and Wi-Fi (Master-to-Hubs) mesh network.

## 🕹 2026 Game Features (REBUILT™)
- **Dynamic Hub Shifts:** Toggles Hub "Active" status in 25s intervals based on Autonomous Game Data.
- **Autonomous Multiplier:** Automated 2x scoring for Fuel detected during the first 15 seconds.
- **Visual Feedback:** Real-time LED patterns signaling Hub status (Green=Active, Dim=Inactive).
- **Audio Cues:** Standard FRC buzzer, bell, and endgame alarm via USB speakers.

## ⚖️ Copyright & Attribution
This software is provided "as-is" for the FRC community to enhance local practice capabilities.

*   **Project Name:** Pi Arena Lite
*   **Core Match Logic:** Derived from the open-source [Cheesy Arena](https://github.com) by **Team 254 (The Cheesy Poofs)**.
*   **Technical Inspiration:** Logic and sensor-handling philosophy influenced by **Team 3476 (Code Orange)**.
*   **Game Rules:** Based on official **FIRST® Robotics Competition 2026: REBUILT™** documentation.

Licensed under the MIT License. Please retain these credits in all derivatives.

---

## 🔌 Hardware Setup
### Master Nodes (1 & 4)
- **Power:** A/C Adapters.
- **Peripherals:** USB Panic Button, USB Speaker, HDMI Monitor.

### Hub Nodes (2 & 3)
- **Power:** 12V Battery → 12V-to-USB Converter.
- **Fuel Sensors:** 4x NO Break-Beam Sensors (GPIO 17, 27, 22, 23).
- **LED Strips:** RGB Data via GPIO 18 (Direct 12V power recommended for LEDs).

## 🚀 Installation
1. Clone this repository to all 4 Pi nodes.
2. Run the automated setup script:
   ```bash
   chmod +x setup/install_dependencies.sh
   ./setup/install_dependencies.sh
