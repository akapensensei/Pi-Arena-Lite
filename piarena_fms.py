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



import time, json, threading, sqlite3, pygame, csv
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit

# --- 2026 REBUILT OFFICIAL TIMELINE ---
TIMELINE = [
    ("AUTO", 20, True, True, "charge"),
    ("TRANSITION", 3, False, False, "buzzer"),
    ("SHIFT 1", 25, True, False, "bells"),
    ("SHIFT 2", 25, False, True, "powerup"),
    ("SHIFT 3", 25, True, False, "powerup"),
    ("SHIFT 4", 12, False, True, "powerup"),
    ("ENDGAME", 30, True, True, "whistle"),
    ("POST_MATCH", 0, False, False, "buzzer")
]

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

class PiArenaFMS:
    def __init__(self):
        self.match_state = "PRE_MATCH"
        self.time_left = 160
        self.match_num = 1
        self.scores = {"RED": {"balls": 0, "pts": 0}, "BLUE": {"balls": 0, "pts": 0}}
        self.hub_data = {"node2": {"online": False, "sensors": [False]*4}, 
                         "node3": {"online": False, "sensors": [False]*4},
                         "node4": {"online": False}}
        
        pygame.mixer.init()
        self.db_name = "rebuilt_2026.db"
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS matches (id INTEGER PRIMARY KEY, match_num INTEGER, red_pts INTEGER, blue_pts INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")

    def play_sound(self, sound_file):
        socketio.emit('play_sound', {'file': sound_file}) # Syncs Node 4 Speaker
        try:
            pygame.mixer.Sound(f"sounds/{sound_file}.wav").play()
        except: pass

    def run_match(self):
        self.scores = {"RED": {"balls": 0, "pts": 0}, "BLUE": {"balls": 0, "pts": 0}}
        total_elapsed = 0
        for period, duration, r_act, b_act, sound in TIMELINE:
            self.match_state = period
            self.play_sound(sound)
            p_start = time.time()
            while time.time() - p_start < duration:
                if self.match_state == "STOPPED": return
                self.time_left = 160 - total_elapsed - int(time.time() - p_start)
                self.broadcast()
                time.sleep(0.5)
            total_elapsed += duration
        self.save_match()

    def broadcast(self):
        m, s = divmod(max(0, self.time_left), 60)
        socketio.emit('update_match', {'period': self.match_state, 'time_str': f"{m}:{s:02d}", 'red': self.scores['RED'], 'blue': self.scores['BLUE']})
        socketio.emit('field_status', self.hub_data)

    def save_match(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO matches (match_num, red_pts, blue_pts) VALUES (?, ?, ?)", (self.match_num, self.scores['RED']['pts'], self.scores['BLUE']['pts']))
        self.match_num += 1

fms = PiArenaFMS()

@app.route('/')
def index(): return render_template('audience.html')

@app.route('/pit')
def pit(): return render_template('pit.html')

@app.route('/api/score', methods=['POST'])
def update_score():
    data = request.json
    fms.scores[data['alliance']]['balls'] += data.get('balls', 0)
    fms.scores[data['alliance']]['pts'] += data.get('pts', 0)
    return jsonify({"status": "ok"})

@app.route('/api/heartbeat', methods=['POST'])
def heartbeat():
    data = request.json
    node = f"node{data.get('node_id')}"
    if node in fms.hub_data:
        fms.hub_data[node]['online'] = True
        if 'sensors' in data: fms.hub_data[node]['sensors'] = data['sensors']
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8080)
