"""
================================================================================
Pi Arena Lite - master_node/main.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

STUDENT EDUCATIONAL OVERVIEW:
1. THE STATE MACHINE: The match moves through "Phases" (AUTO, TELEOP, etc.).
   The code uses these phases to decide how many points to award.
2. THREADING: We run the Match Logic in a "Background Thread." This allows
   the timer to count down without "freezing" the Scoring UI.
3. EVENT-DRIVEN PROGRAMMING: The 'handle_incoming_packets' function waits
   for the Hubs to send a score. It only "wakes up" when a ball is scored.

================================================================================
Attribution:
- Core State Logic: Adapted from Cheesy Arena by Team 254 (BSD 3-Clause).
- Technical Inspiration: Influence from Team 3476 (Code Orange).
- Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
- Implementation: Developed as MIT-Licensed Open Source by Team 3476, 
  with architectural assistance from Google Gemini.
================================================================================
"""

import os
import sys
import time
import threading
from common.constants import *           # Timing and Scoring values
from common.network_utils import ArenaNetwork  # UDP Communication
from common.logger import MatchLogger    # CSV Match Historian
from master_node.ui_display import ScoringUI    # Tkinter GUI
from master_node.audio_controller import GameAudio # Table 5-4 Cues

class PiArenaLiteMaster:
    def __init__(self):
        # 1. INTEGRITY CHECK
        # Before we start, make sure the admin placed all folders/assets correctly.
        if not self.verify_system_integrity():
            print("\n[!] CRITICAL ERROR: Asset folder structure is incorrect.")
            sys.exit(1)

        # 2. COMPONENT INITIALIZATION
        self.ui = ScoringUI()        # Start the visual display
        self.audio = GameAudio()     # Prepare the USB speakers
        self.logger = MatchLogger()  # Prepare the CSV file for records
        self.net = ArenaNetwork(node_role="MASTER_PRIMARY") # Start the "Heartbeat"
        
        # 3. GLOBAL VARIABLES (Match State)
        self.match_active = False    # Is the clock running?
        self.red_score = 0
        self.blue_score = 0
        self.time_remaining = 0
        self.current_phase = "IDLE"  # Start state

        # 4. NETWORK LISTENER
        # We tell the network module: "If you hear a packet, run this function."
        self.net.listen(self.handle_incoming_packets)
        
        # 5. INPUT BINDING
        # We bind the 'Enter' key (USB Mushroom Button) to our trigger function.
        self.ui.root.bind("<Return>", lambda e: self.trigger_button_press())
        
        print("\n[READY] Pi Arena Lite is operational. Press USB Button to start.")

    def verify_system_integrity(self):
        """Student Note: This ensures the software doesn't crash later due to missing files."""
        base_path = os.getcwd()
        # Verify the shortened path structure
        for d in ['common', 'master_node', 'assets', 'hub_node']:
            if not os.path.isdir(os.path.join(base_path, d)):
                return False
        return True

    def handle_incoming_packets(self, data, addr):
        """
        Event-Driven Scoring Logic.
        This function processes data sent from Hub Nodes 2 & 3.
        """
        if data.get("type") == "SCORE_INC" and self.match_active:
            points = data.get("points", 0)
            
            # RULE: 2026 REBUILT awards 2x points during Autonomous
            if self.current_phase == "AUTO":
                points *= 2
                
            if data.get("alliance") == "RED":
                self.red_score += points
            else:
                self.blue_score += points

    def trigger_button_press(self):
        """Logic for the physical USB Panic Button."""
        if not self.match_active:
            self.start_match()
        else:
            self.abort_match() # Emergency Stop if pressed during a match

    def start_match(self):
        """Initializes the match variables and starts the logic thread."""
        self.match_active = True
        self.red_score = 0
        self.blue_score = 0
        # EDUCATIONAL NOTE: We start a 'Thread' here so the timer can run
        # independently of the User Interface.
        threading.Thread(target=self.run_match_sequence, daemon=True).start()

    def abort_match(self):
        """The 'Foghorn' logic: Immediately stops the field."""
        self.match_active = False
        self.audio.stop_all()
        self.audio.play("abort") # Play FMS Foghorn
        self.logger.log_match(self.current_phase, self.red_score, self.blue_score, "ABORTED")
        self.current_phase = "ABORTED"

    def run_match_sequence(self):
        """The 2026 REBUILT™ State Machine."""
        
        # PHASE 1: AUTO (15s)
        self.current_phase = "AUTO"
        self.audio.play("match_start")
        self.countdown(AUTO_DURATION)
        if not self.match_active: return

        # PHASE 2: TRANSITION (10s)
        self.current_phase = "PAUSE"
        self.audio.play("auto_end")
        self.countdown(TRANSITION_DURATION)
        if not self.match_active: return

        # PHASE 3: TELEOP (135s Total)
        self.current_phase = "TELEOP"
        self.audio.play("teleop_start")
        
        # Teleop runs until the 30-second Endgame mark
        teleop_main_time = TELEOP_DURATION - ENDGAME_START
        self.countdown(teleop_main_time)
        if not self.match_active: return

        # PHASE 4: ENDGAME (30s)
        self.current_phase = "ENDGAME"
        self.audio.play("endgame")
        self.countdown(ENDGAME_START)
        if not self.match_active: return

        # PHASE 5: COMPLETION
        self.audio.play("match_end")
        self.logger.log_match("FINAL", self.red_score, self.blue_score, "COMPLETED")
        self.match_active = False
        self.current_phase = "POST-MATCH"

    def countdown(self, seconds):
        """Simple loop that updates the time and refreshes the UI."""
        self.time_remaining = seconds
        while self.time_remaining > 0 and self.match_active:
            # We push the data to the UI module for display
            self.ui.update_display(
                self.time_remaining, 
                self.current_phase, 
                self.red_score, 
                self.blue_score
            )
            time.sleep(1) # Wait one second
            self.time_remaining -= 1

    def run(self):
        """Runs the Tkinter UI on the Main Thread."""
        self.ui.run()

if __name__ == "__main__":
    # Create the controller object and start the program
    app = PiArenaLiteMaster()
    app.run()

