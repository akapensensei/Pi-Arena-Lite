"""
================================================================================
Pi Arena Lite - setup/ping_test.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

STUDENT EDUCATIONAL OVERVIEW:
1. SUBPROCESS: This module allows Python to "talk" to the Linux OS. It runs 
   the system 'ping' command exactly as if a student typed it into the terminal.
2. DICTIONARIES: We store our Field IPs in Key-Value pairs {Name: IP}. This
   makes the code "Infrastructure as Code"—easy to read and easy to expand.
3. EXIT CODES: Every computer command returns a number. '0' indicates success. 
   In networking, a '0' means the node answered the heartbeat (echo request).
4. MESH VALIDATION: In a distributed system, this script is your first line 
   of defense. If a Hub is offline, the Practice Modes (RED/BLUE) cannot 
   function correctly.

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

# The Field Mesh Map - These must match your static IP reservations in the router.
# Students: If you add a "Node 5" in the future, just add a new line here!
FIELD_NODES = {
    "Node 4 (Secondary Master)": "192.168.1.11",
    "Node 2 (Red Hub)": "192.168.1.12",
    "Node 3 (Blue Hub)": "192.168.1.13"
}

def run_diagnostic():
    print("=" * 65)
    print("PI ARENA LITE: Network Mesh Diagnostic Tool")
    print("Verifying Connectivity for Team 3476 Practice Field...")
    print("=" * 65)

    for name, ip in FIELD_NODES.items():
        # EDUCATIONAL NOTE:
        # ping -c 1: Send one "heartbeat" packet.
        # -W 1: Wait 1 second for a response before marking the node as dead.
        # stdout/stderr=DEVNULL: This hides the messy system text from the user.
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # In Linux, a Return Code of 0 means "Success"
        if result.returncode == 0:
            # \u2705 is the Unicode for the green check mark
            print(f"  [ ONLINE ] {name:<25} ({ip}) \u2705")
        else:
            # \u274c is the Unicode for the red X
            print(f"  [OFFLINE!] {name:<25} ({ip}) \u274c")

    print("=" * 65)
    print("DIAGNOSTIC COMPLETE.")
    print("Tip: If a Hub is OFFLINE, check the 12V battery and Wi-Fi signal.")
    print("=" * 65)

if __name__ == "__main__":
    run_diagnostic()

