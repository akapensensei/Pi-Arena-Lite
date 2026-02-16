"""
Pi Arena Lite - hub_node/sensors.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

Copyright & Attribution:
- Core Match Logic: Derived from Cheesy Arena by Team 254 (The Cheesy Poofs).
- Technical Inspiration: Influence from Team 3476 (Code Orange).
- Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
- Implementation: Developed with assistance from Google Gemini.
"""

from gpiozero import Button
import time

class FuelSensor:
    def __init__(self, pins=[17, 27, 22, 23], node_id="HUB_RED"):
        self.node_id = node_id
        self.fuel_count = 0
        
        # Initialize 4 Break-Beam Sensors
        # We use pull_up=True because the beam being BROKEN pulls the signal
        # Use a bounce_time of 0.1s to prevent double-counting one ball
        self.sensors = []
        for pin in pins:
            sensor = Button(pin, pull_up=True, bounce_time=0.1)
            sensor.when_pressed = self.on_fuel_detected
            self.sensors.append(sensor)
            
        print(f"[{self.node_id}] 4 Fuel Sensors Initialized on GPIO {pins}")

    def on_fuel_detected(self):
        """Callback triggered when a ball breaks the beam."""
        self.fuel_count += 1
        print(f"[{self.node_id}] FUEL SCORED! Total: {self.fuel_count}")
        # Here, we would trigger a network packet to the Master Node (Node 1)
        self.broadcast_score()

    def broadcast_score(self):
        """Placeholder for sending score update to Master via UDP."""
        # This will interface with common/network_utils.py
        pass

    def reset_score(self):
        self.fuel_count = 0
        print(f"[{self.node_id}] Scores Reset for New Match.")

# For standalone testing on the Pi 5:
if __name__ == "__main__":
    hub = FuelSensor()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Sensor Node Shutting Down.")
