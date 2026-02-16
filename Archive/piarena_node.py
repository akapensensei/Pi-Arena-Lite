# Pi Arena Lite - Modular Field Node
#
# Part of: Pi Arena Lite - Modular FRC Practice Field Management System
# Copyright (c) 2026, Team 3476 (Code Orange)
# All rights reserved.
#
# Licensed under the BSD 3-Clause License
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import time, json, requests, threading, os, pygame
from RPi import GPIO
from rpi_ws281x import PixelStrip, Color
import socketio as sio_client

class PiArenaNode:
    def __init__(self, config_path="config.json"):
        with open(config_path) as f:
            self.cfg = json.load(f)
        
        self.master_url = f"http://{self.cfg['master_ip']}:8080"
        self.is_active = False
        self.deactivation_time = 0
        self.last_contact = time.time()
        self.sio = sio_client.Client()

        if self.cfg['role'] in ["MASTER", "DRIVER_STATION"]:
            pygame.mixer.init()
            self.setup_audio_sync()

        if self.cfg['role'] == "HUB":
            self.setup_hub()
        
        if self.cfg.get('reliability_settings', {}).get('hardware_watchdog'):
            try: self.wd = os.open("/dev/watchdog", os.O_WRONLY)
            except: print("Watchdog hardware not found")

    def setup_audio_sync(self):
        @self.sio.on('play_sound')
        def on_play_sound(data):
            try: pygame.mixer.Sound(f"sounds/{data['file']}.wav").play()
            except: pass
        try: self.sio.connect(self.master_url)
        except: pass

    def setup_hub(self):
        self.strip = PixelStrip(60, self.cfg.get('led_pin', 18), 800000, 10, False, 255, 0)
        self.strip.begin()
        self.color = Color(255,0,0) if self.cfg['alliance']=="RED" else Color(0,0,255)
        
        GPIO.setmode(GPIO.BCM)
        for i, pin in enumerate(self.cfg['sensor_pins']):
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=lambda x, idx=i: self.on_fuel(idx), bouncetime=150)

    def on_fuel(self, idx):
        if self.is_active or (time.time() - self.deactivation_time < 3.0):
            self.report_score(1, 1)
        else:
            self.report_score(1, 0)

    def report_score(self, balls, pts):
        try: requests.post(f"{self.master_url}/api/score", 
                          json={"alliance": self.cfg['alliance'], "balls": balls, "pts": pts}, timeout=0.2)
        except: pass

if __name__ == "__main__":
    node = PiArenaNode()
    while True:
        try:
            requests.post(f"{node.master_url}/api/heartbeat", json={"node_id": node.cfg['node_id']}, timeout=1)
            node.last_contact = time.time()
        except: pass
        if hasattr(node, 'wd'): os.write(node.wd, b'1')
        time.sleep(5)
