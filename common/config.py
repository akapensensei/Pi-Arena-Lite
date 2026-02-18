"""
================================================================================
Pi Arena Lite - common/config.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

STUDENT EDUCATIONAL OVERVIEW:
1. JSON PARSING: We read 'config.json' to understand the entire field layout. 
   This teaches how software "consumes" data to make decisions.
2. IDENTITY DISCOVERY: The Pi checks its own IP address against the 'nodes' 
   list in the JSON. This allows the same code to run differently on a Master 
   vs. a Hub Node without manual changes.
3. FAIL-SAFES: If the JSON is missing or an IP isn't found, we use 'fallback' 
   values to ensure the match can still run.

================================================================================
Attribution:
- Core State Logic: Adapted from Cheesy Arena (BSD 3-Clause) by Team 254.
- Technical Inspiration: Influence from Team 3476 (Code Orange).
- Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
- Implementation: Developed as MIT-Licensed Open Source by Team 3476, 
  with architectural assistance from Google Gemini.
================================================================================
"""

import json
import os
import socket

# --- 1. PHYSICAL HARDWARE CONSTANTS (Static) ---
# These are fixed based on how we wired the Raspberry Pi 5.
PORT = 5555
HUB_SENSORS = [5, 6, 13, 19]  # BCM Pins for the 4 break-beams
PANIC_BUTTON_PIN = 26

# --- 2. GAME RULES (REBUILT™ 2026 Official) ---
AUTO_SECONDS = 20
TELEOP_SECONDS = 135
SHIFT_DURATION = 25

# --- 3. DYNAMIC IDENTITY DISCOVERY ---

def get_local_ip():
    """Helper for the Pi to find its own address on the practice network."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Does not actually connect, just probes the local interface
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# Locate 'config.json' in the root directory (one level up from /common)
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

# Default Fallbacks
MASTER_IP = "192.168.1.10"
MY_ROLE = "UNKNOWN"
ALLIANCE_COLOR = "red"

if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        data = json.load(f)
        my_ip = get_local_ip()
        
        # Pull the Master Primary IP so Hubs know where to send scores
        MASTER_IP = data['nodes']['node_1']['ip_address']
        
        # Identity Logic: "Who am I in this arena?"
        for node_id, info in data['nodes'].items():
            if info['ip_address'] == my_ip:
                MY_ROLE = info['role']
                if "RED" in MY_ROLE: ALLIANCE_COLOR = "red"
                if "BLUE" in MY_ROLE: ALLIANCE_COLOR = "blue"
else:
    print("[CONFIG] Warning: config.json not found! Using hardcoded defaults.")
