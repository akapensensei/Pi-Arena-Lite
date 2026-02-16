"""
Pi Arena Lite - common/logger.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

Copyright & Attribution:
- Core Match Logic: Derived from Cheesy Arena by Team 254 (The Cheesy Poofs).
- Technical Inspiration: Influence from Team 3476 (Code Orange).
- Implementation: Developed with assistance from Google Gemini.
"""

import csv
import os
from datetime import datetime

class MatchLogger:
    def __init__(self, filename="match_history.csv"):
        self.filename = filename
        # Create header if file doesn't exist
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Phase", "Red_Score", "Blue_Score", "Status"])

    def log_match(self, phase, red, blue, status="COMPLETED"):
        """Appends match results to the CSV file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.filename, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([timestamp, phase, red, blue, status])
            print(f"[LOGGER] Match saved to {self.filename}")
        except Exception as e:
            print(f"[LOGGER] Error saving match: {e}")
