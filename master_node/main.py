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
from common.network_utils import ArenaNetwork
from master_node.ui_display import ScoringUI
from master_node.audio_controller import GameAudio

class PiArenaLiteMaster:
    def __init__(self):
        # Initialize Core Modules
        self.ui = ScoringUI()
        self.audio = GameAudio()
        self.net = ArenaNetwork(node_role="MASTER_PRIMARY")
        
        # Match State Variables
        self.match_active = False
        self.red_score = 0
        self.blue_score = 0
        self.time_remaining = 0
        self.current_phase = "IDLE"

        # Start Networking Listener (for scores from Hubs)
        self.net.listen(self.handle_incoming_packets)

        # Bind the USB Panic Button (Enter Key) to the trigger
        self.ui.root.bind("<Return>", lambda e: self.trigger_button_press())
        
        print("Pi Arena Lite: System Ready. Press USB Button to start.")

    def handle_incoming_packets(self, data, addr):
        """Processes score updates from Node 2 and 3 Hubs."""
        if data.get("type") == "SCORE_INC" and self.match_active:
            points = data.get("points", 0)
            # Apply 2x Multiplier if in Autonomous
            if self.current_phase == "AUTO":
                points *= 2
                
            if data.get("alliance") == "RED":
                self.red_score += points
            else:
                self.blue_score += points

    def trigger_button_press(self):
        """Logic for the USB Panic Button."""
        if not self.match_active:
            self.start_match()
        else:
            self.abort_match()

    def start_match(self):
        self.match_active = True
        self.red_score = 0
        self.blue_score = 0
        threading.Thread(target=self.run_match_sequence, daemon=True).start()

    def abort_match(self):
        self.match_active = False
        self.audio.stop_all()
        self.audio.play("abort")
        self.current_phase = "ABORTED"
        print("[PANIC] Match Aborted and Reset.")

    def run_match_sequence(self):
        """The 2026 REBUILT Match Timing Sequence."""
        
        # 1. AUTONOMOUS (15s)
        self.current_phase = "AUTO"
        self.audio.play("match_start")
        self.countdown(AUTO_DURATION)
        if not self.match_active: return

        # 2. TRANSITION (10s)
        self.current_phase = "PAUSE"
        self.audio.play("auto_end")
        self.countdown(TRANSITION_DURATION)
        if not self.match_active: return

        # 3. TELEOP (135s Total)
        self.current_phase = "TELEOP"
        self.audio.play("teleop_start")
        
        # Teleop until Endgame
        teleop_main_time = TELEOP_DURATION - ENDGAME_START
        self.countdown(teleop_main_time)
        if not self.match_active: return

        # 4. ENDGAME (30s)
        self.current_phase = "ENDGAME"
        self.audio.play("endgame")
        self.countdown(ENDGAME_START)
        if not self.match_active: return

        # 5. MATCH COMPLETE
        self.audio.play("match_end")
        self.current_phase = "POST-MATCH"
        self.match_active = False

    def countdown(self, seconds):
        """Standard timer loop that updates the UI every second."""
        self.time_remaining = seconds
        while self.time_remaining > 0 and self.match_active:
            self.ui.update_display(
                self.time_remaining, 
                self.current_phase, 
                self.red_score, 
                self.blue_score
            )
            time.sleep(1)
            self.time_remaining -= 1

    def run(self):
        """Keep the UI alive on the main thread."""
        self.ui.run()

if __name__ == "__main__":
    app = PiArenaLiteMaster()
    app.run()
