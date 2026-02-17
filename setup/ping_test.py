"""
Pi Arena Lite - Python Network Diagnostic Tool
File: /home/pi/frc2026/setup/ping_test.py

EDUCATIONAL NOTE FOR STUDENTS:
In Python, we use the 'subprocess' module to "talk" to the Operating System. 
This script runs the system 'ping' command and looks at the 'returncode'.
- Return Code 0: Success (The node is there!)
- Return Code Non-Zero: Failure (The node is missing!)
"""

import subprocess
import os

# Dictionary of our Field Mesh IPs
# Students: You can easily add more nodes here in the future!
FIELD_NODES = {
    "Node 4 (Secondary Master)": "192.168.1.11",
    "Node 2 (Red Hub)": "192.168.1.12",
    "Node 3 (Blue Hub)": "192.168.1.13"
}

def check_field_mesh():
    print("-" * 50)
    print("PI ARENA LITE: Python Diagnostic Start")
    print("Verifying 2026 REBUILT Network Mesh...")
    print("-" * 50)

    for name, ip in FIELD_NODES.items():
        # subprocess.run executes the system ping command
        # -c 1: Send one "heartbeat" packet
        # -W 1: Wait 1 second for a response
        # stdout/stderr=DEVNULL hides the messy terminal output
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result.returncode == 0:
            print(f"[ ONLINE ] {name:<25} ({ip}) ✅")
        else:
            print(f"[OFFLINE!] {name:<25} ({ip}) ❌")

    print("-" * 50)
    print("Diagnostic Complete. Happy Practicing!")
    print("-" * 50)

if __name__ == "__main__":
    check_field_mesh()
