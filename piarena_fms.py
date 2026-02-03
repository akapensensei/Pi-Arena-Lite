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
import threading
import sqlite3
import pygame
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO

# --- 2026 REBUILT OFFICIAL TIMELINE ---
# Period: (Duration, Red_Active, Blue_Active, Audio_Cue)
TIMELINE = [
    ("AUTO", 20, True, True, "START"),
    ("TRANSITION", 3, False, False, "END_AUTO"),
    ("SHIFT 1", 25, True, False, "TELEOP"),
    ("SHIFT 2", 25, False, True, "SHIFT"),
    ("SHIFT 3", 25, True, False, "SHIFT"),
    ("SHIFT 4", 12, False, True, "SHIFT"),
    ("ENDGAME", 30, True, True, "ENDGAME"),
    ("POST_MATCH", 0, False, False, "MATCH_END")
]

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

class FMSCore:
    def __init__(self):
        self.match_state = "PRE_MATCH"
        self.time_left = 160
        self.match_number = 1
        self.scores = {
            "RED": {"balls": 0, "pts": 0},
            "BLUE": {"balls": 0, "pts": 0}
        }
        self.hub_data = {
            "node2": {"online": False, "sensors": [False]*4},
            "node3": {"online": False, "sensors": [False]*4},
            "node4": {"online": False}
        }
        
        # Initialize Audio (USB Speaker)
        pygame.mixer.init()
        self.sounds = {
            "START": pygame.mixer.Sound("sounds/charge.wav"),
            "END_AUTO": pygame.mixer.Sound("sounds/buzzer.wav"),
            "TELEOP": pygame.mixer.Sound("sounds/bells.wav"),
            "SHIFT": pygame.mixer.Sound("sounds/powerup.wav"),
            "ENDGAME": pygame.mixer.Sound("sounds/whistle.wav"),
            "MATCH_END": pygame.mixer.Sound("sounds/buzzer.wav"),
            "STOP": pygame.mixer.Sound("sounds/foghorn.wav")
        }
        
        # Initialize Database
        self.db_name = "rebuilt_2026.db"
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_num INTEGER,
                red_pts INTEGER,
                blue_pts INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )""")

    def play_sound(self, key):
        if key in self.sounds:
            self.sounds[key].play()

    def run_match(self):
        self.scores = {"RED": {"balls": 0, "pts": 0}, "BLUE": {"balls": 0, "pts": 0}}
        total_time = 0
        
        for period, duration, red_act, blue_act, sound in TIMELINE:
            self.match_state = period
            self.play_sound(sound)
            
            start_period = time.time()
            while time.time() - start_period < duration:
                if self.match_state == "STOPPED": return
                self.time_left = 160 - total_time - int(time.time() - start_period)
                self.broadcast_update()
                time.sleep(0.5)
            
            total_time += duration
        
        self.save_to_db()
        self.match_state = "POST_MATCH"
        self.match_number += 1

    def broadcast_update(self):
        mins, secs = divmod(max(0, self.time_left), 60)
        socketio.emit('update_match', {
            'period': self.match_state,
            'time_str': f"{mins}:{secs:02d}",
            'red': self.scores['RED'],
            'blue': self.scores['BLUE']
        })
        socketio.emit('field_status', self.hub_data)

    def save_to_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO matches (match_num, red_pts, blue_pts) VALUES (?, ?, ?)",
                        (self.match_number, self.scores['RED']['pts'], self.scores['BLUE']['pts']))

fms = FMSCore()

# --- API ENDPOINTS ---
@app.route('/')
def audience(): return render_template('audience.html')

@app.route('/pit')
def pit(): return render_template('pit.html')

@app.route('/api/status')
def status():
    return jsonify({"period": fms.match_state, "time": fms.time_left})

@app.route('/api/score', methods=['POST'])
def update_score():
    data = request.json
    alliance = data.get('alliance') # "RED" or "BLUE"
    fms.scores[alliance]['balls'] += data.get('balls', 0)
    fms.scores[alliance]['pts'] += data.get('pts', 0)
    return jsonify({"status": "ok"})

@app.route('/api/heartbeat', methods=['POST'])
def heartbeat():
    data = request.json
    node = f"node{data.get('node_id')}"
    if node in fms.hub_data:
        fms.hub_data[node]['online'] = True
        if 'sensors' in data:
            fms.hub_data[node]['sensors'] = data['sensors']
    return jsonify({"status": "received"})

if __name__ == "__main__":
    # In a real setup, trigger run_match via the USB button logic
    # For now, starts server on Node 1 IP
    socketio.run(app, host='0.0.0.0', port=8080, debug=False)




