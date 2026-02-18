"""
================================================================================
Pi Arena Lite - master_node/audio_controller.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

STUDENT EDUCATIONAL OVERVIEW:
1. PYGAME MIXER: The 'mixer' module allows sounds to play in the background.
2. DICTIONARIES: "Event Names" (keys) are mapped to "File Paths" (values). This makes it easy to change a sound effect without touching the main logic.
3. ERROR HANDLING: The code checks 'os.path.exists' before playing. This prevents the program from crashing if a student forgets a file.

Attribution:
- Core State Logic: Adapted from Cheesy Arena by Team 254 The Cheesy Poofs (BSD 3-Clause).
- Technical Inspiration: Influence from Team 3476 Code Orange.
- Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
- Implementation: Developed as MIT-Licensed Open Source by Team 3476 Code Orange, with architectural assistance from Google Gemini.
================================================================================
"""

import pygame
import os

class GameAudio:
    def __init__(self):
        # Initialize the mixer specifically for USB Speaker output
        pygame.mixer.init()
        
        # TABLE 5-4 AUDIO MAPPING:
        # These keys match the events triggered in master_node/main.py
        self.sounds = {
            "match_start": "assets/match_start.wav",   # Auto Start: Buzzer
            "auto_end": "assets/match_stop.wav",      # Auto End: Buzzer
            "teleop_start": "assets/teleop_start.wav",# Teleop Start: Bell
            "endgame": "assets/endgame_alarm.wav",    # T-30 Seconds: Siren
            "match_end": "assets/match_stop.wav",     # Match End: Long Buzzer
            "abort": "assets/foghorn.wav"             # Match Abort: Foghorn
        }

    def play(self, sound_key):
        """
        Plays the requested sound if the file exists in the /assets folder.
        """
        if sound_key in self.sounds:
            file_path = self.sounds[sound_key]
            
            if os.path.exists(file_path):
                print(f"[AUDIO] Triggering: {sound_key}")
                # Load and play the sound
                pygame.mixer.Sound(file_path).play()
            else:
                print(f"[!] WARNING: Asset {file_path} is missing!")
        else:
            print(f"[!] ERROR: {sound_key} is not a valid game cue.")

    def stop_all(self):
        """
        Immediately silences the speakers. 
        Crucial for the 'Abort' sequence when the Panic Button is hit.
        """
        pygame.mixer.stop()
        print("[AUDIO] Output silenced.")

# STUDENT TEST BLOCK
# Run this file directly to test your USB speakers: python3 audio_controller.py
if __name__ == "__main__":
    audio = GameAudio()
    print("Testing Match Start Buzzer...")
    audio.play("match_start")
