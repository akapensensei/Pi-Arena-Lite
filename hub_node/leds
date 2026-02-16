"""
Pi Arena Lite - hub_node/leds.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

Copyright & Attribution:
- Core Match Logic: Derived from Cheesy Arena by Team 254 (The Cheesy Poofs).
- Technical Inspiration: Influence from Team 3476 (Code Orange).
- Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
- Implementation: Developed with assistance from Google Gemini.
"""

import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT      = 60      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

class HubLights:
    def __init__(self):
        self.strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        self.strip.begin()

    def set_color(self, color, wait_ms=50):
        """Set the entire strip to one color."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
        self.strip.show()

    def game_state_update(self, state, is_active=True):
        """Update LEDs based on 2026 REBUILT game state."""
        if state == "AUTO":
            self.set_color(Color(0, 255, 0)) # Solid Green for Auto
        elif state == "TELEOP":
            if is_active:
                # Active Hubs show Alliance Color (Example: Red)
                self.set_color(Color(255, 0, 0)) 
            else:
                # Inactive Hubs go "Dim/Pulse" per 2026 Shift Rules
                self.set_color(Color(20, 0, 0)) 
        elif state == "ENDGAME":
            self.flash_gold() # Special 2026 REBUILT Tower effect
        else:
            self.set_color(Color(0, 0, 0)) # Off / Idle

    def flash_gold(self):
        """Endgame signal for the REBUILT Tower climb."""
        for _ in range(5):
            self.set_color(Color(255, 215, 0))
            time.sleep(0.5)
            self.set_color(Color(0, 0, 0))
            time.sleep(0.5)

# Example Usage
if __name__ == "__main__":
    lights = HubLights()
    lights.game_state_update("AUTO")
