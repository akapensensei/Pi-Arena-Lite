#!/bin/bash
# ==============================================================================
# Pi Arena Lite - Network Mesh Diagnostic Tool
# ==============================================================================
# 
# DESCRIPTION:
# This script verifies that Node 1 (Master) can "see" the other 3 nodes 
# over the Wi-Fi and Ethernet links.
#
# HOW TO USE THIS SCRIPT:
# 1. Open the terminal on Node 1.
# 2. Make it executable: 
#    chmod +x /home/pi/frc2026/setup/ping_test.sh
# 3. Run it: 
#    /home/pi/frc2026/setup/ping_test.sh
#
# STUDENT NOTE:
# If a node is OFFLINE, it means the network packets aren't returning. 
# Check the 12V battery on the Hubs or the Ethernet cable to Node 4.
# ==============================================================================

# Target IP addresses for the 2026 REBUILT field mesh
MASTER_SEC="192.168.1.11"
HUB_RED="192.168.1.12"
HUB_BLUE="192.168.1.13"

echo "-------------------------------------------------------"
echo "PI ARENA LITE: Network Diagnostic Start"
echo "Verifying node connectivity..."
echo "-------------------------------------------------------"

# This function runs the actual 'ping' command for each node
check_node() {
    local NAME=$1
    local IP=$2
    
    # -c 2: Try twice | -W 2: Wait 2 seconds max
    if ping -c 2 -W 2 $IP > /dev/null 2>&1; then
        echo "   [ ONLINE ] $NAME ($IP) ✅"
    else
        echo "   [OFFLINE!] $NAME ($IP) ❌"
    fi
}

# Run the checks for all connected appliances
check_node "Node 4 (Sec. Master)" $MASTER_SEC
check_node "Node 2 (Red Hub)"    $HUB_RED
check_node "Node 3 (Blue Hub)"   $HUB_BLUE

echo "-------------------------------------------------------"
echo "Diagnostic Complete. Ready for Match Play?"
echo "-------------------------------------------------------"
