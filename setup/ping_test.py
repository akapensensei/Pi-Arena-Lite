"""
================================================================================
Pi Arena Lite - setup/ping_test.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

STUDENT EDUCATIONAL OVERVIEW:
1. SUBPROCESS: The 'subprocess' module allows Python to "talk" to the Linux OS.
   It runs the system 'ping' command just as if a student typed it.
2. DICTIONARIES: We store our Field IPs in Key-Value pairs {Name: IP}. This
   makes the code modular and easy to expand if you add more Hubs.
3. EXIT CODES: Computer commands return an 'exit code'. 0 means the node
   answered correctly. Anything else means the network path is blocked.

Attribution:
- Core State Logic: Adapted from Cheesy Arena by Team 254 The Cheesy Poofs (BSD 3-Clause).
- Technical Inspiration: Influence from Team 3476 Code Orange.
- Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
- Implementation: Developed as MIT-Licensed Open Source by Team 3476 Code Orange, 
  with architectural assistance from Google Gemini.
================================================================================
"""

import subprocess
import os

# The Field Mesh Map - These must match your router's static IP reservations.
FIELD_NODES = {
    "Node 4 (Secondary Master)": "192.168.1.11",
    "Node 2 (Red Hub)": "192.168.1.12",
    "Node 3 (Blue Hub)": "192.168.1.13"
}

def run_diagnostic():
    print("=" * 60)
    print("PI ARENA LITE: Network Mesh Diagnostic")
    print("Verifying 2026 REBUILT Practice Field Connectivity...")
    print("=" * 60)

    for name, ip in FIELD_NODES.items():
        # EDUCATIONAL NOTE:
        # ping -c 1: Send one "heartbeat" packet.
        # -W 1: Wait 1 second for a response before giving up.
        # stdout/stderr=DEVNULL: This prevents the raw system text from 
        # cluttering your clean Python output.
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result.returncode == 0:
            # Displays a green check for students to see it is safe to play.
            print(f"  [ ONLINE ] {name:<25} ({ip}) \u2705")
        else:
            # Displays a red X indicating a hardware or network failure.
            print(f"  [OFFLINE!] {name:<25} ({ip}) \u274c")

    print("=" * 60)
    print("Diagnostic Complete. All nodes must be ONLINE for match play.")
    print("=" * 60)

if __name__ == "__main__":
    run_diagnostic()
