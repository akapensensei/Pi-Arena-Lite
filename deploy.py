# Pi Arena Lite - Deployment & Provisioning Tool
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

import tkinter as tk
from tkinter import messagebox
import paramiko, json, os, pygame
from scp import SCPClient

FIELD_NODES = [
    {"ip": "10.0.100.12", "role": "RED HUB", "cfg": "provisioning/node_2.json"},
    {"ip": "10.0.100.13", "role": "BLUE HUB", "cfg": "provisioning/node_3.json"},
    {"ip": "10.0.100.14", "role": "VISITOR DS", "cfg": "provisioning/node_4.json"}
]

class DeployTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Pi Arena Lite: Field Provisioner")
        self.root.geometry("500x550")
        pygame.mixer.init()

        msg = "VERIFY BEFORE DEPLOYMENT:\n" + "\n".join([f"• {n['role']} at {n['ip']}" for n in FIELD_NODES])
        tk.Label(root, text=msg, justify="left", padx=20, pady=20, font=("Arial", 10)).pack()
        
        tk.Button(root, text="🔊 TEST LOCAL AUDIO", command=self.test_audio).pack(pady=5)
        self.confirm = tk.BooleanVar()
        tk.Checkbutton(root, text="I have verified Node IPs & SSH Keys", variable=self.confirm, command=self.toggle).pack(pady=10)
        
        self.btn = tk.Button(root, text="PROVISION & PUSH AUDIO", state="disabled", bg="green", fg="white", 
                             command=self.start, font=("Arial", 12, "bold"), height=2)
        self.btn.pack(pady=20)
        self.status_label = tk.Label(root, text="Waiting...", fg="gray")
        self.status_label.pack()

    def test_audio(self):
        try: pygame.mixer.Sound("sounds/charge.wav").play()
        except: messagebox.showerror("Audio Error", "Check sounds/ folder.")

    def toggle(self):
        self.btn.config(state="normal" if self.confirm.get() else "disabled")

    def start(self):
        for node in FIELD_NODES:
            ip = node['ip']
            self.status_label.config(text=f"Deploying to {ip}...", fg="yellow")
            self.root.update()
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, username='pi', timeout=5)
                with SCPClient(ssh.get_transport()) as scp:
                    scp.put(node['cfg'], '/home/pi/frc2026/config.json')
                    scp.put('piarena_node.py', '/home/pi/frc2026/piarena_node.py')
                    if os.path.exists('sounds'):
                        ssh.exec_command("mkdir -p /home/pi/frc2026/sounds")
                        scp.put('sounds/', recursive=True, remote_path='/home/pi/frc2026/')
                ssh.exec_command("sudo pkill -f piarena_node.py; cd ~/frc2026 && nohup python3 piarena_node.py > node.log 2>&1 &")
                ssh.close()
            except Exception as e:
                messagebox.showerror("Failed", f"Error on {ip}: {e}")
                return
        self.status_label.config(text="ALL NODES ONLINE", fg="green")
        messagebox.showinfo("Success", "Field Provisioning Complete!")

if __name__ == "__main__":
    root = tk.Tk()
    DeployTool(root)
    root.mainloop()
