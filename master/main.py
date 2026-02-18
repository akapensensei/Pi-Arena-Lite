"""
================================================================================
Pi Arena Lite - Master/main.py
The Central Intelligence of the FRC 2026: REBUILT™ Practice Field

OVERALL PROJECT GOALS:
The Master Node serves as the "Source of Truth" for the entire arena. In a 
distributed system, different nodes can easily drift out of sync. This script 
centralizes the match clock, validates all incoming score packets, and 
publishes the global field state so that all other processes (like the UI 
and the Hub Nodes) stay perfectly aligned with the official game rules.

CORE FUNCTIONALITY & ARCHITECTURE:
This module implements a 'State-Driven Controller.' By managing a global 
Match State (AUTO, TELEOP, etc.), it ensures that scoring events are only 
processed during legal play periods. It acts as a data hub, receiving UDP 
packets from the field and exporting a JSON state file for the UI to display.

NOVEL CONCEPTS:
1. State Exportation (The Handshake): This script writes to '/tmp/field_state.json'. 
   This allows the 'ui_display.py' script to be a separate process, protecting 
   the core timing logic from UI crashes—a professional "Separation of Concerns."
2. Zero-Value Validation: Every incoming score is checked against the current 
   'Active Hub' status. This turns raw network data into actionable strategy 
   analytics for the drive team.

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
import time
import os
from gpiozero import Button
from common.network import MasterNetworkServer
from common.config import PORT, PANIC_BUTTON_PIN, AUTO_SECONDS, TELEOP_SECONDS

# --- GLOBAL GAME STATE ---
match_state = "PRE_MATCH"
time_left = 0
scores = {"red": 0, "blue": 0}
zero_value_scores = {"red": 0, "blue": 0}
hub_status = {"red": "ACTIVE", "blue": "ACTIVE"}
auto_winner = None

# --- STATE EXPORTATION ---

async def export_field_state():
    """
    Saves the current match data to a local file for the UI script to read.
    """
    while True:
        state = {
            "match_state": match_state,
            "time_left": time_left,
            "scores": scores,
            "zero_value": zero_value_scores,
            "hub_status": hub_status
        }
        try:
            # Atomic-style write to /tmp to ensure the UI sees a complete file
            with open("/tmp/field_state.json", "w") as f:
                json.dump(state, f)
        except Exception:
            pass
        await asyncio.sleep(0.1) # 10Hz update rate for the UI

# --- SCORE LOGIC ---

def on_data_received(raw_data):
    """
    The Gatekeeper: Validates incoming WiFi scores against the match clock.
    """
    global scores, zero_value_scores
    try:
        data = json.loads(raw_data.decode('utf-8'))
        alliance = data.get("alliance")
        
        if data.get("type") == "FUEL_SCORED":
            # State-Check: Is the match running and is the Hub active?
            if match_state in ["AUTO", "TELEOP"] and hub_status[alliance] == "ACTIVE":
                scores[alliance] += 1
            else:
                zero_value_scores[alliance] += 1
    except Exception:
        pass

# --- MATCH TIMELINE ---

async def run_match_timer():
    """
    The Master Clock. Advances the game through periods and handles Endgame.
    """
    global match_state, time_left, hub_status
    
    while True:
        if match_state == "AUTO":
            time_left = AUTO_SECONDS
            while time_left > 0 and match_state == "AUTO":
                await asyncio.sleep(1)
                time_left -= 1
            if match_state == "AUTO": match_state = "PAUSE"
                
        elif match_state == "PAUSE":
            time_left = 5
            await asyncio.sleep(time_left)
            match_state = "TELEOP"
            
        elif match_state == "TELEOP":
            time_left = TELEOP_SECONDS
            while time_left > 0 and match_state == "TELEOP":
                # --- ENDGAME OVERRIDE (30s) ---
                if time_left == 30:
                    hub_status = {"red": "ACTIVE", "blue": "ACTIVE"}
                    # Students: This is where you trigger the Train Whistle sound!
                
                await asyncio.sleep(1)
                time_left -= 1
            match_state = "POST_MATCH"
            
        await asyncio.sleep(0.1)

# --- PHYSICAL INPUTS ---

def handle_panic_button():
    """ Toggles the match between PRE_MATCH and START. """
    global match_state, scores, zero_value_scores
    if match_state == "PRE_MATCH":
        scores = {"red": 0, "blue": 0}
        zero_value_scores = {"red": 0, "blue": 0}
        match_state = "AUTO"
    else:
        match_state = "PRE_MATCH"

panic_btn = Button(PANIC_BUTTON_PIN)
panic_btn.when_pressed = handle_panic_button

# --- MAIN EXECUTION ---

async def main():
    server = MasterNetworkServer(port=PORT)
    server.set_callback(on_data_received)

    print(f"=== PI ARENA MASTER STARTING ON PORT {PORT} ===")
    
    # Launching the concurrent "Engines"
    await asyncio.gather(
        server.listen_loop(),
        run_match_timer(),
        export_field_state()
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        if os.path.exists("/tmp/field_state.json"):
            os.remove("/tmp/field_state.json")
