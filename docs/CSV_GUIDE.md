# 📊 Pi Arena Lite: CSV Data & Analytics Guide
### **System:** 2026 REBUILT™ Data Historian

The `match_history.csv` file is located in `/home/pi/frc2026/`. It is a "Volatile-Safe" log, meaning it only writes to the disk when a match ends, protecting the Pi’s SD card from excessive wear during live play.

## 1. Column Definitions (The Data Map)

| Column | Description | Student Educational Note |
| :--- | :--- | :--- |
| **Timestamp** | YYYY-MM-DD HH:MM:SS | Used to sort matches chronologically. |
| **Phase** | AUTO / TELEOP / FINAL | Shows exactly when the match ended or was aborted. |
| **Red_Score** | Total Points for Red | Includes the 2x Autonomous multiplier. |
| **Blue_Score** | Total Points for Blue | Includes the 2x Autonomous multiplier. |
| **Status** | COMPLETED / ABORTED | 'ABORTED' indicates the Panic Button was hit. |

---

## 2. Analyzing the Data in Excel / Google Sheets
To build a **Leaderboard** for your drive teams:
1.  **Import:** Open a blank sheet and select `File > Import > match_history.csv`.
2.  **Filter:** Click the top row and select `Data > Create a Filter`.
3.  **Clean:** Filter the **Status** column to show only `COMPLETED` matches to remove practice restarts.
4.  **Calculate:** Create a new column named `Point_Spread` using the formula `=ABS(C2-D2)` to see how competitive your practice sessions are.

---

## 3. Educational Overview for Students
*   **Comma Separated Values (CSV):** This is a universal "Plain Text" format. It is used because it doesn't require special software to read, making it the most compatible way to share data between a Raspberry Pi and a Windows/Mac scouting computer.
*   **The Append Method:** Our Python code uses the `'a'` (append) flag. This ensures we don't overwrite previous practice sessions; we simply keep adding new rows to the bottom of the "ledger."

---

## ⚖️ Attribution
*   **Core State Logic:** Adapted from Cheesy Arena by **Team 254 The Cheesy Poofs** (BSD 3-Clause).
*   **Technical Inspiration:** Influence from **Team 3476 Code Orange**.
*   **Game Rules:** Based on official **FIRST® REBUILT™ 2026** documentation.
*   **Implementation:** Developed as MIT-Licensed Open Source by **Team 3476 Code Orange**, with architectural assistance from Google Gemini.
