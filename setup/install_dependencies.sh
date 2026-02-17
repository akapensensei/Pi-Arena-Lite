#!/bin/bash
# ==============================================================================
# Pi Arena Lite - Universal Installation Script
# 
# DESCRIPTION:
# This script prepares a Raspberry Pi 4 or 5 to act as a node in the 
# Pi Arena Lite mesh. It installs system libraries, Python modules, 
# and handles the hardware-specific PWM/Audio conflicts.
#
# EDUCATIONAL NOTE FOR STUDENTS:
# We use 'grep' to check the hardware version. This allows one script to 
# manage multiple generations of hardware (Pi 4 vs Pi 5).
#
# Attribution:
# - Core State Logic: Adapted from Cheesy Arena (BSD 3-Clause) by Team 254 (The Cheesy Poofs).
# - Technical Inspiration: Influence from Team 3476 (Code Orange).
# - Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
# - Implementation: Developed as MIT-Licensed Open Source by Team 3476, 
#  with architectural assistance from Google Gemini.
# ==============================================================================

echo "-------------------------------------------------------"
echo "PI ARENA LITE: Hardware Initialization"
echo "-------------------------------------------------------"

# 1. Update the Operating System
echo "[1/4] Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install Core System Tools
# python3-tk: Required for the Master UI
# alsa-utils: Required for USB Audio management
echo "[2/4] Installing system-level dependencies..."
sudo apt-get install -y python3-pip python3-setuptools python3-tk alsa-utils git

# 3. Install Python Modules
# --break-system-packages is required on modern 'Bookworm' OS versions
echo "[3/4] Installing Python libraries (GPIO, LEDs, Audio)..."
sudo pip3 install rpi-ws281x gpiozero pygame --break-system-packages

# 4. Hardware-Specific PWM Fix (The "Contributor's Fix")
# GPIO 18 (used for LEDs) conflicts with onboard audio on both Pi 4 and 5.
echo "[4/4] Optimizing hardware for LED PWM (GPIO 18)..."

# Detect Hardware Version
PI_MODEL=$(cat /proc/device-tree/model)
echo "   Detected: $PI_MODEL"

if ! grep -q "dtparam=audio=off" /boot/config.txt; then
    echo "   Action: Disabling onboard audio to free up PWM timers..."
    echo "dtparam=audio=off" | sudo tee -a /boot/config.txt
    echo "   NOTE: You must use USB SPEAKERS for match audio."
else
    echo "   Action: Audio conflict already resolved."
fi

echo "-------------------------------------------------------"
echo "INSTALLATION COMPLETE"
echo "Please reboot your Pi to apply the hardware changes."
echo "-------------------------------------------------------"
