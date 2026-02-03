# Pi-Arena-Lite
Modular FRC Practice Field Management System

This software turns a collection of Raspberry Pis and/or PCs into a professional Field Management System. 
It is designed to be a set of "Plug-and-Play" appliances for practice fields. 

---

## 📂 File Directory & Purpose

### 🧠 Core Logic (The Brains)
*   **`piarena_fms.py`**: Runs ONLY on **Node 1 (Intel PC or Raspberry Pi)**. It manages the 160-second match clock, handles the SQLite database, and plays the official audio cues.
*   **`piarena_node.py`**: Runs on **Nodes 2, 3, and 4**. It handles the physical world: reading sensors, pulsing LEDs, and reporting scores back to Node 1.

### ⚙️ Configuration (The Settings)
*   **`config.json`**: The "Identity Card." You edit this on each node to tell the software if it is a Red Hub, Blue, Hub, Blue Master, etc.
*   **`network_config.json`**: Tells the system how to talk to your network switch and whether you are using a PLC or Pi Nodes for scoring/LED control.

### 🌐 Web Interfaces (The Displays)
*   **`templates/audience.html`**: The big scoreboard for the crowd. Show this on Node 4.
*   **`templates/pit.html`**: The "Doctor's Office." Check this on any laptop to see if your Pis are healthy or if sensors are broken.

### 🛠️ Utilities (The Tools)
*   **`requirements.txt`**: A checklist of Python libraries that must be installed for the "appliance" to work.
*   **`deploy_field.sh` / `.ps1`**: The "Go Button." Run this once from Node 1 to wake up the entire field simultaneously.

---

## 🔌 Hardware Setup (The Appliance Wiring)
1. **Node 1 (Master)**:
   - USB Panic Button.
   - USB Speaker (for Match Start/End sounds).
2. **Nodes 2 & 3 (Hubs)**: 
   - 12V Proximity Sensors → **Optocoupler** (translates 12V to Pi-safe 3.3V) → GPIO 17, 27, 22, 23.
   - WS2812B LEDs → GPIO 18.

---

## 🛡️ Reliability & "Self-Healing"
This software is designed to be an appliance.
*   **Hardware Watchdog**: If the code hangs, the Pi hardware will force a reboot within 15 seconds.
*   **Network Guard**: If a Hub loses WiFi for 60 seconds, it will automatically reboot to try and reconnect.
*   **Auto-Launch**: Using `systemd`, the software starts the moment power is applied.

---

## 📜 License
Modified BSD 3-Clause License. Portions Copyright (c) Team 254. 
Designed for the **FIRST Robotics Competition 2026: REBUILT presented by Haas**.




















## 🛠️ Built With
- **Original Foundation**: Cheesy Arena Lite by [Team 254](https://github.com).
- **Assistance**: This Python port and modular appliance logic were developed with assistance from **Google Gemini**.
