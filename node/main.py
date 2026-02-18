"""
================================================================================
Pi Arena Lite - Node/main.py
The Distributed Sensory Edge of the FRC 2026: REBUILT™ Practice Field

OVERALL PROJECT GOALS:
The Hub Node acts as a high-fidelity event reporter. In a 
distributed arena, the Hub is the "eyes" of the system. It detects rapid-fire 
physical events (Fuel balls passing through sensors) and relays that data to the 
Master Node with minimal latency, ensuring no scoring event is lost 
during high-intensity play.

CORE FUNCTIONALITY & ARCHITECTURE:
This module uses an 'Interrupt-Driven' architecture. Rather than constantly checking 
if a sensor is blocked (polling), the code uses hardware interrupts. This allows 
the Pi to remain in a low-power waiting state or handle auxiliary tasks like LED 
animations, only "waking up" the scoring logic the microsecond a beam is broken.

NOVEL CONCEPTS:
1. Deterministic Reporting: The Hub is "logic-blind." It does not 
   decide if a ball is worth points or if the game is active. By simply 
   reporting the event and a timestamp, it allows the Master Node to perform 
   centralized validation, preventing "split-brain" scoring errors.
2. Async Hardware Interfacing: By using 'asyncio.gather', the Hub can manage 
   background network health and LED status signals without creating "jitter" 
   in the sensor detection logic.

================================================================================
Attribution:
- Core State Logic: Adapted from Cheesy Arena (BSD 3-Clause) by Team 254.
- Technical Inspiration: Influence from Team 3476 (Code Orange).
- Implementation: Developed as MIT-Licensed Open Source by Team 3476, 
  with architectural assistance from Google Gemini.
================================================================================
"""

import asyncio
from gpiozero import Button
from common.network import ArenaNetworkNode
from common.config import MASTER_IP, PORT, HUB_SENSORS, ALLIANCE_COLOR

# --- HARDWARE INTERFACE ---

# Initialize sensors using BCM GPIO pins defined in config.py.
# Internal pull-up resistors are enabled to ensure a clean HIGH signal.
sensors = [Button(pin, pull_up=True) for pin in HUB_SENSORS]

# Initialize the outbound network engine targeting the Master Node.
network = ArenaNetworkNode(target_ip=MASTER_IP, port=PORT)

def on_fuel_detected():
    """
    Hardware Interrupt Callback.
    Triggered instantly when a Fuel ball breaks the beam sensor.
    """
    # Create a standardized event packet
    message = {
        "type": "FUEL_SCORED",
        "alliance": ALLIANCE_COLOR
    }
    
    # Drop the message into the async queue for immediate transmission
    network.send_message(message)
    print(f"[{ALLIANCE_COLOR.upper()}] Event reported to Master.")

# Register the interrupt handler for all sensors in this Hub.
for sensor in sensors:
    sensor.when_pressed = on_fuel_detected

# --- BACKGROUND TASKS ---

async def hub_feedback_loop():
    """
    Manages local feedback, such as the RGB LED Hub status.
    This task runs concurrently with the network engine.
    """
    while True:
        # Future Logic: Update LEDs based on ACTIVE/INACTIVE signals from Master
        await asyncio.sleep(0.1)

# --- EXECUTION ENGINE ---

async def main():
    """
    Synchronizes the network engine and auxiliary hub tasks.
    """
    print(f"=== {ALLIANCE_COLOR.upper()} HUB NODE INITIALIZED ===")
    print(f"Monitoring Pins: {HUB_SENSORS}")
    
    # Run the networking engine and feedback loops in parallel
    await asyncio.gather(
        network.run_engine(),
        hub_feedback_loop()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n[SHUTDOWN] {ALLIANCE_COLOR.upper()} Hub Node offline.")
