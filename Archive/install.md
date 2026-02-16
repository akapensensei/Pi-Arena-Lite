# 🛠️ Pi Arena Lite: Installation & Setup Guide

This guide provides a step-by-step path to transforming a standard set of computers into a professional, synchronized **REBUILT 2026** practice field. By following this "Appliance" model, you only need to configure the Master PC; it will handle the rest of the field automatically.

---

## **Phase 1: Master Station Setup (Node 1 - PC/Master Pi)**

The Master Station is the central brain. It hosts the FMS, the Database, and the Deployment Tool.

1.  **System Preparation**:
    Open a terminal (`Ctrl+Alt+T`) and run:
    ```bash
    sudo apt update
    sudo apt install git python3-pip python3-tk python3-pygame -y
    ```

2.  **Clone the Repository**:
    ```bash
    cd ~
    git clone https://github.com
    cd Pi-Arena-Lite
    ```

3.  **Install Libraries**:
    The Master PC requires the full suite of libraries to manage the field:
    ```bash
    pip install -r requirements.txt --break-system-packages
    ```

4.  **Audio Setup**:
    Ensure the `sounds/` folder contains your official Table 5-4 `.wav` files (charge, buzzer, bells, powerup, whistle, foghorn).

---

## **Phase 2: Satellite Node Preparation (Nodes 2, 3, & 4)**

On each Raspberry Pi (the Hubs and Visitor Station), perform this **one-time** physical and firmware setup:

1.  **Enable Interfaces**:
    Run `sudo raspi-config` and enable:
    - **SSH** (Interface Options -> SSH)
    - **Watchdog** (Advanced Options -> Watchdog)

2.  **Enable Hardware Watchdog**:
    Open the boot config: `sudo nano /boot/config.txt`
    Add this line to the bottom: `dtparam=watchdog=on`
    Save (Ctrl+O) and Reboot (sudo reboot).

3.  **Create Project Directory**:
    ```bash
    mkdir -p ~/frc2026
    ```

---

## **Phase 3: SSH Trust (The "Skeleton Key")**

For the Master PC to "push" code and command the Pis without a password, you must establish trust.

1.  **Generate Key (On Node 1)**:
    ```bash
    ssh-keygen -t rsa -b 4096
    ```
    *(Press Enter for all prompts. Do NOT set a passphrase.)*

2.  **Copy Key to Each Pi**:
    Run these commands for each of your nodes (replace IPs if yours are different):
    ```bash
    ssh-copy-id pi@10.0.100.12
    ssh-copy-id pi@10.0.100.13
    ssh-copy-id pi@10.0.100.14
    ```

---

## **Phase 4: Field Provisioning (The "Push")**

You do not need to manually install software on the Hubs. The Master PC handles it via the `deploy.py` script.

1.  **Configure**:
    Ensure your `config.json` files are ready in the `provisioning/` folder on Node 1. Update the `master_ip` to `10.0.100.5`.

2.  **Run the Provisioner**:
    ```bash
    python3 deploy.py
    ```

3.  **Deployment Options**:
    - **START DEPLOYMENT**: Copies code, pushes audio to Node 4, and launches the field.
    - **FORCE RE-INSTALL**: Check this if a Pi is brand new; it will force-install the required packages on the satellite nodes.

---

## **Phase 5: Automation (Optional Appliance Mode)**

To make the field start automatically on power-up, set up a system service on each node.

1.  **Create Service**: `sudo nano /etc/systemd/system/piarena.service`
2.  **Configuration**:
    ```ini
    [Unit]
    Description=Pi Arena Lite Appliance
    After=network.target

    [Service]
    User=pi
    WorkingDirectory=/home/pi/Pi-Arena-Lite
    ExecStart=/usr/bin/python3 piarena_fms.py
    Restart=always
    RestartSec=5

    [Install]
    WantedBy=multi-user.target
    ```
3.  **Enable**: `sudo systemctl daemon-reload && sudo systemctl enable piarena.service`

---

## **Phase 6: Verification Checklist**
- [ ] **FMS IP**: Is Node 1 set to a static IP of `10.0.100.5`?
- [ ] **Pit Dashboard**: Open `http://10.0.100.5` - Are Hubs Green?
- [ ] **Sensors**: Wave a ball in the Hub - Does the Pit Dashboard "Beam" light up?
- [ ] **Audio**: Press the USB Panic Button - Do both Node 1 and Node 4 play the Foghorn?
- [ ] **Scouting**: Complete a match and click "Export Scouting CSV" to verify data logging.
