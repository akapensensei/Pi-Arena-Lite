"""
Pi Arena Lite - common/constants.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

Copyright & Attribution:
- Core Match Logic: Derived from Cheesy Arena by Team 254 (The Cheesy Poofs).
- Technical Inspiration: Influence from Team 3476 (Code Orange).
- Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
- Implementation: Developed with assistance from Google Gemini.
"""

# MATCH TIMING (Seconds)
AUTO_DURATION = 15.0        # Autonomous period
TRANSITION_DURATION = 10.0  # Hub assessment & shift calculation
TELEOP_DURATION = 135.0     # Total Teleop including Endgame
SHIFT_DURATION = 25.0       # Duration of each active/inactive Alliance Shift
ENDGAME_START = 30.0        # Time remaining in match when Endgame begins

# SCORING VALUES
FUEL_AUTO_POINTS = 1        # 1pt per Fuel in Auto (per official rules)
FUEL_TELEOP_POINTS = 1      # 1pt per Fuel in an ACTIVE Hub during Teleop
AUTO_CLIMB_LEVEL_1 = 15     # Level 1 climb in Auto
TELEOP_CLIMB_LEVEL_1 = 10   # Level 1 climb in Endgame

# NETWORK SETTINGS
HEARTBEAT_INTERVAL = 0.5    # Seconds between node health checks
UDP_PORT = 5555             # Port for inter-node communication
