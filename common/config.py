"""
================================================================================
Pi Arena Lite - common/config.py
The Blueprint and Identity Registry for the FRC 2026: REBUILT™ Practice Field

OVERALL PROJECT GOALS:
The goal of this module is to centralize the "Magic Numbers" that define the 
physical and logical boundaries of the field. By separating configuration from 
execution, changes to game rules, network addresses, or hardware 
pinouts can be made in a single location without risking bugs in the core 
functional logic.

CORE FUNCTIONALITY & ARCHITECTURE:
This module implements a "Hybrid Configuration" model. It combines static 
constants (like Game Rules and GPIO pins) with dynamic discovery (Identity 
Mapping). At startup, the module probes its own network interface and 
cross-references the result with a 'config.json' map to determine its specific 
role—Master, Red Hub, or Blue Hub.

NOVEL CONCEPTS:
1. Automated Identity Discovery: This allows for "Zero-Touch Deployment." The 
   exact same software package is pushed to all four Raspberry Pi nodes. The 
   code "decides" who it is based on its network IP, drastically reducing 
   maintenance overhead for the student team.
2. The Global Source of Truth: This file acts as the single point of entry for 
   all hardware and timing definitions. If the Hub shift duration changes from 
   25s to 30s in an official FIRST update, the change is made here once.

================================================================================
Attribution:
- Core State Logic: Adapted from Cheesy Arena (BSD 3-Clause) by Team 254.
- Technical Inspiration: Influence from Team 3476 (Code Orange).
- Implementation: Developed as MIT-Licensed Open Source by Team 3476, 
  with architectural assistance from Google Gemini.
================================================================================
"""

import json
import os
import socket

# --- 1. PHYSICAL HARDWARE DEFINITIONS ---
# These pins refer to the Broadcom (BCM) GPIO numbering on the Raspberry Pi 5.
PORT = 5555
HUB_SENSORS = [5, 6, 13, 19]  # 4 Normally Open break-beam sensors per Hub
PANIC_BUTTON_PIN = 26         # Physical match start/stop button on Master nodes

# --- 2. GAME RULES & TIMING (REBUILT™ 2026) ---
AUTO_SECONDS = 20
TELEOP_SECONDS = 135
SHIFT_DURATION = 25           # Duration of Hub 'Active/Inactive' cycles

# --- 3. DYNAMIC IDENTITY & NETWORK DISCOVERY ---

def get_local_ip():
    """ Probes the system to find the IP assigned to the local network. """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # We don't actually connect, we just use this to find the local interface
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

# We look for the 'Map' of the field at the root level of the repository.
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

# Default Fallback Values (Used if config.json is missing or corrupted)
MASTER_IP = "192.168.1.10"
MY_ROLE = "UNKNOWN"
ALLIANCE_COLOR = "red"

if os.path.exists(config_path):
    with open(config_path, 'r') as f:
        data = json.load(f)
        my_ip = get_local_ip()
        
        # Pull the primary Master IP so Hubs know where to report scores
        MASTER_IP = data['nodes']['node_1']['ip_address']
        
        # Identity Logic: The Pi finds its role by matching its IP to the map
        for node_id, info in data['nodes'].items():
            if info['ip_address'] == my_ip:
                MY_ROLE = info['role']
                # Sets alliance identity based on the node's configured role
                if "RED" in MY_ROLE: ALLIANCE_COLOR = "red"
                if "BLUE" in MY_ROLE: ALLIANCE_COLOR = "blue"
else:
    print(f"[CONFIG] Warning: {config_path} not found. Operating in fallback mode.")


# --- 4. AGITATOR & MECHANICAL TUNING (Node 2 & 3) ---
# Students: These settings control the gravity-assist rollers in the Hubs.
# Adjust these to prevent Fuel jams without burning out the brushed motors.

ROLLER_SPEED_FWD = 0.6        # Standard forward clearing speed (0.0 to 1.0)
LEAD_TIME = 10                # Seconds to start spinning BEFORE a period
TRAIL_TIME = 5                # Seconds to keep spinning AFTER a period

# ACTIVE JOSTLE (High-frequency clearing during scoring windows)
ACTIVE_JOSTLE_INTERVAL = 7    # Seconds between kicks
ACTIVE_JOSTLE_DURATION = 1.5  # Length of the reverse kick
ACTIVE_JOSTLE_SPEED = -0.7    # Power of the reverse kick

# INACTIVE JOSTLE (Maintenance pulses to prevent settling)
INACTIVE_JOSTLE_INTERVAL = 5   
INACTIVE_JOSTLE_DURATION = 1.0
INACTIVE_JOSTLE_SPEED = -0.4  
