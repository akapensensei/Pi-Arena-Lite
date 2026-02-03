#!/bin/bash
# REBUILT 2026: Field Deployment Script (Linux/Pi)
# Portions Copyright (c) Team 254 (Cheesy Arena Lite)
# Licensed under the BSD 3-Clause License.

# --- CONFIGURATION ---
# IPs of your Raspberry Pi Nodes
FIELD_NODES=("10.0.100.12" "10.0.100.13" "10.0.100.14")
USER="pi"
REMOTE_DIR="~/frc2026"

echo "==============================================="
echo "   REBUILT 2026: STARTING FIELD APPLIANCES     "
echo "==============================================="

# 1. Start the Master FMS (Node 1)
echo "[1/3] Launching FMS Core on Node 1..."
# We run this in the background so the script can continue
nohup python3 fms_core.py > fms.log 2>&1 &
sleep 2

# 2. Start the Satellite Nodes (2, 3, and 4)
echo "[2/3] Connecting to Satellite Nodes..."
for IP in "${FIELD_NODES[@]}"
do
    echo "  --> Poking Node at $IP..."
    # This command connects via SSH, kills any old versions, and starts the new one
    ssh -o ConnectTimeout=5 $USER@$IP "
        sudo pkill -f frc2026_node.py;
        cd $REMOTE_DIR;
        nohup python3 frc2026_node.py > node.log 2>&1 &
    " &
done

# 3. Final Verification
echo "[3/3] Deployment sequence complete."
echo "-----------------------------------------------"
echo "Monitor: http://localhost:8080/pit"
echo "Scoreboard: http://localhost:8080/"
echo "-----------------------------------------------"
echo "Note: If Node 1 is an Intel PC, ensure USB speakers are ON."


