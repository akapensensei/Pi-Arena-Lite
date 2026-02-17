#!/bin/bash
# ==============================================================================
# Pi Arena Lite - Hub Node Configuration
#
# DESCRIPTION:
# This script creates a "System Service," which is a professional way 
# to run background tasks that don't need a screen. This ensures the 
# scoring sensors and field lights are always active in the background.
#
# TARGET: Nodes 2 & 3
# ==============================================================================

echo "Configuring Hub Node System Service..."

# We create a 'systemd' unit file. Path updated to shortened: /home/pi/frc2026/
sudo bash -c 'cat <<EOT > /etc/systemd/system/piarena-hub.service
[Unit]
Description=Pi Arena Hub Controller
After=network.target

[Service]
# 'python3 -u' ensures logs are sent to the system logger without delay.
ExecStart=/usr/bin/python3 -u /home/pi/frc2026/hub_node/main.py
WorkingDirectory=/home/pi/frc2026
# SELF-HEALING: If the script fails, the OS will restart it in 5 seconds.
Restart=always
RestartSec=5
User=pi

[Install]
# This line ensures the service starts during the standard boot sequence.
WantedBy=multi-user.target
EOT'

# Reload the system manager to recognize the new appliance service.
sudo systemctl daemon-reload

# Enable the service (for future boots) and start it (for right now).
sudo systemctl enable piarena-hub.service
sudo systemctl start piarena-hub.service

echo "SUCCESS: Hub Node is now a background System Service."
