import os
from netmiko import ConnectHandler
import time

# Create backup directory
BACKUP_DIR = "cisco_configs"
os.makedirs(BACKUP_DIR, exist_ok=True)

# List of devices with their credentials
devices = {
    "clab-twitch-ebgp-ispx-01": ("172.20.20.4", "admin", "admin"),
    "clab-twitch-ebgp-ispx-02": ("172.20.20.18", "admin", "admin"),
    "clab-twitch-ebgp-ispx-10": ("172.20.20.3", "admin", "admin"),
    "clab-twitch-ebgp-ispz-01": ("172.20.20.8", "admin", "admin"),
    "clab-twitch-ebgp-ispz-02": ("172.20.20.9", "admin", "admin"),
    "clab-twitch-ebgp-ispz-10": ("172.20.20.10", "admin", "admin"),
    "clab-twitch-ebgp-twitch-r1": ("172.20.20.6", "admin", "cisco123"),
    "clab-twitch-ebgp-twitch-r2": ("172.20.20.19", "admin", "cisco123"),
    "clab-twitch-ebgp-twitch-r3": ("172.20.20.7", "admin", "cisco123"),
    "clab-twitch-ebgp-twitch-r4": ("172.20.20.20", "admin", "cisco123"),
    "clab-twitch-ebgp-twitch-r5": ("172.20.20.21", "admin", "cisco123"),
    "clab-twitch-ebgp-twitch-xrd-rr-01": ("172.20.20.2", "clab", "clab@123"),
    "clab-twitch-ebgp-twitch-xrd-rr-02": ("172.20.20.5", "clab", "clab@123"),
}

# Keep track of successful and failed backups
successful_backups = 0
failed_backups = 0

# Go through each device in the list
for hostname in devices:
    # Get the device details
    ip = devices[hostname][0]
    username = devices[hostname][1]
    password = devices[hostname][2]
    
    print(f"Trying to connect to {hostname} at {ip}...")
    
    try:
        # Create the device connection details for Netmiko
        device = {
            'device_type': 'cisco_ios',  # or 'cisco_xr' for IOS-XR devices
            'host': ip,
            'username': username,
            'password': password,
            'port': 22,  # SSH port
            'timeout': 20,  # Timeout in seconds
        }
        
        # Connect to the device
        connection = ConnectHandler(**device)
        
        # Get the running configuration
        config = connection.send_command("show running-config")
        
        # Create the output file name
        output_file = os.path.join(BACKUP_DIR, f"{hostname}_config.txt")
        
        # Save the configuration to a file
        with open(output_file, 'w') as f:
            f.write(config)
            
        print(f"Successfully saved configuration for {hostname} to {output_file}")
        successful_backups += 1
        
        # Properly close the connection
        connection.disconnect()
        
    except Exception as e:
        # If anything goes wrong, print the error
        print(f"Failed to backup {hostname}: {str(e)}")
        failed_backups += 1
    
    # Wait a bit before connecting to the next device
    time.sleep(1)

# Print final summary
print("\nBackup Summary:")
print(f"Configuration backup completed. Files are saved in {BACKUP_DIR}")
print(f"Successful backups: {successful_backups}")
print(f"Failed backups: {failed_backups}")