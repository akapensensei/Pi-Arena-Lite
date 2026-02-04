# Pi Arena Lite - Deployment & Provisioning Tool
import tkinter as tk
from tkinter import messagebox
import paramiko, json, os
from scp import SCPClient

# Define Appliance Map (Matches your GitHub provisioning folder)
FIELD_NODES = [
    {"ip": "10.0.100.12", "role": "RED HUB", "cfg": "provisioning/node_2.json"},
    {"ip": "10.0.100.13", "role": "BLUE HUB", "cfg": "provisioning/node_3.json"},
    {"ip": "10.0.100.14", "role": "VISITOR DS", "cfg": "provisioning/node_4.json"}
]

class DeployTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Pi Arena Lite: Field Provisioner")
        
        msg = "VERIFY BEFORE DEPLOYMENT:\n" + "\n".join([f"• {n['role']} at {n['ip']}" for n in FIELD_NODES])
        tk.Label(root, text=msg, justify="left", padx=20, pady=20).pack()
        
        self.confirm = tk.BooleanVar()
        tk.Checkbutton(root, text="I have verified Node IPs & SSH Keys", variable=self.confirm, command=self.toggle).pack()
        
        self.btn = tk.Button(root, text="PROVISION FIELD", state="disabled", bg="green", fg="white", command=self.start)
        self.btn.pack(pady=20)

    def toggle(self):
        self.btn.config(state="normal" if self.confirm.get() else "disabled")

    def start(self):
        for node in FIELD_NODES:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(node['ip'], username='pi', timeout=5)
                
                with SCPClient(ssh.get_transport()) as scp:
                    scp.put(node['cfg'], '/home/pi/frc2026/config.json')
                    scp.put('piarena_node.py', '/home/pi/frc2026/piarena_node.py')
                
                ssh.exec_command("sudo pkill -f piarena_node.py; cd ~/frc2026 && nohup python3 piarena_node.py > node.log 2>&1 &")
                ssh.close()
            except Exception as e:
                messagebox.showerror("Error", f"Failed on {node['ip']}: {e}")
                return
        messagebox.showinfo("Success", "All Nodes Provisioned and Launched!")

if __name__ == "__main__":
    root = tk.Tk()
    DeployTool(root)
    root.mainloop()
