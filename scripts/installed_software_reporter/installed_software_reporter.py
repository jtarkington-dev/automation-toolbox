import os
import csv
import winreg
import logging
import datetime
from pathlib import Path
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# --- Setup log paths and logging ---
script_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(script_dir, "logs")
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
txt_log_file = os.path.join(log_dir, f"installed_software_{timestamp}.txt")
csv_log_file = os.path.join(log_dir, f"installed_software_{timestamp}.csv")

logging.basicConfig(
    filename=txt_log_file,
    level=logging.INFO,
    format='%(message)s'
)

def log_and_print(message, color=None):
    if color:
        print(color + message + Style.RESET_ALL)
    else:
        print(message)
    logging.info(message)

# --- Collect installed software from Windows Registry ---
def get_software_from_registry(hive, subkey):
    software_list = []
    try:
        with winreg.OpenKey(hive, subkey) as key:
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name) as subkey_handle:
                        name = winreg.QueryValueEx(subkey_handle, 'DisplayName')[0]
                        values = [winreg.EnumValue(subkey_handle, j) for j in range(winreg.QueryInfoKey(subkey_handle)[1])]
                        version = next((v[1] for v in values if v[0] == 'DisplayVersion'), 'Unknown')
                        publisher = next((v[1] for v in values if v[0] == 'Publisher'), 'Unknown')
                        install_location = next((v[1] for v in values if v[0] == 'InstallLocation'), 'Unknown')
                        software_list.append((name, version, publisher, install_location))
                except Exception:
                    continue
    except FileNotFoundError:
        pass
    return software_list

# --- Scan Program Files directories for additional folders ---
def scan_common_program_dirs():
    paths = [
        Path(os.environ['ProgramFiles']),
        Path(os.environ['ProgramFiles(x86)']) if 'ProgramFiles(x86)' in os.environ else None
    ]
    found = []
    for path in paths:
        if path and path.exists():
            for entry in path.iterdir():
                if entry.is_dir():
                    found.append((entry.name, 'Unknown', 'Unknown', str(entry)))
    return found

# --- Main execution logic ---
def main():
    header = f"{'Program Name':<40} {'Version':<20} {'Publisher':<30} {'Install Location'}"
    separator = "=" * len(header)

    log_and_print("=== Installed Applications Report ===", Fore.CYAN)
    log_and_print(f"Generated: {datetime.datetime.now()}\n", Fore.CYAN)
    log_and_print(header, Fore.YELLOW)
    log_and_print(separator, Fore.YELLOW)

    # Define registry paths to scan
    reg_paths = [
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    ]

    # Collect installed software from registry
    all_software = []
    for hive, subkey in reg_paths:
        log_and_print(f"Scanning: {hive}\\{subkey}", Fore.BLUE)
        all_software.extend(get_software_from_registry(hive, subkey))

    # Include folder scans from common install directories
    log_and_print("\nScanning Program Files directories...", Fore.BLUE)
    scanned_folders = scan_common_program_dirs()

    seen_names = set()
    final_software = []

    for name, version, publisher, location in sorted(all_software + scanned_folders, key=lambda x: x[0].lower()):
        if name.lower() not in seen_names:
            seen_names.add(name.lower())
            log_and_print(f"{name:<40} {version:<20} {publisher:<30} {location}")
            final_software.append((name, version, publisher, location))

    # Save CSV file 
    with open(csv_log_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Program Name", "Version", "Publisher", "Install Location"])
        writer.writerows(final_software)

    log_and_print(f"\nReport saved to TXT: {txt_log_file}", Fore.GREEN)
    print(Fore.GREEN + f"CSV report saved to: {csv_log_file}")

if __name__ == '__main__':
    main()
