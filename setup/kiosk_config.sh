#!/bin/bash
# ==============================================================================
# Pi Arena Lite - Kiosk Polish Script
# 
# DESCRIPTION:
# Hides the mouse cursor (using unclutter) and prevents the screen from
# blanking/sleeping during a match.
#
# Attribution:
# - Core State Logic: Derived from Cheesy Arena by Team 254 The Cheesy Poofs.
# - Technical Inspiration: Influence from Team 3476 Code Orange.
# - Implementation: Developed as MIT-Licensed Open Source by Team 3476 Code Orange, 
#   with architectural assistance from Google Gemini.
# ==============================================================================

echo "Applying Kiosk Polish to Master Node..."

# Install 'unclutter' to hide the mouse cursor after 5 seconds of inactivity
sudo apt-get install -y unclutter

# Add Kiosk commands to the autostart file we created earlier
# 1. Hide mouse | 2. Disable screen saver | 3. Disable power management
cat <<EOF >> /home/pi/.config/autostart/piarena.desktop
Exec=unclutter -idle 5
Exec=xset s off
Exec=xset s noblank
Exec=xset -dpms
EOF

echo "SUCCESS: Master Node will now operate in Kiosk Mode."
