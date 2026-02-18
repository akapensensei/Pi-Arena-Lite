# 🛠️ Pi Arena Lite: Hardware & Power Guide
## FRC 2026: REBUILT™ Practice Field Setup

This guide explains how to power and wire the **Hub Nodes (2 & 3)** using a 12V Power Source (Bench Power Supply or Robot Battery).

---

### 1. Power Distribution (The "Heart")
To prevent the Raspberry Pi 5 from crashing (brownouts), we split the power into two parallel paths:

*   **Logic Power (Pi 5):** Powered via a dedicated USB-C cable from the 12V-to-USB converter.
*   **LED Power (RGB Strips):** Powered via a USB Breakout Connector (Screw Terminals). 
    *   *Note:* The Pi 5 GPIO cannot provide enough current for the LED strips; they must be fed directly from the 12V source.

### 2. The Shared Ground (Critical Requirement)
**THE PI AND THE LEDS MUST SHARE A COMMON GROUND.** Without a shared ground, the Data signal will be "noisy," causing flickering or failed scores.

**Wiring Instructions:**
1.  **5V (Red):** Connect the LED Strip 5V wire to the **(+) Terminal** of the USB Breakout.
2.  **GND (White/Black):** Connect the LED Strip Ground to the **(-) Terminal** of the USB Breakout **AND** to Physical **Pin 6 (GND)** on the Raspberry Pi 5.
3.  **DATA (Green/Yellow):** Connect the LED Data wire directly to **GPIO 18 (Physical Pin 12)** on the Raspberry Pi 5.

### 3. Bench Power Supply Settings
If using a Lab Bench Power Supply instead of a battery:
*   **Voltage:** Set to **12.0V - 13.5V**.
*   **Current Limit:** Set to at least **5.0A** to handle the surge when LEDs hit full brightness during Endgame.

---

### Student Lab Note:
Observe the Ammeter on the bench supply. You will see the current (Amps) spike during **Endgame** when the LEDs turn white. This is a real-time visualization of the energy required to run a 2026 FRC field!
