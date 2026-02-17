"""
================================================================================
Pi Arena Lite - common/network_utils.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

STUDENT EDUCATIONAL OVERVIEW:
1. UDP vs TCP: Most websites use TCP (which checks for every packet). 
   Robotics uses UDP because it is "Fire and Forget." It is much faster, 
   which is critical for real-time scoring.
2. JSON: We "package" our data into a JSON string (like a digital envelope) 
   so the Master node knows exactly what the Hub is reporting.
3. PORTS: Think of the IP as the building address and the PORT as the 
   specific door. Pi Arena Lite always uses Port 5555.

================================================================================
Attribution:
- Core State Logic: Adapted from Cheesy Arena (BSD 3-Clause) by Team 254 (The Cheesy Poofs).
- Technical Inspiration: Influence from Team 3476 (Code Orange).
- Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
- Implementation: Developed as MIT-Licensed Open Source by Team 3476, 
  with architectural assistance from Google Gemini.
================================================================================
"""

import socket
import json
import threading
from common.constants import UDP_PORT

class ArenaNetwork:
    def __init__(self, node_role, target_ips=None):
        self.node_role = node_role
        self.target_ips = target_ips or []
        # Create a UDP Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        try:
            self.sock.bind(('', UDP_PORT))
        except OSError:
            print(f"[NET] Port {UDP_PORT} Busy.")

    def listen(self, callback):
        """
        Threading Lesson: We run this in the background so the node 
        can 'hear' messages while still doing its main job.
        """
        def listener():
            while True:
                data, addr = self.sock.recvfrom(1024)
                # 'Unpack' the digital envelope
                decoded = json.loads(data.decode('utf-8'))
                callback(decoded, addr)

        threading.Thread(target=listener, daemon=True).start()

    def send_score_update(self, alliance, points, master_ip):
        """Sends a 'Score Increment' packet to the Master."""
        packet = {"type": "SCORE_INC", "alliance": alliance, "points": points}
        message = json.dumps(packet).encode('utf-8')
        self.sock.sendto(message, (master_ip, UDP_PORT))
