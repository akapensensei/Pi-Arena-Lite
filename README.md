# 🏟️ Pi Arena Lite
### Distributed Field Management System for FRC 2026: REBUILT™

**Pi Arena Lite** is a modular, Python-based field management system designed to run on a mesh of Raspberry Pi 4/5 nodes. It handles timing, scoring, and 2026 game logic without the need for industrial PLCs.

---

## 🏗️ Repository Structure
- **`/master_node`**: UI, Audio, and Match State logic (Nodes 1 & 4).
- **`/hub_node`**: Sensor and LED logic (Nodes 2 & 3).
- **`/common`**: Shared constants, network utilities, and CSV logging.
- **`/setup`**: Infrastructure-as-Code scripts for auto-boot and networking.
- **`/docs`**: Full [Admin Guide](docs/ADMIN_GUIDE.md) and [Scouting/CSV Guide](docs/CSV_GUIDE.md).

## 🚀 Quick Start
1. Clone to all 4 nodes: `git clone https://github.com[Your-Repo]/frc2026`
2. Run `setup/install_dependencies.sh` on all nodes.
3. Configure IPs in `common/config.json`.
4. Run `setup/master_config.sh` (Masters) or `setup/hub_config.sh` (Hubs) to enable Appliance Mode.

## ⚖️ Attribution & License
- **Architectural Inspiration:** Based on the match-flow logic of **Cheesy Arena (Team 254 The Cheesy Poofs)**.
- **Technical Influence:** **Team 3476 Code Orange**.
- **Implementation:** Custom Python 3 modular build for Raspberry Pi.
- **License:** MIT License. See `LICENSE` for details.

## 🏗️ Repository Map
```text
frc2026/
├── assets/                     # Official Table 5-4 Audio Cues (.wav)
├── common/                     # Shared Logic & Networking (All Nodes)
├── master_node/                # Driver Station Logic (Nodes 1 & 4)
├── hub_node/                   # Field Goal Logic (Nodes 2 & 3)
├── setup/                      # Infrastructure as Code (Setup & Appliance Config)
│   ├── install_dependencies.sh # System & Hardware Prep
│   ├── master_config.sh        # UI Autostart Configuration
│   ├── hub_config.sh           # Systemd Service Configuration
│   ├── kiosk_config.sh         # Mouse/Taskbar Hiding
│   ├── piarena.service         # Systemd Service Template
│   ├── ping_test.sh            # Bash Mesh Diagnostic
│   └── ping_test.py            # Python Mesh Diagnostic (Educational)
├── docs/                       # System Documentation & Manuals
├── LICENSE                     # MIT License
└── README.md                   # You are here.
```
