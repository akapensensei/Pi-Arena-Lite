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
        pygame.mixer.init()
        # Paths to your assets
        self.sounds = {
            "start": "assets/match_start.wav",
            "teleop": "assets/teleop_start.wav",
            "endgame": "assets/endgame_alarm.wav",
            "stop": "assets/match_stop.wav"
        }

    def play(self, sound_key):
        if sound_key in self.sounds and os.path.exists(self.sounds[sound_key]):
            pygame.mixer.Sound(self.sounds[sound_key]).play()
        else:
            print(f"Audio file for {sound_key} missing.")

# Example: audio = GameAudio(); audio.play("start")
