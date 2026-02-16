"""
Pi Arena Lite - master_node/main.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

Copyright & Attribution:
- Core Match Logic: Derived from Cheesy Arena by Team 254 (The Cheesy Poofs).
- Technical Inspiration: Influence from Team 3476 (Code Orange).
- Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
- Implementation: Developed with assistance from Google Gemini.
"""

import time
import threading
from common.constants import *

class MatchController:
    def __init__(self):
        self.state = "IDLE"
        self.red_score = 0
        self.blue_score = 0
        self.match_thread = None
        self.is_running = False

    def toggle_match(self):
        """Triggered by the USB Panic Button."""
        if not self.is_running:
            self.start_match()
        else:
            self.stop_match()

    def start_match(self):
        print("\n[MATCH START] Initializing 2026 REBUILT Cycle...")
        self.is_running = True
        self.match_thread = threading.Thread(target=self.game_loop)
        self.match_thread.start()

    def stop_match(self):
        print("\n[EMERGENCY STOP] Game halted by Master Button.")
        self.is_running = False
        self.state = "IDLE"

    def game_loop(self):
        # 1. AUTONOMOUS
        self.state = "AUTO"
        print(f"--- STARTING AUTONOMOUS ({AUTO_DURATION}s) ---")
        time.sleep(AUTO_DURATION)
        
        if not self.is_running: return

        # 2. TRANSITION
        self.state = "PAUSE"
        print(f"--- TRANSITION / GAME DATA ({TRANSITION_DURATION}s) ---")
        time.sleep(TRANSITION_DURATION)

        if not self.is_running: return

        # 3. TELEOP
        self.state = "TELEOP"
        print(f"--- STARTING TELEOP ({TELEOP_DURATION}s) ---")
        # In a full build, logic for 25s Hub Shifts goes here
        time.sleep(TELEOP_DURATION)

        self.is_running = False
        self.state = "IDLE"
        print("--- MATCH COMPLETE ---")

# Setup for USB Button Listening
if __name__ == "__main__":
    controller = MatchController()
    print("PI ARENA LITE: Ready. Press 'Enter' (USB Button) to Start.")
    try:
        while True:
            input() # Mimics the USB Button Press
            controller.toggle_match()
    except KeyboardInterrupt:
        print("\nShutting down Master Node.")
