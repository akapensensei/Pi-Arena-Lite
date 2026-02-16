#!/bin/bash
# Pi Arena Lite - Installation Script for Raspberry Pi 5
# Distributed Practice Field Controller for FRC 2026: REBUILT™

echo "-------------------------------------------------------"
echo "Initializing Pi Arena Lite Setup..."
echo "Credits: Team 254 (Logic), Team 3476 (Inspiration)"
echo "-------------------------------------------------------"

# 1. Update System Repositories
echo "[1/4] Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install System-Level Dependencies
# python3-tk: For the master_node UI
# alsa-utils: For USB speaker management
# libsdl2-mixer-2.0-0: Required by pygame for match audio
echo "[2/4] Installing system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-setuptools \
    python3-tk \
    alsa-utils \
    libsdl2-mixer-2.0-0 \
    git

# 3. Install Python Libraries
# rpi-ws281x: For Node 2/3 Hub LEDs
# gpiozero: For Hub Break-Beams and Master Node interrupts
# pygame: For official Table 5-4 audio cues
echo "[3/4] Installing Python modules..."
sudo pip3 install rpi-ws281x gpiozero pygame --break-system-packages

# 4. Hardware Configuration for LEDs (PWM Fix)
# The Pi 5 uses the same PWM timer for onboard audio and GPIO 18.
# Since you are using USB Speakers, we disable onboard audio to prevent LED flickering.
echo "[4/4] Configuring hardware for LED PWM (GPIO 18)..."
if ! grep -q "dtparam=audio=off" /boot/config.txt; then
    echo "dtparam=audio=off" | sudo tee -a /boot/config.txt
    echo "SUCCESS: Onboard audio disabled. LED PWM enabled."
else
    echo "SKIP: PWM audio conflict already resolved in /boot/config.txt."
fi

# Create Assets directory if it doesn't exist
mkdir -p ../assets

echo "-------------------------------------------------------"
echo "SETUP COMPLETE!"
echo "1. Place your sound files in the /assets/ folder."
echo "2. Please REBOOT your Pi 5 now to apply PWM changes."
echo "-------------------------------------------------------"
