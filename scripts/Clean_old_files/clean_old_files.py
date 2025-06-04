import os
import shutil
import time
from datetime import datetime
import logging

# --- Setup Logging ---
log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "clean_old_files.log")
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

print("\n=== Old File Cleaner ===\n")

# --- Get User Input ---
target_dir = input("Enter the full path of the folder to clean: ").strip()
while not os.path.isdir(target_dir):
    print("Invalid path. Please try again.")
    target_dir = input("Enter the full path of the folder to clean: ").strip()

archive_dir = input("Enter the full path of the archive folder (optional, leave blank to skip archiving): ").strip()
archive_enabled = bool(archive_dir)
if archive_enabled:
    os.makedirs(archive_dir, exist_ok=True)

try:
    days_old = int(input("Delete or archive files older than how many days? "))
except ValueError:
    print("Invalid number. Defaulting to 30 days.")
    days_old = 30

cutoff_time = time.time() - (days_old * 86400)

# === Cleanup Logic ===

def is_old_enough(file_path):
    file_mtime = os.path.getmtime(file_path)
    return file_mtime < cutoff_time

def process_file(file_path):
    if archive_enabled:
        dest_path = os.path.join(archive_dir, os.path.basename(file_path))
        shutil.move(file_path, dest_path)
        print(f"[ARCHIVED] {file_path}")
        logging.info(f"Archived: {file_path} -> {dest_path}")
    else:
        os.remove(file_path)
        print(f"[DELETED] {file_path}")
        logging.info(f"Deleted: {file_path}")

def scan_old_files():
    old_files = []
    for root, _, files in os.walk(target_dir):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                if is_old_enough(full_path):
                    old_files.append(full_path)
            except Exception as e:
                print(f"[ERROR] Failed to check {full_path}: {e}")
    return old_files

def clean_directory():
    print(f"\n[SCAN] Checking for files older than {days_old} days in:\n{target_dir}\n")
    files_to_clean = scan_old_files()

    if not files_to_clean:
        print("[INFO] No files found matching criteria.")
        return

    print(f"\nFound {len(files_to_clean)} file(s) to {'archive' if archive_enabled else 'delete'}:")
    for f in files_to_clean:
        print("  -", f)

    confirm = input("\nProceed with cleanup? (y/n): ").strip().lower()
    if confirm != 'y':
        print("[CANCELLED] No files were modified.")
        return

    for file_path in files_to_clean:
        try:
            process_file(file_path)
        except Exception as e:
            print(f"[ERROR] Could not process {file_path}: {e}")
            logging.error(f"Error processing {file_path}: {e}")

    print(f"\n[COMPLETE] Cleanup finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    clean_directory()
