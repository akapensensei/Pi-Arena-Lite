#!/bin/bash
# ==============================================================================
# Pi Arena Lite - Master Node Configuration
#
# DESCRIPTION:
# This script turns a standard Raspberry Pi 5 into a dedicated 
# "Driver Station Display." It configures the graphical environment 
# to launch the Scoring UI as an appliance immediately upon boot.
#
# TARGET: Nodes 1 & 4
# ==============================================================================

echo "Initializing Master Node Appliance Mode..."

# Create the hidden autostart directory used by the LXDE Desktop Environment.
mkdir -p /home/pi/.config/autostart

# Write the Desktop Entry file.
# This is the 'instruction card' the OS reads to know what to launch.
cat <<EOT > /home/pi/.config/autostart/piarena.desktop
[Desktop Entry]
Type=Application
Name=Pi Arena Master
# Command to run:
Exec=python3 /home/pi/frc2026-practice-field/master_node/main.py
# Working Directory ensures assets/ and common/ are found:
WorkingDirectory=/home/pi/frc2026-practice-field
Terminal=false
EOT

# Set permissions to ensure the OS has the right to execute the main script.
chmod +x /home/pi/frc2026-practice-field/master_node/main.py

echo "SUCCESS: Master Node UI is now a dedicated Driver Station Display."
