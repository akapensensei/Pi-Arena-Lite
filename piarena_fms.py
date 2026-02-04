# Pi Arena Lite - Modular FRC FMS
#
# Part of: Pi Arena Lite - Modular FRC Practice Field Management System
# Copyright (c) 2026, Team 3476 (Code Orange)
# Developed with assistance from Google Gemini.
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

import time, json, threading, sqlite3, pygame, csv, io, os
from flask import Flask, render_template, jsonify, request, send_file
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

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

class PiArenaFMS:
    def __init__(self):
        self.match_state = "PRE_MATCH"
        self.time_left = 160
        self.match_number = 1
        self.scores = {"RED": {"balls": 0, "pts": 0}, "BLUE": {"balls": 0, "pts": 0}}
        self.move_bonus = {k: 0 for k in ['r1','r2','r3','b1','b2','b3']}
        self.hub_data = {"node2": {"online": False, "sensors": [False]*4}, 
                         "node3": {"online": False, "sensors": [False]*4},
                         "node4": {"online": False}}
        
        self.db_name = "rebuilt_2026.db"
        self.init_db()
        pygame.mixer.init()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY, match_num INTEGER, 
                r1 TEXT, r2 TEXT, r3 TEXT, b1 TEXT, b2 TEXT, b3 TEXT,
                r1_m INTEGER, r2_m INTEGER, r3_m INTEGER, b1_m INTEGER, b2_m INTEGER, b3_m INTEGER,
                red_pts INTEGER, blue_pts INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)""")

    def play_sound(self, sound):
        socketio.emit('play_sound', {'file': sound})
        try: pygame.mixer.Sound(f"sounds/{sound}.wav").play()
        except: pass

    def broadcast(self):
        m, s = divmod(max(0, self.time_left), 60)
        red_move = sum([self.move_bonus[k] for k in ['r1','r2','r3']]) * 3
        blue_move = sum([self.move_bonus[k] for k in ['b1','b2','b3']]) * 3
        
        socketio.emit('update_match', {
            'period': self.match_state,
            'time_str': f"{m}:{s:02d}",
            'red': {'pts': self.scores['RED']['pts'] + red_move, 'balls': self.scores['RED']['balls']},
            'blue': {'pts': self.scores['BLUE']['pts'] + blue_move, 'balls': self.scores['BLUE']['balls']}
        })
        socketio.emit('field_status', self.hub_data)

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

@app.route('/api/export/csv')
def export_csv():
    conn = sqlite3.connect(fms.db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM matches")
    rows = cursor.fetchall()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Match', 'R1', 'R2', 'R3', 'B1', 'B2', 'B3', 'R1m', 'R2m', 'R3m', 'B1m', 'B2m', 'B3m', 'RedFinal', 'BlueFinal', 'Time'])
    writer.writerows(rows)
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name="PiArena_Scouting.csv")

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=8080)
