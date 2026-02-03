# Pi Arena Lite - Modular FRC Practice Field Management System
# Copyright (c) 2026, Team 3476 (Code Orange)
# Portions Copyright (c) Team 254 (Cheesy Arena Lite)
# All rights reserved.
#
# Licensed under the BSD 3-Clause License.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.

import time
import json
import requests
import threading
import os
from RPi import GPIO
from rpi_ws281x import PixelStrip, Color

class FieldNode:
    def __init__(self, config_path="config.json"):
        # Load Appliance Identity
        with open(config_path) as f:
            self.cfg = json.load(f)
        
        self.node_id = self.cfg['node_id']
        self.role = self.cfg['role']
        self.alliance = self.cfg['alliance']
        self.master_url = f"http://{self.cfg['master_ip']}:8080"
        
        # Scoring State
        self.is_active = False
        self.deactivation_time = 0
        self.current_period = "PRE_MATCH"
        self.sensor_states = [False] * 4
        
        # Reliability Settings
        self.rel = self.cfg.get('reliability_settings', {})
        self.last_contact = time.time()
        self.wd_handle = None

        if self.role == "HUB":
            self.setup_hardware()
        
        if self.rel.get('hardware_watchdog', True):
            self.start_watchdog()

    def setup_hardware(self):
        # 1. LED Strip Setup (WS2812B)
        # GPIO 18 (PWM0) used for data
        self.strip = PixelStrip(60, self.cfg['led_pin'], 800000, 10, False, 255, 0)
        self.strip.begin()
        self.color = Color(255, 0, 0) if self.alliance == "RED" else Color(0, 0, 255)

        # 2. Sensor Setup (12V Proximity via Optocoupler)
        GPIO.setmode(GPIO.BCM)
        for i, pin in enumerate(self.cfg['sensor_pins']):
            # PUD_UP assumes optocoupler pulls to GND when ball detected
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.FALLING, 
                                  callback=lambda ch, idx=i: self.on_fuel_break(idx), 
                                  bouncetime=150)

    def start_watchdog(self):
        try:
            self.wd_handle = os.open("/dev/watchdog", os.O_WRONLY)
        except Exception as e:
            print(f"Watchdog error: {e}")

    def on_fuel_break(self, sensor_index):
        """Rule: Count if Hub is Active OR within 3s Buffer."""
        now = time.time()
        scored = False
        
        # Logic for "In-Flight" scoring buffer
        if self.is_active or (now - self.deactivation_time < self.cfg['scoring_buffer']):
            scored = True
            pts = 2 if self.current_period == "AUTO" else 1
            self.report_score(1, pts)
        else:
            self.report_score(1, 0) # Ball counted, 0 points

    def report_score(self, balls, pts):
        try:
            requests.post(f"{self.master_url}/api/score", 
                          json={"alliance": self.alliance, "balls": balls, "pts": pts},
                          timeout=0.5)
        except:
            pass

    def sync_with_fms(self):
        """Polls Node 1 for match state and sends health heartbeat."""
        while True:
            try:
                # Get Match State
                r = requests.get(f"{self.master_url}/api/status", timeout=1)
                if r.status_code == 200:
                    data = r.json()
                    self.current_period = data['period']
                    # logic to determine if this hub should be active
                    # (In production, the Master sends Hub state directly)
                    self.last_contact = time.time()

                # Send Health Heartbeat (Sensors status for Pit Display)
                requests.post(f"{self.master_url}/api/heartbeat",
                             json={"node_id": self.node_id, "sensors": self.sensor_states},
                             timeout=1)
            except:
                if self.rel.get('reboot_on_network_loss') and (time.time() - self.last_contact > self.rel.get('network_timeout_seconds', 60)):
                    os.system('sudo reboot')
            
            # Pat the Hardware Watchdog
            if self.wd_handle:
                os.write(self.wd_handle, b'1')
            
            time.sleep(self.rel.get('heartbeat_interval', 5))

    def led_animator(self):
        """Handles 2026 Shift visuals and the 3s pulsing warning."""
        while True:
            if not self.is_active:
                for i in range(60): self.strip.setPixelColor(i, Color(0,0,0))
            else:
                # Check for pulsing (add pulsing logic here based on timer)
                for i in range(60): self.strip.setPixelColor(i, self.color)
            self.strip.show()
            time.sleep(0.05)

if __name__ == "__main__":
    node = FieldNode()
    if node.role == "HUB":
        threading.Thread(target=node.led_animator, daemon=True).start()
    node.sync_with_fms()



