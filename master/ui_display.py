"""
================================================================================
Pi Arena Lite - Master/ui_display.py
The Numerical Audience Display for FRC 2026: REBUILT™

OVERALL PROJECT GOALS:
This script provides the "Situational Awareness" for the drive team. By 
replicating the official FMS (Field Management System) numerical ratios, 
drivers can instantly see their progress toward the 100/360 Fuel thresholds. 
The goal is to remove visual clutter and provide high-speed data.

CORE FUNCTIONALITY:
This is a 'Read-Only' script. It does not calculate scores or run the match 
timer. Instead, it "observes" a shared state file (/tmp/field_state.json) 
written by the Master Controller. This separation ensures that if the UI 
crashes, the match timing and scoring logic remain unaffected.

NOVEL CONCEPTS:
1. Dynamic Denominators: The target threshold automatically flips from /100 
   to /360 once the first Ranking Point is achieved.
2. Analytics Transparency: This UI displays 'Zero-Value Scores' as a 
   sub-metric, helping coaches identify strategy timing errors in real-time.

================================================================================
Attribution:
- Technical Inspiration: Influence from Team 3476 (Code Orange).
- Implementation: Developed as MIT-Licensed Open Source by Team 3476, 
  with architectural assistance from Google Gemini.
================================================================================
"""

import time
import json
import os

# --- FIELD DEFINITIONS ---
STATE_FILE = "/tmp/field_state.json"
THRESHOLD_ENERGIZED = 100
THRESHOLD_SUPERCHARGED = 360

def render_fms_ui():
    """
    Main Loop: Clears the screen and draws the numerical FMS scoreboard.
    """
    while True:
        try:
            # Step 1: Check if the Master Controller has started yet
            if not os.path.exists(STATE_FILE):
                print(">>> WAITING FOR MASTER CONTROLLER...")
                time.sleep(1)
                continue

            # Step 2: Read the 'Source of Truth' from the Master
            with open(STATE_FILE, "r") as f:
                data = json.load(f)

            # Step 3: Clear Terminal (ANSI Escape for no-flicker)
            print("\033[H\033[J", end="") 
            
            # --- HEADER ---
            print("="*60)
            print(f"  MATCH TIME: {data['time_left']:03d}s   |   STATE: {data['match_state']}")
            print("="*60)

            # --- ALLIANCE SCORING ---
            for alliance in ["red", "blue"]:
                fuel = data['scores'][alliance]
                
                # Dynamic RP Logic: Flip the target denominator as they score
                if fuel < THRESHOLD_ENERGIZED:
                    target = THRESHOLD_ENERGIZED
                    rp_icon = "[ ]" # Not yet Energized
                elif fuel < THRESHOLD_SUPERCHARGED:
                    target = THRESHOLD_SUPERCHARGED
                    rp_icon = "[●]" # Energized!
                else:
                    target = fuel
                    rp_icon = "[✸]" # Supercharged!

                # Main Display Line: "RED  142 / 360  [●]"
                print(f"\n {alliance.upper():5} ALLIANCE:  {fuel:3} / {target:3}   {rp_icon}")
                
                # Strategy Note: Display Zero-Value Scores for coaching
                zv = data['zero_value'].get(alliance, 0)
                if zv > 0:
                    print(f"   (Zero-Value Scores: {zv})")

            print("\n" + "="*60)
            
        except Exception:
            # If the Master is currently writing to the file, we just skip one frame
            pass
        
        time.sleep(0.25) # 4Hz refresh rate is ideal for human readability

if __name__ == "__main__":
    try:
        render_fms_ui()
    except KeyboardInterrupt:
        print("\nUI Display Terminated.")
