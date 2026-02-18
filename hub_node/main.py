"""
================================================================================
Pi Arena Lite - Node/main.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

STUDENT EDUCATIONAL OVERVIEW:
1. HARDWARE INTERRUPTS: We use 'when_pressed' on the beam sensors. Instead of 
   the Pi checking the sensor in a loop, the sensor "interrupts" the CPU the 
   instant a ball is detected. This ensures we never miss a score.
2. UDP CLIENT: The Node sends a UDP "packet" to the Master. Unlike TCP, UDP 
   doesn't wait for a reply, making it ideal for the high-speed scoring of 
   6-inch foam Fuel balls in REBUILT™.
3. MODULARITY: This script is identical for both Red and Blue Hubs. The only 
   difference is the 'ALLIANCE' variable in config.py.

================================================================================
Attribution:
- Technical Inspiration: Influence from Team 3476 (Code Orange).
- Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
- Implementation: Developed as MIT-Licensed Open Source by Team 3476, 
  with architectural assistance from Google Gemini.
================================================================================
"""

import asyncio
from gpiozero import Button
from common.network import ArenaNetworkNode
from common.config import MASTER_IP, HUB_SENSORS, ALLIANCE_COLOR, PORT

# --- CORE HARDWARE SETUP ---

# Students: The HUB_SENSORS list in config.py maps to the 4 break-beam sensors.
sensors = [Button(pin, pull_up=True) for pin in HUB_SENSORS]

# Initialize our specialized Network Client targeting the Master Node.
network = ArenaNetworkNode(target_ip=MASTER_IP, port=PORT)

def on_fuel_detected():
    """
    Core Function: What happens when a Fuel ball passes through the Hub.
    Students: We simply "fire and forget" a message to the Master.
    """
    print(f"[{ALLIANCE_COLOR.upper()}] Fuel Detected! Sending to Master...")
    
    # We send a standard dictionary that the Master knows how to decode.
    message = {
        "type": "FUEL_SCORED",
        "alliance": ALLIANCE_COLOR
    }
    network.send_message(message)

# Attach our scoring function to every physical sensor.
for sensor in sensors:
    sensor.when_pressed = on_fuel_detected

# --- AUXILIARY TASKS ---

async def status_led_loop():
    """
    Students: This is where you would add code to control the RGB LED strips.
    The Master will eventually send a "Hub Status" back to us to change colors.
    """
    while True:
        # Example: Pulse the Hub's alliance color
        await asyncio.sleep(0.1)

# --- MAIN ENTRY POINT ---

async def main():
    """
    Starts the network sender and the local status tasks concurrently.
    """
    print(f"=== {ALLIANCE_COLOR.upper()} HUB NODE ACTIVE ===")
    print(f"Targeting Master at {MASTER_IP}:{PORT}")
    
    # asyncio.gather allows the Pi to handle network and LEDs at once.
    await asyncio.gather(
        network.run_engine(),  # Keeps the UDP connection ready
        status_led_loop()      # Handles local visual feedback
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"Shutting down {ALLIANCE_COLOR} Node...")
