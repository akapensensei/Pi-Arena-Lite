"""
================================================================================
Pi Arena Lite - hub_node/leds.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

STUDENT EDUCATIONAL OVERVIEW:
1. PWM (Pulse Width Modulation): Computers can't easily send "half" power. 
   Instead, they blink the light on and off so fast that your eye sees it 
   as a specific brightness or mixed color.
2. RGB MIXING: By varying the intensity of Red, Green, and Blue, we can create 
   any color needed for the 2026 game status (like Gold for the Tower).
3. DIRECT POWER: Note that the Pi 5 sends the DATA, but the 12V Battery 
   provides the POWER to keep the Pi from "browning out."

Attribution:
- Core Match Logic: Derived from Cheesy Arena by Team 254 (The Cheesy Poofs).
- Technical Inspiration: Influence from Team 3476 (Code Orange).
- Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
- Implementation: Developed with assistance from Google Gemini.
================================================================================
"""

import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration (GPIO 18 is a PWM-capable pin on Pi 5)
LED_COUNT      = 60      
LED_PIN        = 18      
LED_FREQ_HZ    = 800000  
LED_DMA        = 10      
LED_BRIGHTNESS = 255     

class HubLights:
    def __init__(self):
        # Initialize the hardware library
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, False, LED_BRIGHTNESS)
        self.strip.begin()

    def set_color(self, color):
        """Standard 'Fill' command to change the whole Hub color."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def game_state_update(self, state, is_active=True):
        """
        Translates FRC Game Phases into visual colors.
        Rules: Green for Auto, Alliance Color for Teleop, Gold for Endgame.
        """
        if state == "AUTO":
            self.set_color(Color(0, 255, 0)) # Green
        elif state == "TELEOP":
            if is_active:
                self.set_color(Color(255, 0, 0)) # Example: Full Red
            else:
                self.set_color(Color(20, 0, 0))  # Dim/Inactive
        elif state == "ENDGAME":
            self.set_color(Color(255, 215, 0)) # Gold/Tower Effect
        else:
            self.set_color(Color(0, 0, 0))     # Off
