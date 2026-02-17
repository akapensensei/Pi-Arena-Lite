#!/bin/bash
# ==============================================================================
# Pi Arena Lite - Hub Node Configuration Script
# 
# DESCRIPTION:
# This script creates a "System Service," which is a professional way to run 
# background tasks that do not need a screen. This ensures the scoring sensors 
# and Hub lights are always active in the background.
#
# EDUCATIONAL NOTE FOR STUDENTS:
# We are using 'systemd', the standard Linux service manager. This is powerful 
# because it includes 'Self-Healing' logic: if your Python code crashes or 
# the power blips, the OS will automatically restart it without human help.
#
# Attribution:
# - Core State Logic: Adapted from Cheesy Arena by Team 254 The Cheesy Poofs (BSD 3-Clause).
# - Technical Inspiration: Influence from Team 3476 Code Orange.
# - Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
# - Implementation: Developed as MIT-Licensed Open Source by Team 3476 Code Orange, 
#   with architectural assistance from Google Gemini.
# ==============================================================================

echo "Configuring Hub Node Background Service..."

# We write a service unit file to /etc/systemd/system/
sudo bash -c 'cat <<EOF > /etc/systemd/system/piarena-hub.service
[Unit]
Description=Pi Arena Hub Controller
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
WantedBy=multi-user.target
EOF'

sudo systemctl daemon-reload
sudo systemctl enable piarena-hub.service
sudo systemctl start piarena-hub.service

echo "SUCCESS: Hub Node is now an automated Background System Service."
