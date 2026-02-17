"""
================================================================================
Pi Arena Lite - master_node/main.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

STUDENT EDUCATIONAL OVERVIEW:
1. CONDITIONAL SCORING: By checking the 'field_mode' before adding points, 
   we can run a match where only one side is active.
2. MODULARITY: Notice how 'main.py' doesn't care HOW the UI draws the 
   button—it just reads the 'mode_var' value to make logic decisions.

Attribution:
- Core Match Logic: Derived from Cheesy Arena by Team 254 The Cheesy Poofs (BSD 3-Clause).
- Technical Inspiration: Influence from Team 3476 Code Orange.
- Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
- Implementation: Developed as MIT-Licensed Open Source by Team 3476 Code Orange, 
  with architectural assistance from Google Gemini.
================================================================================
"""

import os
import sys
import time
import threading
from common.constants import *
from common.network_utils import ArenaNetwork
from common.logger import MatchLogger
from master_node.ui_display import ScoringUI
from master_node.audio_controller import GameAudio

class PiArenaLiteMaster:
    def __init__(self):
        if not self.verify_system_integrity():
            sys.exit(1)

        self.ui = ScoringUI()
        self.audio = GameAudio()
        self.logger = MatchLogger()
        self.net = ArenaNetwork(node_role="MASTER_PRIMARY")
        
        self.match_active = False
        self.red_score = 0
        self.blue_score = 0
        self.current_phase = "IDLE"

        self.net.listen(self.handle_incoming_packets)
        self.ui.root.bind("<Return>", lambda e: self.trigger_button_press())
        
        print("\n[READY] Pi Arena Lite Multi-Mode Controller Ready.")

    def verify_system_integrity(self):
        base_path = os.getcwd()
        for d in ['common', 'master_node', 'assets', 'hub_node']:
            if not os.path.isdir(os.path.join(base_path, d)): return False
        return True

    def handle_incoming_packets(self, data, addr):
        # Read the practice mode selected on the UI
        field_mode = self.ui.mode_var.get()

        if data.get("type") == "SCORE_INC" and self.match_active:
            alliance = data.get("alliance")
            
            # FILTER: If in Solo Mode, ignore the other alliance
            if field_mode != "FULL" and alliance != field_mode:
                return 

            points = data.get("points", 1)
            if self.current_phase == "AUTO": points *= 2
            
            if alliance == "RED": self.red_score += points
            else: self.blue_score += points

    def trigger_button_press(self):
        if not self.match_active: self.start_match()
        else: self.abort_match()

    def start_match(self):
        self.match_active = True
        self.red_score = 0
        self.blue_score = 0
        threading.Thread(target=self.run_match_sequence, daemon=True).start()

    def abort_match(self):
        self.match_active = False
        self.audio.stop_all()
        self.audio.play("abort")
        self.logger.log_match(self.ui.mode_var.get(), self.red_score, self.blue_score, "ABORTED")
        self.current_phase = "ABORTED"

    def run_match_sequence(self):
        # The logic follows the mode. If in 'RED' mode, only Red sounds and scores fire.
        self.current_phase = "AUTO"; self.audio.play("match_start")
        self.countdown(AUTO_DURATION)
        if not self.match_active: return

        self.current_phase = "PAUSE"; self.audio.play("auto_end")
        self.countdown(TRANSITION_DURATION)
        if not self.match_active: return

        self.current_phase = "TELEOP"; self.audio.play("teleop_start")
        self.countdown(TELEOP_DURATION - ENDGAME_START)
        if not self.match_active: return

        self.current_phase = "ENDGAME"; self.audio.play("endgame")
        self.countdown(ENDGAME_START)
        if not self.match_active: return

        self.audio.play("match_end")
        self.logger.log_match(self.ui.mode_var.get(), self.red_score, self.blue_score, "COMPLETED")
        self.match_active = False
        self.current_phase = "POST-MATCH"

    def countdown(self, seconds):
        self.time_remaining = seconds
        while self.time_remaining > 0 and self.match_active:
            self.ui.update_display(self.time_remaining, self.current_phase, self.red_score, self.blue_score)
            time.sleep(1)
            self.time_remaining -= 1

    def run(self):
        self.ui.run()

if __name__ == "__main__":
    app = PiArenaLiteMaster()
    app.run()
