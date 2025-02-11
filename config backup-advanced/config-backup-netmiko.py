import os
import paramiko
from typing import Dict, Tuple
import time

# Define backup directory
BACKUP_DIR = "cisco_configs"
os.makedirs(BACKUP_DIR, exist_ok=True)

# Devices and their corresponding credentials
# Format: "hostname": (ip, username, password)
devices: Dict[str, Tuple[str, str, str]] = {
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

def get_device_config(hostname: str, ip: str, username: str, password: str) -> bool:
    """
    Retrieve configuration from a device using SSH and save it to a file.
    
    Args:
        hostname: Device hostname
        ip: Device IP address
        username: SSH username
        password: SSH password
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Initialize SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the device
        print(f"Fetching configuration from {hostname} at {ip}...")
        ssh.connect(ip, username=username, password=password, timeout=10)
        
        # Send command and get output
        stdin, stdout, stderr = ssh.exec_command("show running-config")
        config = stdout.read().decode()
        
        # Save configuration to file
        output_file = os.path.join(BACKUP_DIR, f"{hostname}_config.txt")
        with open(output_file, 'w') as f:
            f.write(config)
            
        print(f"Configuration for {hostname} saved to {output_file}")
        return True
        
    except Exception as e:
        print(f"Failed to retrieve configuration for {hostname}: {str(e)}")
        return False
        
    finally:
        ssh.close()

def main():
    """Main function to backup configurations from all devices."""
    successful_backups = 0
    failed_backups = 0
    
    for hostname, (ip, username, password) in devices.items():
        if get_device_config(hostname, ip, username, password):
            successful_backups += 1
        else:
            failed_backups += 1
        # Add a small delay between connections to prevent overwhelming the network
        time.sleep(1)
    
    print("\nBackup Summary:")
    print(f"Configuration backup completed. Files are saved in {BACKUP_DIR}")
    print(f"Successful backups: {successful_backups}")
    print(f"Failed backups: {failed_backups}")

if __name__ == "__main__":
    main()