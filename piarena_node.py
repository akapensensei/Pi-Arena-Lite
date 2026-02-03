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

        # Audio Setup (Node 1 and Node 4)
        if self.cfg['role'] in ["MASTER", "DRIVER_STATION"]:
            pygame.mixer.init()
            self.setup_audio_sync()

        # Hub Setup (Nodes 2 & 3)
        if self.cfg['role'] == "HUB":
            self.setup_hub()

        if self.cfg.get('reliability_settings', {}).get('hardware_watchdog'):
            self.wd = os.open("/dev/watchdog", os.O_WRONLY)

    def setup_audio_sync(self):
        @self.sio.on('play_sound')
        def on_play_sound(data):
            try: pygame.mixer.Sound(f"sounds/{data['file']}.wav").play()
            except: pass
        try: self.sio.connect(self.master_url)
        except: print("FMS Audio Sync Offline")

    def setup_hub(self):
        self.strip = PixelStrip(60, self.cfg['led_pin'], 800000, 10, False, 255, 0)
        self.strip.begin()
        self.color = Color(255,0,0) if self.cfg['alliance']=="RED" else Color(0,0,255)
        GPIO.setmode(GPIO.BCM)
        for i, pin in enumerate(self.cfg['sensor_pins']):
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(pin, GPIO.FALLING, callback=lambda x, idx=i: self.on_fuel(idx), bouncetime=150)

    def on_fuel(self, idx):
        now = time.time()
        # 3s Scoring Buffer Rule
        if self.is_active or (now - self.deactivation_time < 3.0):
            self.report(1, 1) # Simplified: Master handles multipliers
        else:
            self.report(1, 0)

    def report(self, balls, pts):
        try: requests.post(f"{self.master_url}/api/score", json={"alliance": self.cfg['alliance'], "balls": balls, "pts": pts}, timeout=0.2)
        except: pass

    def heartbeat_loop(self):
        while True:
            try:
                requests.post(f"{self.master_url}/api/heartbeat", json={"node_id": self.cfg['node_id']}, timeout=1)
                self.last_contact = time.time()
            except:
                if self.cfg['reliability_settings']['reboot_on_network_loss']:
                    if time.time() - self.last_contact > 60: os.system('sudo reboot')
            if hasattr(self, 'wd'): os.write(self.wd, b'1')
            time.sleep(5)

if __name__ == "__main__":
    node = PiArenaNode()
    threading.Thread(target=node.heartbeat_loop, daemon=True).start()
    while True: time.sleep(1)
