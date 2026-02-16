"""
Pi Arena Lite - master_node/audio_controller.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

Copyright & Attribution:
- Core Match Logic: Derived from Cheesy Arena by Team 254 (The Cheesy Poofs).
- Technical Inspiration: Influence from Team 3476 (Code Orange).
- Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
- Implementation: Developed with assistance from Google Gemini.
"""

import pygame
import os

class GameAudio:
    def __init__(self):
        # Initialize the mixer for USB Audio Output
        pygame.mixer.init()
        
        # Audio File Mapping per 2026 Game Manual Table 5-4
        # Note: 'Buzzer' is often the same file, played for different durations
        self.sounds = {
            "match_start": "assets/match_start.wav",   # Auto Start: Buzzer
            "auto_end": "assets/match_stop.wav",      # Auto End: Buzzer
            "teleop_start": "assets/teleop_start.wav",# Teleop Start: Bell
            "endgame": "assets/endgame_alarm.wav",    # T-30 Seconds: Alarm
            "match_end": "assets/match_stop.wav",     # Match End: Long Buzzer
            "abort": "assets/foghorn.wav"             # Match Abort: Foghorn (FMS Standard)
        }

    def play(self, sound_key):
        """Plays the mapped sound if the asset exists."""
        if sound_key in self.sounds:
            file_path = self.sounds[sound_key]
            if os.path.exists(file_path):
                print(f"[AUDIO] Playing: {sound_key}")
                pygame.mixer.Sound(file_path).play()
            else:
                print(f"[ERROR] Audio asset missing at {file_path}")
        else:
            print(f"[ERROR] Sound key '{sound_key}' not defined in Table 5-4.")

    def stop_all(self):
        """Immediately silences all audio (used during Panic Button reset)."""
        pygame.mixer.stop()
        print("[AUDIO] All sounds silenced.")

# Testing block for the Master Node
if __name__ == "__main__":
    audio = GameAudio()
    print("Testing Match Start Audio...")
    audio.play("match_start")

