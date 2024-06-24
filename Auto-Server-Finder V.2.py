import subprocess
import sys
import os
from tqdm import tqdm

# Importing required modules
if os.name == "posix":  # Unix-based
    import select
    import termios
else:  # Windows
    import msvcrt

# Function to check if the Enter key is pressed
def is_enter_pressed():
    if os.name == "posix":  # Unix-based system
        dr, dw, de = select.select([sys.stdin], [], [], 0)
        return dr != []
    else:  # Windows
        return msvcrt.kbhit() and msvcrt.getch() == b'\r'

# Function to scan a single target
def scan_target(target):
    command = f"nmap -Pn -p 25565 {target}"
    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    open_ports = []
    lines = output.split("\n")
    for line in lines:
        if "open" in line:
            port = line.split("/")[0]
            open_ports.append(port)
    return output, open_ports

# Main function
def main():
    base_ip = input("Enter the base IP address (e.g., 192.168.5): ")
    save_dir = input("Enter the directory to save scan results: ")
    os.makedirs(save_dir, exist_ok=True)
    
    targets = [f"{base_ip}.{i}" for i in range(1, 255)]
    save_file = os.path.join(save_dir, f"{base_ip.replace('.', '_')}_scan.txt")

    total_targets = len(targets)
    open_count = 0
    closed_count = 0
    open_ips = []

    # Create a progress bar with the total number of targets
    pbar = tqdm(total=total_targets, desc="Scanning")

    with open(save_file, 'w') as f:
        for target in targets:
            output, open_ports = scan_target(target)
            f.write(f"Results for {target}:\n{output}\n")
            if open_ports:
                open_count += 1
                open_ips.append(target)
                print(f"Open ports for {target}:")
                print(", ".join(open_ports))
                print("-----------------------")
            else:
                closed_count += 1

            # Update the progress bar
            pbar.update(1)

            # Check if Enter key is pressed to update the progress
            if is_enter_pressed():
                pbar.set_postfix_str(f"Scanned: {pbar.n}, Open: {open_count} (IPs: {', '.join(open_ips)}), Closed: {closed_count}")
                pbar.refresh()

    # Close the progress bar
    pbar.close()

    # Final summary
    print(f"Final Summary:\nScanned: {total_targets}\nOpen: {open_count} (IPs: {', '.join(open_ips)})\nClosed: {closed_count}")

if __name__ == "__main__":
    main()
