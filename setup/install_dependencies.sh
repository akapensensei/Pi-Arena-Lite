#!/bin/bash
# Pi Arena Lite - Installation Script for Raspberry Pi 5

echo "Installing Pi Arena Lite Dependencies..."

# Update System
sudo apt-get update && sudo apt-get upgrade -y

# Install Python Libraries
sudo apt-get install -y python3-pip python3-setuptools alsa-utils
sudo pip3 install rpi-ws281x gpiozero pygame

# Configure PWM for LEDs (GPIO 18)
echo "Configuring PWM for LED strips..."
if ! grep -q "dtparam=audio=off" /boot/config.txt; then
    echo "dtparam=audio=off" | sudo tee -a /boot/config.txt
    echo "Note: Onboard audio disabled to allow LED PWM. Using USB Audio."
fi

echo "Installation Complete. Please reboot your Pi 5."
