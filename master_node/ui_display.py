"""
Pi Arena Lite - master_node/ui_display.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

Copyright & Attribution:
- Core Match Logic: Derived from Cheesy Arena by Team 254 (The Cheesy Poofs).
- Technical Inspiration: Influence from Team 3476 (Code Orange).
- Game Rules: Based on official FIRST® REBUILT™ 2026 documentation.
- Implementation: Developed with assistance from Google Gemini.
"""

import tkinter as tk
from common.constants import *

class ScoringUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Pi Arena Lite - 2026 REBUILT")
        self.root.attributes('-fullscreen', True) # Maximize for Driver Station monitors
        self.root.configure(bg='black')

        # Header: Game State and Timer
        self.state_label = tk.Label(self.root, text="WAITING FOR START", font=("Helvetica", 48), fg="white", bg="black")
        self.state_label.pack(pady=20)

        self.timer_label = tk.Label(self.root, text="02:30", font=("Helvetica", 120, "bold"), fg="yellow", bg="black")
        self.timer_label.pack(pady=10)

        # Score Container
        self.score_frame = tk.Frame(self.root, bg="black")
        self.score_frame.pack(expand=True, fill="both", padx=50)

        # Red Alliance Score
        self.red_frame = tk.Frame(self.score_frame, bg="#CC0000", bd=10)
        self.red_frame.pack(side="left", expand=True, fill="both", padx=20, pady=20)
        tk.Label(self.red_frame, text="RED", font=("Helvetica", 40), fg="white", bg="#CC0000").pack()
        self.red_score_var = tk.StringVar(value="0")
        tk.Label(self.red_frame, textvariable=self.red_score_var, font=("Helvetica", 150, "bold"), fg="white", bg="#CC0000").pack()

        # Blue Alliance Score
        self.blue_frame = tk.Frame(self.score_frame, bg="#0000CC", bd=10)
        self.blue_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)
        tk.Label(self.blue_frame, text="BLUE", font=("Helvetica", 40), fg="white", bg="#0000CC").pack()
        self.blue_score_var = tk.StringVar(value="0")
        tk.Label(self.blue_frame, textvariable=self.blue_score_var, font=("Helvetica", 150, "bold"), fg="white", bg="#0000CC").pack()

        # Shutdown Key (Escape to exit fullscreen for admin work)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

    def update_display(self, time_left, state, r_score, b_score):
        """Update the numbers on the screen."""
        self.timer_label.config(text=self.format_time(time_left))
        self.state_label.config(text=state)
        self.red_score_var.set(str(r_score))
        self.blue_score_var.set(str(b_score))

        # Visual Cues for Game Phases
        if state == "AUTO":
            self.timer_label.config(fg="lime")
        elif state == "TELEOP":
            self.timer_label.config(fg="yellow")
        elif state == "ENDGAME":
            self.timer_label.config(fg="orange")
            # Flashing or extra border logic could go here

        self.root.update()

    def format_time(self, seconds):
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ui = ScoringUI()
    # Simple test loop
    ui.update_display(150, "TELEOP", 42, 38)
    ui.run()
