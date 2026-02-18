"""
================================================================================
Pi Arena Lite - common/network.py
The communication framework for the FRC 2026 practice field.

OVERALL PROJECT GOALS:
This module provides the communication framework that connects hardware nodes. In a fast-paced robotics environment, 
the network must be fast, reliable, and invisible. The goal is to ensure that a physical event (such as a ball 
breaking a beam) is reflected in the Master Node's logic with minimal delay.

CORE FUNCTIONALITY & ARCHITECTURE:
The module uses a Dual-Role Networking Engine with Python's 'asyncio' framework. It handles "Non-Blocking I/O," 
meaning the Raspberry Pi can send or receive data while running other tasks. 

NOVEL CONCEPTS:
1. UDP vs TCP: TCP (Transmission Control Protocol) checks every packet. UDP (User Datagram Protocol) is "Fire and 
   Forget," making it faster. This is important for real-time scoring.
2. Callback Injection: The Master server is "logic-agnostic." It receives data and sends it to a 'callback' 
   function. This lets programmers change game rules in main.py without changing the network engine.
3. Queue Buffering: An 'asyncio.Queue' is used as a "To-Do" list. If multiple events occur quickly, the Hub 
   places them in the queue and returns to the sensor. The network engine processes the queue as fast as possible.

================================================================================
Attribution:
- Core State Logic: Adapted from Cheesy Arena (BSD 3-Clause) by Team 254.
- Technical Inspiration: Influence from Team 3476 (Code Orange).
- Implementation: Developed as MIT-Licensed Open Source by Team 3476, 
  with architectural assistance from Google Gemini.
================================================================================
"""

import asyncio
import json
import socket

class ArenaNetworkNode:
    """
    The 'Outbound Engine' used by Hub Nodes to report field events.
    Students: This class handles the 'Client' side of the UDP connection.
    """
    def __init__(self, target_ip, port):
        self.target_ip = target_ip
        self.port = port
        self.queue = asyncio.Queue()

    async def run_engine(self):
        """
        Maintains the lifecycle of the UDP socket.
        It continuously watches the 'To-Do' list (queue) and fires 
        packets at the Master as they arrive.
        """
        loop = asyncio.get_event_loop()
        
        # SOCK_DGRAM specifies UDP (User Datagram Protocol)
        # AF_INET specifies IPv4 addressing
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(False)

        while True:
            # Step 1: Wait for a dictionary message from the Hub logic
            message_dict = await self.queue.get()
            
            try:
                # Step 2: Convert Python objects to JSON "envelopes" for transmission
                packet = json.dumps(message_dict).encode('utf-8')
                # Step 3: Fire-and-Forget non-blocking send
                await loop.sock_sendto(sock, packet, (self.target_ip, self.port))
            except Exception:
                # In UDP, we log the error but keep the engine running
                pass
            
            self.queue.task_done()

    def send_message(self, message_dict):
        """
        Thread-safe method to queue a message for the next available 
        transmission window.
        """
        self.queue.put_nowait(message_dict)


class MasterNetworkServer:
    """
    The 'Inbound Engine' used by the Master Node to listen for field data.
    Students: This class acts as the 'Server' that funnels raw network traffic 
    into the high-level game logic.
    """
    def __init__(self, port):
        self.port = port
        self.callback = None 

    def set_callback(self, func):
        """
        Plugs a specific function (like on_data_received) into the 
        network engine's data stream.
        """
        self.callback = func

    async def listen_loop(self):
        """
        Listens on a specific port for any incoming UDP data.
        As data arrives, it is immediately handed to the callback function.
        """
        loop = asyncio.get_event_loop()
        
        # Bind the socket to the configured port to begin 'Listening'
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', self.port))
        sock.setblocking(False)

        while True:
            # Step 1: Wait for raw bytes from the field without freezing the Pi
            data, addr = await loop.sock_recvfrom(sock, 1024)
            
            # Step 2: If a callback is registered, pass the data to main.py
            if self.callback:
                # The callback performs the JSON decoding and scoring rules
                self.callback(data)
            
            # Step 3: Tiny yield to allow other background tasks (like display/timer) to run
            await asyncio.sleep(0.001)
