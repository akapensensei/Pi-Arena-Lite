# Pi Arena Lite - Deployment & Provisioning Tool
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
        self.root.geometry("500x600")
        pygame.mixer.init()

        msg = "VERIFY BEFORE DEPLOYMENT:\n" + "\n".join([f"• {n['role']} at {n['ip']}" for n in FIELD_NODES])
        tk.Label(root, text=msg, justify="left", padx=20, pady=20, font=("Arial", 10)).pack()
        
        self.reinstall_var = tk.BooleanVar()
        tk.Checkbutton(root, text="FORCE RE-INSTALL DEPENDENCIES", variable=self.reinstall_var).pack(pady=5)

        self.confirm_var = tk.BooleanVar()
        tk.Checkbutton(root, text="I have verified Node IPs & SSH Keys", variable=self.confirm_var, command=self.toggle).pack(pady=10)
        
        self.btn = tk.Button(root, text="PROVISION FIELD", state="disabled", bg="green", fg="white", 
                             command=self.start, font=("Arial", 12, "bold"), height=2)
        self.btn.pack(pady=20)
        self.status = tk.Label(root, text="Status: Ready", fg="gray")
        self.status.pack()

    def toggle(self):
        self.btn.config(state="normal" if self.confirm_var.get() else "disabled")

    def start(self):
        for node in FIELD_NODES:
            ip = node['ip']
            self.status.config(text=f"Deploying to {ip}...", fg="yellow")
            self.root.update()
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, username='pi', timeout=5)
                if self.reinstall_var.get():
                    ssh.exec_command("sudo pip install rpi-ws281x requests socketio-client --break-system-packages")
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
        self.status.config(text="ALL NODES ONLINE", fg="green")
        messagebox.showinfo("Success", "Provisioning Complete!")

if __name__ == "__main__":
    root = tk.Tk()
    DeployTool(root)
    root.mainloop()
