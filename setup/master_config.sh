#!/bin/bash
# ==============================================================================
# Pi Arena Lite - Master Node Auto-Boot Configuration
# 
# DESCRIPTION:
# This script turns a standard Raspberry Pi into a dedicated "Driver Station 
# Display." It configures the Desktop environment to launch the Scoring UI 
# as a standalone appliance immediately upon login.
#
# EDUCATIONAL NOTE FOR STUDENTS:
# We create a '.desktop' entry in the hidden .config/autostart folder. 
# In the Linux world, this is the standard way to tell the Graphical User 
# Interface (GUI) to launch a specific program as soon as it loads.
#
# Attribution:
# - Core State Logic: Adapted from Cheesy Arena by Team 254 The Cheesy Poofs (BSD 3-Clause).
# - Technical Inspiration: Influence from Team 3476 Code Orange.
# - Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
# - Implementation: Developed as MIT-Licensed Open Source by Team 3476 Code Orange, 
#   with architectural assistance from Google Gemini.
# ==============================================================================

echo "Configuring Master Node Appliance Mode..."

mkdir -p /home/pi/.config/autostart

cat <<EOF > /home/pi/.config/autostart/piarena.desktop
[Desktop Entry]
Type=Application
Name=Pi Arena Master
Exec=python3 /home/pi/frc2026/master_node/main.py
WorkingDirectory=/home/pi/frc2026
Terminal=false
EOF

chmod +x /home/pi/frc2026/master_node/main.py

echo "SUCCESS: Master Node UI is now a dedicated Driver Station Display."
