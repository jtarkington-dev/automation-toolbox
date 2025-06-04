import os
import platform
import socket
import psutil
import datetime
import logging
import shutil
import subprocess

try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPUtil = None
    GPU_AVAILABLE = False

# --- Setup logging ---
script_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(script_dir, "logs")
os.makedirs(log_dir, exist_ok=True)
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = os.path.join(log_dir, f"system_info_{timestamp}.txt")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(message)s'
)

def log_and_print(message):
    print(message)
    logging.info(message)

def get_os_build_number():
    if platform.system() == "Windows":
        return platform.version()
    elif platform.system() == "Linux":
        try:
            return subprocess.check_output("uname -r", shell=True).decode().strip()
        except Exception:
            return "Unknown"
    else:
        return "Unknown"

def gather_system_info():
    log_and_print("=== System Information Report ===")
    log_and_print(f"Generated: {datetime.datetime.now()}")
    log_and_print(f"Hostname: {socket.gethostname()}")
    log_and_print(f"OS: {platform.system()} {platform.release()} (Build: {get_os_build_number()})")
    log_and_print(f"Architecture: {platform.machine()}")
    log_and_print(f"Processor: {platform.processor()}")
    log_and_print(f"Python Version: {platform.python_version()}")
    log_and_print("")

    # --- Memory Info ---
    mem = psutil.virtual_memory()
    log_and_print("=== Memory Information ===")
    log_and_print(f"Total: {mem.total / (1024 ** 3):.2f} GB")
    log_and_print(f"Available: {mem.available / (1024 ** 3):.2f} GB")
    log_and_print(f"Used: {mem.used / (1024 ** 3):.2f} GB ({mem.percent}%)")

    # --- Disk Info ---
    log_and_print("\n=== Disk Usage ===")
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            log_and_print(f"{part.device} on {part.mountpoint}: {usage.free / (1024 ** 3):.2f} GB free of {usage.total / (1024 ** 3):.2f} GB")
        except PermissionError:
            log_and_print(f"{part.device} - Permission Denied")

    # --- GPU Info ---
    log_and_print("\n=== GPU Information ===")
    if GPU_AVAILABLE:
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                for gpu in gpus:
                    log_and_print(f"GPU: {gpu.name} | Memory Free: {gpu.memoryFree}MB | Memory Used: {gpu.memoryUsed}MB | Load: {gpu.load * 100:.1f}%")
            else:
                log_and_print("No compatible GPU detected (likely integrated graphics).")
        except Exception as e:
            log_and_print(f"[ERROR] GPUtil error: {e}")
    else:
        log_and_print("[WARNING] GPUtil is not installed. Skipping GPU info.")

    # --- Environment Variables ---
    log_and_print("\n=== Environment Variables ===")
    for key, value in os.environ.items():
        log_and_print(f"{key} = {value}")

if __name__ == "__main__":
    gather_system_info()
    print(f"\nSystem information saved to: {log_file}")
