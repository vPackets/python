#!/bin/bash

# Define backup directory
BACKUP_DIR="cisco_configs"
mkdir -p "$BACKUP_DIR"

# Devices and their corresponding credentials
declare -A devices=(
    ["clab-twitch-ebgp-ispx-01"]="172.20.20.4 admin admin"
    ["clab-twitch-ebgp-ispx-02"]="172.20.20.18 admin admin"
    ["clab-twitch-ebgp-ispx-10"]="172.20.20.3 admin admin"
    ["clab-twitch-ebgp-ispz-01"]="172.20.20.8 admin admin"
    ["clab-twitch-ebgp-ispz-02"]="172.20.20.9 admin admin"
    ["clab-twitch-ebgp-ispz-10"]="172.20.20.10 admin admin"
    ["clab-twitch-ebgp-twitch-r1"]="172.20.20.6 cisco cisco123"
    ["clab-twitch-ebgp-twitch-r2"]="172.20.20.19 cisco cisco123"
    ["clab-twitch-ebgp-twitch-r3"]="172.20.20.7 cisco cisco123"
    ["clab-twitch-ebgp-twitch-r4"]="172.20.20.20 cisco cisco123"
    ["clab-twitch-ebgp-twitch-r5"]="172.20.20.21 cisco cisco123"
    ["clab-twitch-ebgp-twitch-xrd-rr-01"]="172.20.20.2 clab clab@123"
    ["clab-twitch-ebgp-twitch-xrd-rr-02"]="172.20.20.5 clab clab@123"
)

# Iterate through each device and retrieve the configuration
for device in "${!devices[@]}"; do
    IFS=' ' read -r ip username password <<< "${devices[$device]}"
    output_file="$BACKUP_DIR/${device}_config.txt"

    echo "Fetching configuration from $device at $ip..."

    # Use sshpass with SSH to login and retrieve configuration
    sshpass -p "$password" ssh -o StrictHostKeyChecking=no "$username@$ip" "show running-config" > "$output_file"

    if [ $? -eq 0 ]; then
        echo "Configuration for $device saved to $output_file."
    else
        echo "Failed to retrieve configuration for $device."
    fi
done

echo "Configuration backup completed. Files are saved in $BACKUP_DIR."