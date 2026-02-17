"""
================================================================================
Pi Arena Lite - master_node/ui_display.py
Distributed Practice Field Controller for FRC 2026: REBUILT™

STUDENT EDUCATIONAL OVERVIEW:
1. TKINTER: This is Python's built-in Graphical User Interface (GUI) library. 
   It is lightweight and perfect for "Appliance" displays on Raspberry Pi.
2. STRINGVARS: We use 'tk.StringVar' so that when the score changes in our 
   code, the text on the screen updates automatically without redrawing.
3. FULLSCREEN MODE: For a professional "FMS" feel, we force the window to 
   cover the entire screen and hide the desktop.

Attribution:
- Core State Logic: Adapted from Cheesy Arena by Team 254 The Cheesy Poofs (BSD 3-Clause).
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
        # Initialize the main window
        self.root = tk.Tk()
        self.root.title("Pi Arena Lite - 2026 REBUILT")
        
        # APPLIANCE SETTING: Cover the whole screen
        self.root.attributes('-fullscreen', True) 
        self.root.configure(bg='black')

        # HEADER: Match Phase and Timer
        self.state_label = tk.Label(self.root, text="WAITING FOR START", font=("Helvetica", 48), fg="white", bg="black")
        self.state_label.pack(pady=20)

        self.timer_label = tk.Label(self.root, text="02:30", font=("Helvetica", 120, "bold"), fg="yellow", bg="black")
        self.timer_label.pack(pady=10)

        # SCORE CONTAINER: Uses a 'Frame' to group Red and Blue side-by-side
        self.score_frame = tk.Frame(self.root, bg="black")
        self.score_frame.pack(expand=True, fill="both", padx=50)

        # RED ALLIANCE DISPLAY
        self.red_frame = tk.Frame(self.score_frame, bg="#CC0000", bd=10)
        self.red_frame.pack(side="left", expand=True, fill="both", padx=20, pady=20)
        tk.Label(self.red_frame, text="RED", font=("Helvetica", 40), fg="white", bg="#CC0000").pack()
        
        # Student Note: self.red_score_var acts as a "link" between code and screen
        self.red_score_var = tk.StringVar(value="0")
        tk.Label(self.red_frame, textvariable=self.red_score_var, font=("Helvetica", 150, "bold"), fg="white", bg="#CC0000").pack()

        # BLUE ALLIANCE DISPLAY
        self.blue_frame = tk.Frame(self.score_frame, bg="#0000CC", bd=10)
        self.blue_frame.pack(side="right", expand=True, fill="both", padx=20, pady=20)
        tk.Label(self.blue_frame, text="BLUE", font=("Helvetica", 40), fg="white", bg="#0000CC").pack()
        
        self.blue_score_var = tk.StringVar(value="0")
        tk.Label(self.blue_frame, textvariable=self.blue_score_var, font=("Helvetica", 150, "bold"), fg="white", bg="#0000CC").pack()

        # ADMIN ACCESS: Press Escape to exit fullscreen if you need to debug!
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))

    def update_display(self, time_left, state, r_score, b_score):
        """
        Updates the UI elements based on the current Match State.
        This is called every second by the Master's countdown loop.
        """
        self.timer_label.config(text=self.format_time(time_left))
        self.state_label.config(text=state)
        self.red_score_var.set(str(r_score))
        self.blue_score_var.set(str(b_score))

        # 2026 REBUILT VISUAL CUES: Change timer color based on phase
        if state == "AUTO":
            self.timer_label.config(fg="lime")   # Bright green for Auto
        elif state == "TELEOP":
            self.timer_label.config(fg="yellow") # Classic FRC yellow
        elif state == "ENDGAME":
            self.timer_label.config(fg="orange") # Warning color for final 30s

        # Force the screen to refresh
        self.root.update()

    def format_time(self, seconds):
        """Turns raw seconds into a readable MM:SS format."""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

    def run(self):
        """Starts the Tkinter 'Event Loop'."""
        self.root.mainloop()

# Test block: Can be run by students locally to see the UI without the whole field.
if __name__ == "__main__":
    ui = ScoringUI()
    ui.update_display(150, "TELEOP", 10, 10)
    ui.run()
