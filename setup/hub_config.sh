#!/bin/bash
# ==============================================================================
# Pi Arena Lite - Hub Node System Service Configuration (2026 REBUILT)
# 
# DESCRIPTION:
# This script creates a "System Service," which is a professional way to run 
# background tasks that do not need a screen. This ensures the scoring sensors 
# and Hub lights are always active in the background.
#
# EDUCATIONAL NOTE FOR STUDENTS:
# We are using 'systemd', the standard Linux service manager. This is powerful 
# because it includes 'Self-Healing' logic: if your Python code crashes or 
# the power blips, the OS will automatically restart it.
#
# Attribution:
# - Core State Logic: Adapted from Cheesy Arena (BSD 3-Clause) by Team 254 (The Cheesy Poofs).
# - Technical Inspiration: Influence from Team 3476 (Code Orange).
# - Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
# - Implementation: Developed as MIT-Licensed Open Source by Team 3476, 
#   with architectural assistance from Google Gemini.
# ==============================================================================

echo "Configuring Hub Node Background Service..."

# We write a service unit file to /etc/systemd/system/
# This requires 'sudo' because it is a protected system directory.
sudo bash -c 'cat <<EOF > /etc/systemd/system/piarena-hub.service
[Unit]
Description=Pi Arena Hub Controller
# Ensure the network is up before we try to talk to the Master node.
After=network.target

[Service]
# -u flag for "unbuffered" output so logs appear instantly in journalctl.
ExecStart=/usr/bin/python3 -u /home/pi/frc2026/hub_node/main.py
WorkingDirectory=/home/pi/frc2026
# SELF-HEALING: Restart the script after 5 seconds if it fails.
Restart=always
RestartSec=5
User=pi

[Install]
# Starts the service during the standard multi-user boot sequence.
WantedBy=multi-user.target
EOF'

# Tell the OS to look for the new configuration we just wrote.
sudo systemctl daemon-reload

# Enable the service (to start on boot) and start it (for right now).
sudo systemctl enable piarena-hub.service
sudo systemctl start piarena-hub.service

echo "SUCCESS: Hub Node is now an automated Background System Service."
