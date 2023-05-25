import subprocess
import time
import sys
import os
from tqdm import tqdm

# Importing required modules
if os.name == "posix":  # Unix-based
    import select
    import termios
else:  # Windows
    import msvcrt

# Generate list of target IP addresses
targets = [f"76.144.{i}.0/24" for i in range(1, 256)]

# Create a progress bar with the total number of targets
pbar = tqdm(total=len(targets), desc="Scanning")

# Flag to indicate whether to update the progress bar
update_progress = False

# Function to check if the Enter key is pressed
def is_enter_pressed():
    if os.name == "posix":  # Unix-based system
        dr, dw, de = select.select([sys.stdin], [], [], 0)
        return dr != []
    else:  # Windows
        return msvcrt.kbhit() and msvcrt.getch() == b'\r'

for target in targets:
    command = f"nmap -sC -sV -Pn -p 25565 {target}"
    
    # Run the command and capture the output
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    
    # Search for open ports in the output
    open_ports = []
    lines = output.split("\n")
    for line in lines:
        if "open" in line:
            port = line.split("/")[0]
            open_ports.append(port)
    
    # Display the open ports
    if open_ports:
        print(f"Open ports for {target}:")
        print(", ".join(open_ports))
        print("-----------------------")
    
    # Update the progress bar
    pbar.update(1)
    
    # Check if Enter key is pressed to update the progress
    if is_enter_pressed():
        update_progress = True
    
    # Display updated progress and results if Enter key is pressed
    if update_progress:
        pbar.set_postfix_str(f"Targets Scanned: {pbar.n}/{pbar.total}")
        pbar.refresh()
        update_progress = False

# Close the progress bar
pbar.close()