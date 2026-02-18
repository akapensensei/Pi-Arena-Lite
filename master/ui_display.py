"""
================================================================================
Pi Arena Lite - master_node/ui_display.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

STUDENT EDUCATIONAL OVERVIEW:
1. MODE SELECTOR: We added a button that cycles through FULL, RED, and BLUE 
   modes. This allows mentors to "silence" half the field for debugging.
2. DYNAMIC UI: The background colors and labels change based on the selected 
   mode to give immediate visual feedback to the teams.

Attribution:
- Core Match Logic: Adapted from Cheesy Arena by Team 254 The Cheesy Poofs (BSD 3-Clause).
- Technical Inspiration: Influence from Team 3476 Code Orange.
- Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
- Implementation: Developed as MIT-Licensed Open Source by Team 3476 Code Orange, 
  with architectural assistance from Google Gemini.
================================================================================
"""

import tkinter as tk
from common.constants import *

class ScoringUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pi Arena Lite - 2026 REBUILT")
        self.root.attributes('-fullscreen', True) 
        self.root.configure(bg='black')

        # MODE SELECTOR: Allows solo practice for Red or Blue side
        self.mode_var = tk.StringVar(value="FULL")
        self.mode_button = tk.Button(
            self.root, 
            textvariable=self.mode_var, 
            command=self.toggle_field_mode,
            font=("Helvetica", 18, "bold"), 
            bg="#333", fg="white",
            relief="flat", pady=10
        )
        self.mode_button.pack(pady=10)

        # HEADER: Match Phase and Timer
        self.state_label = tk.Label(self.root, text="WAITING FOR START", font=("Helvetica", 48), fg="white", bg="black")
        self.state_label.pack(pady=10)

        self.timer_label = tk.Label(self.root, text="02:30", font=("Helvetica", 120, "bold"), fg="yellow", bg="black")
        self.timer_label.pack(pady=10)

        # SCORE CONTAINER
        self.score_frame = tk.Frame(self.root, bg="black")
        self.score_frame.pack(expand=True, fill="both", padx=50)

        # RED ALLIANCE DISPLAY
        self.red_frame = tk.Frame(self.score_frame, bg="#CC0000", bd=10)
        self.red_frame.pack(side="left", expand=True, fill="both", padx=20, pady=20)
        tk.Label(self.red_frame, text="RED ALLIANCE", font=("Helvetica", 40), fg="white", bg="#CC0000").pack()
        self.red_score_var = tk.StringVar(value="0")
        self.red_label = tk.Label(self.red_frame, textvariable=self.red_score_var, font=("Helvetica", 150, "bold"), fg="white", bg="#CC0000")
        self.red_label.pack()

        # BLUE ALLIANCE DISPLAY
        self.blue_frame = tk.Frame(self.score_frame, bg="#0000CC", bd=10)
        self.blue_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)
        tk.Label(self.blue_frame, text="BLUE ALLIANCE", font=("Helvetica", 40), fg="white", bg="#0000CC").pack()
        self.blue_score_var = tk.StringVar(value="0")
        self.blue_label = tk.Label(self.blue_frame, textvariable=self.blue_score_var, font=("Helvetica", 150, "bold"), fg="white", bg="#0000CC")
        self.blue_label.pack()

        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

    def toggle_field_mode(self):
        """Cycles through RED, BLUE, and FULL practice modes."""
        modes = ["FULL", "RED", "BLUE"]
        current = modes.index(self.mode_var.get())
        next_mode = modes[(current + 1) % len(modes)]
        self.mode_var.set(next_mode)
        
        # Visually dim the inactive side
        if next_mode == "RED":
            self.blue_frame.config(bg="#111"); self.blue_label.config(bg="#111", fg="#333")
            self.red_frame.config(bg="#CC0000"); self.red_label.config(bg="#CC0000", fg="white")
        elif next_mode == "BLUE":
            self.red_frame.config(bg="#111"); self.red_label.config(bg="#111", fg="#333")
            self.blue_frame.config(bg="#0000CC"); self.blue_label.config(bg="#0000CC", fg="white")
        else:
            self.red_frame.config(bg="#CC0000"); self.red_label.config(bg="#CC0000", fg="white")
            self.blue_frame.config(bg="#0000CC"); self.blue_label.config(bg="#0000CC", fg="white")

    def update_display(self, time_left, state, r_score, b_score):
        self.timer_label.config(text=self.format_time(time_left))
        self.state_label.config(text=state)
        self.red_score_var.set(str(r_score))
        self.blue_score_var.set(str(b_score))

        if state == "AUTO": self.timer_label.config(fg="lime")
        elif state == "TELEOP": self.timer_label.config(fg="yellow")
        elif state == "ENDGAME": self.timer_label.config(fg="orange")

        self.root.update()

    def format_time(self, seconds):
        return f"{int(seconds // 60):02d}:{int(seconds % 60):02d}"

    def run(self):
        self.root.mainloop()
