# Define the output file
output_file = "vlan_config.txt"

# Open the file for writing
with open(output_file, "w") as file:
    # Initialize VLAN and Interface counters
    vlan = 10  # VLAN starts at 10
    interface = 0  # First interface

    # Loop until we reach Ethernet508
    while interface <= 508:
        # Write commands for the first interface
        file.write(f"sudo config vlan add {vlan}\n")
        file.write(f"sudo config vlan member add -u {vlan} Ethernet{interface}\n")
        file.write(f"sudo config interface startup Ethernet{interface}\n")

        # Write commands for the second interface (increment by 4)
        second_interface = interface + 4
        if second_interface <= 508:
            file.write(f"sudo config vlan member add -u {vlan} Ethernet{second_interface}\n")
            file.write(f"sudo config interface startup Ethernet{second_interface}\n")

        # Move to the next VLAN and next set of interfaces
        vlan += 10  # Increment VLAN by 10
        interface += 8  # Move to the next block (Ethernet0, Ethernet4 → Ethernet8, Ethernet12)

print(f"VLAN configuration commands have been written to {output_file}")