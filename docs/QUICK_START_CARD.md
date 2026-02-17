# 📑 Pi Arena Lite: Field Crew Quick-Start
### **Game:** FRC 2026 REBUILT™ | **System:** Appliance v1.1

---

## 🚦 1. Startup Sequence (The "Cold Start")
1.  **Clear the Hubs:** Ensure no **Fuel** (balls) are inside Hub 2 or 3.
2.  **Power On:** Plug in 12V batteries for Hubs. Node 1 (Master) will boot to the UI.
3.  **Verify Mesh:** On Node 1, run the diagnostic tool:
    ```bash
    /home/pi/frc2026/setup/ping_test.sh
    ```
    *All nodes must show ✅ **ONLINE** before starting a match.*

---

## 🕹️ 2. Match Control (The "Panic Button")
*   **START:** Press the **USB Mushroom Button** (or `Enter`) once to begin.
*   **ABORT:** If a safety issue occurs, **HIT THE BUTTON AGAIN**.
    *   *Result:* The **Foghorn** will sound, and all scoring will stop immediately.

---

## 💡 3. Hub Status (Table 5-3)
*   **Solid Alliance Color:** Hub is **ACTIVE**. Fuel scores count.
*   **Pulsing Color:** Hub **WARNING**. Shift change in 3 seconds.
*   **Dim Color:** Hub **INACTIVE**. Fuel will **NOT** count.
*   **Solid Green:** Field is **SAFE**. Match is over.

---

## 🛠️ 4. Mode Selection (Solo Practice)
If a team only needs one side of the field, click the **Mode Button** on the UI:
*   **RED:** Silences Blue side.
*   **BLUE:** Silences Red side.
*   **FULL:** Standard 2-Alliance Match.

---

## ⚖️ Attribution
- **Core Match Logic:** Derived from Cheesy Arena by Team 254 The Cheesy Poofs (BSD 3-Clause).
- **Technical Inspiration:** Influence from Team 3476 Code Orange.
- **Implementation:** Developed as MIT-Licensed Open Source by Team 3476 Code Orange.
